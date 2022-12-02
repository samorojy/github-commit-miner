import aiohttp
import asyncio
import json
import requests
from urllib.parse import parse_qs, urlparse
from collections import OrderedDict, namedtuple
from print_commits import print_commits

GITHUB_API = "https://api.github.com/"
COMMITS_API = "repos/{}/{}/commits?"
QUERY_PARAMETERS = "page={}&per_page={}"
AUTHORIZATION = "Authorization"

Commit = namedtuple("Commit", ["num", "message", "removed", "added"])
commits = OrderedDict()


def count_commits_pages(owner: str, repo: str, header: dict, commits_on_page: int = 100) -> int:
    """
    Returns the number of pages of commits to a GitHub repository.
    """
    url = GITHUB_API + COMMITS_API.format(owner, repo) + QUERY_PARAMETERS.format(1, commits_on_page)
    commits_count = 1
    r = requests.get(url, headers=header)
    links = r.links
    try:
        rel_last_link_url = urlparse(links["last"]["url"])
        rel_last_link_url_args = parse_qs(rel_last_link_url.query)
        rel_last_link_url_page_arg = rel_last_link_url_args["page"][0]
        commits_count = int(rel_last_link_url_page_arg)
    except KeyError:
        print("\033[91mThere are 1 commits page or your API rate limit exceeded.\nLast accepted respond: \n \033[0m")
        print(r.json())
    return commits_count


async def download_commits_page(
    session: aiohttp.ClientSession, owner: str, repo: str, page: int, header: dict, commits_on_page: int = 100
):
    url = GITHUB_API + COMMITS_API.format(owner, repo) + QUERY_PARAMETERS.format(page, commits_on_page)
    async with session.get(url) as response:
        commits_list = await response.json()
        commit_counter = 0
        for i in commits_list:
            commit_number = page * commits_on_page + commit_counter
            try:
                commit_info = requests.get(i["url"], headers=header).json()
                print(f"Processing commit {commit_number}")
                commits[commit_number] = Commit(
                    commit_number,
                    i["commit"]["message"],
                    commit_info["stats"]["deletions"],
                    commit_info["stats"]["additions"],
                )
                commit_counter += 1
            except TypeError:
                print("\033[91mProbably your API rate limit exceeded.\nLast accepted respond: \n \033[0m")
                print(commits_list)
            except KeyError:
                print("\033[91mProbably your API rate limit exceeded.\nLast accepted respond: \n \033[0m")
                print(commit_info)


async def download_commits(owner: str, repo: str, token: str, pages: int):
    header = {}
    if token != "":
        header = {AUTHORIZATION: "token " + token}
    async with aiohttp.ClientSession(headers=header) as session:
        if pages < 0:
            pages = count_commits_pages(owner, repo, header)
        tasks = [asyncio.create_task(download_commits_page(session, owner, repo, i, header)) for i in range(0, pages)]
        await asyncio.gather(*tasks)


def scrap_commits(output_path: str, owner: str, repo: str, token: str, pages: int):
    """
    Scraping list of commit from given repo and printing it in file
    """
    asyncio.new_event_loop().run_until_complete(download_commits(owner, repo, token, pages))
    print_commits(output_path, commits)
