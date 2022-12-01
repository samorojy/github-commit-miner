import aiohttp
import asyncio
import json
import requests
from urllib.parse import parse_qs, urlparse
from collections import OrderedDict, namedtuple
from print_commits import print_commits

GITHUB_API = 'https://api.github.com/'
COMMITS_API = 'repos/{}/{}/commits?'
QUERY_PARAMETERS = 'page={}&per_page={}'

Commit = namedtuple('Commit', ['num', 'message', 'removed', 'added'])
commits = OrderedDict()


def count_commits_pages(owner: str, repo: str, commits_on_page: int = 100) -> int:
    """
    Returns the number of pages of commits to a GitHub repository.
    """
    url = GITHUB_API + COMMITS_API.format(owner, repo) + QUERY_PARAMETERS.format(1, commits_on_page)
    r = requests.get(url)
    links = r.links
    rel_last_link_url = urlparse(links["last"]["url"])
    rel_last_link_url_args = parse_qs(rel_last_link_url.query)
    rel_last_link_url_page_arg = rel_last_link_url_args["page"][0]
    commits_count = int(rel_last_link_url_page_arg)
    return commits_count


async def download_commits_page(session: aiohttp.ClientSession, owner: str, repo: str, page: int,
                                commits_on_page: int = 100):
    url = GITHUB_API + COMMITS_API.format(owner, repo) + QUERY_PARAMETERS.format(page, commits_on_page)
    async with session.get(url) as response:
        commits_list = await response.json()
        for i in commits_list:
            try:
                commit_info = requests.get(i['url']).json()
            except TypeError:
                print('\033[91mProbably your API rate limit exceeded.\nLast accepted respond: \n \033[0m')
                print(commits_list)
            try:
                commits[page] = Commit(page, i['commit']['message'], commit_info['stats']['deletions'],
                                       commit_info['stats']['additions'])
            except KeyError:
                print('\033[91mProbably your API rate limit exceeded.\nLast accepted respond: \n \033[0m')
                print(commit_info)


async def download_commits(owner: str, repo: str):
    async with aiohttp.ClientSession() as session:
        pages_num = 1
        # count_commits_pages(owner, repo)
        tasks = [asyncio.create_task(download_commits_page(session, owner, repo, i)) for i in range(0, pages_num)]
        await asyncio.gather(*tasks)


def scrap_commits(output_path: str, owner: str, repo: str, branch: str):
    """
    Scraping list of commit from given repo and printing it in file
    """
    asyncio.new_event_loop().run_until_complete(download_commits(owner, repo))
    print_commits(output_path, commits)
