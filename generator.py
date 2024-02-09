import argparse
import random
import json
from itertools import permutations, chain

def parse_input():
    parser = argparse.ArgumentParser(description='Generate random Ranked Choice Voting (RCV) elections.')

    # Add command-line arguments
    parser.add_argument('--num-voters',         type=int, default=10, help='Number of voters in the election (default: 10)')
    parser.add_argument('--num-candidates',     type=int, default=3, help='Number of candidates in the election (default: 3)')
    parser.add_argument('--max-unique-rankings',type=int, default=float('inf'), help='Max number of unique rankings (default: infinity)')
    parser.add_argument('--max-ranking-length', type=int, help='Max length of a ranking (default: num-candidates)')
    parser.add_argument('--min-ranking-length', type=int, default=None, help='Min length of a ranking (default: num-candidates)')
    parser.add_argument('--num-elections',      type=int, default=1, help='Number of elections to generate (default: 1)')
    parser.add_argument('--output-file',        type=str, help='File to write the election (If not specified, write to stdout)')

    # Parse the command-line arguments
    args = parser.parse_args()

    return args

def generate_election(num_voters, num_candidates, max_unique_rankings, max_ranking_length, min_ranking_length):
    rankings = make_rankings(min_ranking_length, max_ranking_length, max_unique_rankings, num_candidates)
    election = assign_votes(num_voters, rankings)
    return election

def assign_votes(num_voters, rankings):
    num_dividers = len(rankings) - 1
    dividers = []
    for _ in range(num_dividers):
        divider = random.randint(0, num_voters)
        dividers.append(divider)
    
    dividers = sorted(dividers)

    ballots = []
    for i in range(len(dividers) + 1):
        ballot = {"ranking": [], "count": 0}
        ranking = rankings[i]

        if i == 0:
            num_votes = dividers[i]
        elif i == len(dividers):
            num_votes = num_voters - dividers[i-1]
        else:
            num_votes = dividers[i] - dividers[i-1]

        ballot["ranking"] = ranking
        ballot["count"] = num_votes
        ballots.append(ballot)
    
    return ballots
            


def make_rankings(min_ranking_length, max_ranking_length, max_unique_rankings, num_candidates):
    # all_rankings contains every permutation of rankings of size min to max ranking lengths
    all_rankings = list(chain.from_iterable(permutations(range(num_candidates), r) for r in range(min_ranking_length, max_ranking_length + 1)))
    # if there is no limit on # of rankings or if the limit is the maximum possible amount of rankings
    if max_unique_rankings >= len(all_rankings):
        for i in range(len(all_rankings)):
            all_rankings[i] = list(all_rankings[i])
        return all_rankings
    
    # case for when there is an upper limit on amount of unique rankings
    unique_rankings = set()
    i = 0
    # pick a random ranking until we have the desired amount of rankings
    while len(unique_rankings) < max_unique_rankings:
        ind = random.randint(0, len(all_rankings)-1)
        ranking = all_rankings[ind]
        unique_rankings.add(ranking)
    
    for i in range(len(all_rankings)):
        all_rankings[i] = list(all_rankings[i])

    return list(unique_rankings)
    


if __name__ == '__main__':
    parsed_args = parse_input()
    
    num_voters = parsed_args.num_voters
    num_candidates = parsed_args.num_candidates
    max_unique_rankings = parsed_args.max_unique_rankings
    max_ranking_length = parsed_args.max_ranking_length
    if (max_ranking_length == None):
        max_ranking_length = num_candidates
    
    min_ranking_length = parsed_args.min_ranking_length
    if (min_ranking_length == None):
        min_ranking_length = num_candidates

    num_elections = parsed_args.num_elections
    output_file = parsed_args.output_file

    output = {"num_voters": num_voters,
              "num_candidates": num_candidates,
              "max_unique_rankings": max_unique_rankings,
              "max_ranking_length": max_ranking_length,
              "min_ranking_length": min_ranking_length,
              "num_elections": num_elections,
              "elections": []}

    for i in range(num_elections):
        election = generate_election(num_voters, num_candidates, max_unique_rankings, max_ranking_length, min_ranking_length)
        ballots = {"ballots": election}
        output['elections'].append(ballots)
    
    if output_file == None:
        print(json.dumps(output, indent=2))
        exit(-1)

    with open(output_file, 'w') as json_file:
        json.dump(output, json_file, indent=2)


    
    