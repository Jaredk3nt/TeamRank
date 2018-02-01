class Team:
	def __init__(self, name, id):
		self.name = name
		self.id = id
		self.wins = 0
		self.losses = 0
		self.score = 1.0 # start at 1 to get the algorithm going
		self.matches = []

	def playTeam(self, team, wins, losses):
		self.wins = self.wins + wins
		self.losses = self.losses + losses
		self.matches.append({"wins": wins, "losses": losses, "team": team})

def teamRank(teams):
	# Giving 10 iterations to converge
	for i in range(2):
		lowScore = 0.0
		maxScore = -10000.0
		scoreHolder = [0.0 for x in range(len(teams))] # holder with past score
		for team in teams:
			for match in team.matches:
				if (match["team"].score > 0):
					matchScore = (match["wins"] * match["team"].score) - (match["losses"] / match["team"].score)
					#print("{} wins {} and loses {} for a score of {}".format(team.name, match["wins"], match["losses"], matchScore))
					scoreHolder[team.id - 1] = scoreHolder[team.id - 1] + matchScore
			# Track low score to remove negatives later on
			if (scoreHolder[team.id - 1] < lowScore):
				lowScore = scoreHolder[team.id - 1]
		# get rid of the negatives and track high score to normalize
		for team in teams:
			team.score = scoreHolder[team.id - 1] + abs(lowScore)
			if (team.score > maxScore):
				maxScore = team.score
		# Normalize by the maximum score
		for team in teams:
			team.score = team.score / maxScore

	# While not converged
		# Go through each team's matches
			# set team score to sum of (wins vs team) / (opponents score)
			# keep track of scores in a totalScore var
		# normalize by setting each teams score to score / totalScore
		# Repeat until stablized

def getTeam(teams, id):
	for i in range(len(teams)):
		if (teams[i].id == id):
			return teams[i]

def playGames(teams, matches):
	totalWins = 0
	for match in matches.splitlines():
		team1id, team1Wins, team2id, team2Wins = (int(s) for s in match.split())
		team1 = getTeam(teams, team1id)
		team2 = getTeam(teams, team2id)
		#print("{} won {} and lost {} to {}".format(team1.name, team1Wins, team2Wins, team2.name))
		team1.playTeam(team2, team1Wins, team2Wins)
		team2.playTeam(team1, team2Wins, team1Wins)
		totalWins = totalWins + team1Wins + team2Wins
	return totalWins

def sortTeams(teams):
	printTeams(sorted(teams, key=lambda team: -team.score))

def printTeams(teams):
	for x in range(len(teams)):
		team = teams[x]
		print("{0}. {1:22} have won {2:2} maps and lost {3:2} maps after playing {4:2} matches. Their score is {5:.2f}".format(x+1, team.name, team.wins, team.losses, len(team.matches), team.score))

def main():
	# Setup teams
	teams = [ Team("Los Angeles Valiant", 1), Team("Houston Outlaws", 2), Team("San Francisco Shock", 3), Team("Los Angeles Gladiators", 4), Team("Seoul Dynasty", 5), Team("London Spitfire", 6), Team("New York Excelsior", 7), Team("Philidelphia Fusion", 8), Team("Boston Uprising", 9), Team("Dallas Fuel", 10), Team("Florida Mayhem", 11), Team("Shanghai Dragons", 12) ]
	# Go through teams and simulate all matches
	# read file of matches with format:
		# <team1 id> <matches won> <team2 id> <matches won>
		# 1 4 4 0
		# ties count as a loss for both sides
	week1 = """3 0 1 4
12 0 4 4
10 1 5 2
6 3 11 1
8 3 2 2
9 1 7 3
1 3 10 0
11 0 9 4
3 3 12 1
6 4 8 0
7 3 2 1
5 4 4 0
3 1 8 2
11 0 5 4
2 4 12 0
10 0 2 4
7 3 1 0
8 2 4 3
5 4 9 0
12 0 11 4
6 3 10 1
1 2 6 3
4 0 7 4
9 2 3 3
3 1 6 3
12 1 5 3
4 2 1 3
9 3 6 2
8 3 7 2
2 4 11 0
5 2 7 3
12 2 8 3
10 3 3 0
10 2 9 3
1 3 11 1
4 0 2 4
1 4 8 0
11 1 4 3
2 3 3 1"""
	totalWins = playGames(teams, week1)
	#printTeams(teams)
	teamRank(teams)
	sortTeams(teams)

if __name__ == "__main__":
    main()



