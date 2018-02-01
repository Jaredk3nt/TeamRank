class Team:
	def __init__(self, name, id):
		self.name = name
		self.id = id
		self.wins = 0
		self.losses = 0
		self.ties = 0
		self.score = 1.0 # start at 1 to get the algorithm going
		self.matches = []

	def playTeam(self, team, wins, losses, ties):
		self.wins = self.wins + wins
		self.losses = self.losses + losses
		self.ties = self.ties + ties
		self.matches.append({"wins": wins, "losses": losses, "ties": ties, "team": team})

def teamRank(teams):
	# Giving 10 iterations to converge
	for i in range(100):
		lowScore = 0.0
		maxScore = -10000.0
		#scoreHolder = [0.0 for x in range(len(teams))] # holder with new score
		scoreHolder = {team.id: 0.0 for team in teams}
		for team in teams:
			for match in team.matches:
				if (match["team"].score > 0):
					matchScore = (match["wins"] * match["team"].score) - (match["losses"] / match["team"].score)
					#print("{} wins {} and loses {} for a score of {}".format(team.name, match["wins"], match["losses"], matchScore))
					scoreHolder[team.id ] = scoreHolder[team.id] + matchScore
			# Track low score to remove negatives later on
			if (scoreHolder[team.id] < lowScore):
				lowScore = scoreHolder[team.id]
		# get rid of the negatives and track high score to normalize
		for team in teams:
			team.score = scoreHolder[team.id] + abs(lowScore)
			if (team.score > maxScore):
				maxScore = team.score
		# Normalize by the maximum score
		for team in teams:
			team.score = team.score / maxScore

def getTeam(teams, id):
	for i in range(len(teams)):
		if (teams[i].id == id):
			return teams[i]

def playGames(teams, matches):
	totalWins = 0
	for match in matches:
		matchGenerator = (s for s in match.split())
		team1id = next(matchGenerator) 
		team1Wins = int(next(matchGenerator)) 
		team2id = next(matchGenerator) 
		team2Wins = int(next(matchGenerator))
		ties = int(next(matchGenerator, 0)) # get ties if any, otherwise 0

		team1 = getTeam(teams, team1id)
		team2 = getTeam(teams, team2id)

		team1.playTeam(team2, team1Wins, team2Wins, ties)
		team2.playTeam(team1, team2Wins, team1Wins, ties)
		totalWins = totalWins + team1Wins + team2Wins
	return totalWins

def sortTeams(teams):
	printTeams(sorted(teams, key=lambda team: -team.score))

def printTeams(teams):
	for x in range(len(teams)):
		team = teams[x]
		#print("{0}. {1} ({2:.2f})".format(x+1, team.name, team.score))
		print("    {0}. {1:22} have won {2:2} maps and lost {3:2} maps after playing {4:2} matches. Their score is {5:.2f}".format(x+1, team.name, team.wins, team.losses, len(team.matches), team.score))

def main():
	# Setup teams
	teams = [ Team("Los Angeles Valiant", "val"), Team("Houston Outlaws", "hou"), Team("San Francisco Shock", "sfs"), Team("Los Angeles Gladiators", "gla"), Team("Seoul Dynasty", "seo"), Team("London Spitfire", "ldn"), Team("New York Excelsior", "nye"), Team("Philadelphia Fusion", "phi"), Team("Boston Uprising", "bos"), Team("Dallas Fuel", "dal"), Team("Florida Mayhem", "fla"), Team("Shanghai Dragons", "shd") ]

	matches = open("matches.txt", "r")

	playGames(teams, matches)
	#printTeams(teams)
	teamRank(teams)
	sortTeams(teams)

if __name__ == "__main__":
    main()



