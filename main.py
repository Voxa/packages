from urllib import request
from json import loads
from chevron import render

ORG_USERNAME = "voxa"
TOPICS_LIST = ["open-source"]


org_request = request.Request(f"https://api.github.com/orgs/{ORG_USERNAME}")
org = loads(request.urlopen(org_request).read())
org_name = org["name"]
site_url = org["blog"]

repo_request = request.Request(org["repos_url"])
repos = loads(request.urlopen(repo_request).read())

projects = []

for repo in repos:
    repo_url = repo["url"]

    topics_request = request.Request(f"{repo_url}/topics", headers={
        "Accept": "application/vnd.github.mercy-preview+json"
    })

    topics = loads(request.urlopen(topics_request).read())["names"]

    if not set(TOPICS_LIST).isdisjoint(topics):
        project_name = repo["name"]
        url = repo["html_url"]
        description = repo["description"]

        projects.append({
            "project_name": project_name,
            "url": url,
            "description": description
        })

with open("./index.mustache", "r") as template:
    index_html = render(template, {
        "org_name": org_name,
        "site_url": site_url,
        "projects": projects
    })

    with open("./index.html", "w") as index:
        index.write(index_html)
