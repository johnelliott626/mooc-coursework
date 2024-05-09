# Simulate a sports tournament

import csv
import sys
import random

# Number of simluations to run
N = 1000


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    teams = []
    # TODO: Read teams into memory from file
    filename = sys.argv[1]
    with open(filename) as file:
        reader = csv.DictReader(file)
        # create a dictionary object for each row, add that object to the list of teams
        for row in reader:
            row['rating'] = int(row['rating'])
            teams.append(row)

    counts = {}
    # TODO: Simulate N tournaments and keep track of win counts
    # maps keys to values, names of teams to how many wins for that given team
    for i in range(N):
        name = simulate_tournament(teams)
        if name in counts:
            counts[name] += 1
        else:
            counts[name] = 1

    # Print each team's chances of winning, according to simulation
    for team in sorted(counts, key=lambda team: counts[team], reverse=True):
        print(f"{team}: {counts[team] * 100 / N:.1f}% chance of winning")


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""
    rating1 = team1["rating"]
    rating2 = team2["rating"]
    probability = 1 / (1 + 10 ** ((rating2 - rating1) / 600))
    return random.random() < probability


def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""
    winners = []

    # Simulate games for all pairs of teams
    for i in range(0, len(teams), 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])

    return winners


def simulate_tournament(teams):
    """Simulate a tournament. Return name of winning team."""
    # TODO Continuously simulate rounds until it returns a single team in its return list (the winner)
    while (len(teams) > 1):
        teams = simulate_round(teams)
    
    name = teams[0]['team']
    return name


if __name__ == "__main__":
    main()
