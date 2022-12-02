# GitHub Commit Miner

cli tool for getting GitHub commits data in .csv format

To prepare:

`pip install -r requirments.txt`

to run:

`python src/main/main.py filepath repo-owner repo`

For example:

`python src/main/main.py result.csv huggingface transformers`

This command will save commit list from [huggingface/transformers](https://github.com/huggingface/transformers) to
result.csv

One more example:

`python src/main/main.py result.csv samorojy github-commit-miner`

If your API limit is exceeded use --token flag
