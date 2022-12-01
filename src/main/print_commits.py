import csv
from collections import OrderedDict, namedtuple

HEADER = ['commit_#', 'commit_message', 'diff_', 'diff_-']


def print_commits(output_path: str, commits: OrderedDict):
    with open(output_path, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(HEADER)
        for i in OrderedDict:
            writer.writerow(i)
