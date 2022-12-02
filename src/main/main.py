import argparse
from scrap_commits import scrap_commits


def main():
    parser = argparse.ArgumentParser(
        prog="Commit-miner",
        description="Scraping commits of given repo into .csv",
    )
    parser.add_argument("output_path")
    parser.add_argument("owner")
    parser.add_argument("repo")
    parser.add_argument("-p", "--pages", type=int, default="-1")
    args = parser.parse_args()
    scrap_commits(args.output_path, args.owner, args.repo, args.branch, int(args.pages))
    print(f"Successfully printed results into {args.output_path}")


if __name__ == "__main__":
    main()
