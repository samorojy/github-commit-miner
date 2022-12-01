import argparse
from scrap_commits import scrap_commits


def main():
    parser = argparse.ArgumentParser(
        prog='Commit-miner',
        description='Scraping commits of given repo into .csv',
    )
    parser.add_argument('output_path')
    parser.add_argument('owner')
    parser.add_argument('repo')
    parser.add_argument('-b', '--branch', default="main")
    args = parser.parse_args()
    scrap_commits(args.output_path, args.owner, args.repo, args.branch)
    print(args.output_path, args.branch)


if __name__ == '__main__':
    main()
