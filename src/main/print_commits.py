import csv
from collections import OrderedDict, namedtuple

HEADER = ["commit_#", "commit_message", "diff_+", "diff_-"]


def print_commits(output_path: str, commits: OrderedDict):
    with open(output_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(HEADER)
        for i in commits.values():
            try:
                writer.writerow([i[0], i[1], i[3], i[2]])
            except UnicodeEncodeError:
                print("\033[91mCommit info contains weird symbols\n \033[0m")
