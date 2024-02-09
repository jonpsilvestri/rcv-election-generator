# Generating random ranked choice voting (RCV) election data

The program can take the following commandline arguments

- `--num-voters`: the number of voters in the election (default: 10)
- `--num-candidates`: the number of candidates in the election (default: 3)
- `--max-unique-rankings`: the maximum number of unique rankings to generate (default: num_voters)
- `--max-ranking-length`: the maximum length of a ranking (default: num-candidates)
- `--min-ranking-length`: the minimum length of a ranking (default: num-candidates)
- `--num-elections`: the number of elections to generate (default: 1)
- `--output-file`: the file to write the election. (If not specified, the election will be written to stdout.)

## Output Format

If an output-file is specified, the output file will be a JSON file with the following format:

```json
{
    "num_voters": 10,
    "num_candidates": 3,
    "max_unique_rankings": 4,
    "max_ranking_length": 3,
    "min_ranking_length": 3,
    "num_elections": 1,
    "elections" : [
        {
            "ballots": [
                {
                    "ranking": [1, 2, 0],
                    "count": 4
                },
                {
                    "ranking": [2, 1, 0],
                    "count": 3
                },
                {
                    "ranking": [0, 1, 2],
                    "count": 1
                },
                {
                    "ranking": [1, 0, 2],
                    "count": 2
                }
            ]
        }
    ]
}
```

The `ballots` array contains the ballots in the election. Each ballot has a `ranking` array, which contains the ranking of the candidates. The `count` field indicates how many ballots have that ranking.

## Code sharing

While you may not share code with other students, you may discuss the assignment with other students.

You may also share code that is meant to test your program. For example, you may share code that reads the JSON file and verifies that the election is valid given the parameters.
