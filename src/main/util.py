import re

PATTERN_ADD = re.compile("\\n+(.*?)]\\n ")
PATTERN_REMOVE = re.compile("\\n-(.*?)]\\n ")


# commit_respond API /repos/{owner}/{repo}/commits/{ref}
# patch = commit_respond['files']['patch']

def get_added_rows(patch: str) -> list[str]:
    return re.findall(PATTERN_ADD, patch)


def get_removed_rows(patch: str) -> list[str]:
    return re.findall(PATTERN_REMOVE, patch)
