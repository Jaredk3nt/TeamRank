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

def pageRank(teams):
	for i in range(100):
		scoreHolder = {team.id: 0.0 for team in teams}
		for team in teams:
			tempLosses = {team.id: 0 for team in teams}
			numLosses = 0
			for match in team.matches:
				losses = match["losses"]
				#print("{} loses {} to {}".format(team.id, losses, match["team"].id))
				if(losses > 0):
					numLosses = numLosses + losses
					tempLosses[match["team"].id] = tempLosses[match["team"].id] + losses
			# Loop through teams and give score if lost to
			for (key, value) in tempLosses.items():
				if(value > 0):
					scoreHolder[key] = scoreHolder[key] + (value * (team.score/numLosses)) # Give score based on numlosses to team as proportion to total losses
		# Normalize the scores
		maxScore = 0
		for (key, value) in scoreHolder.items():
			#print("{} : {}".format(key,value))
			if (value > maxScore):
				maxScore = value
		for (key, value) in scoreHolder.items():
			if (value > 0):
				team = getTeam(teams, key)
				team.score = value/maxScore

def teamRank(teams):
	# Giving 10 iterations to converge
	for i in range(50):
		lowScore = 0.0
		maxScore = -10000.0
		#scoreHolder = [0.0 for x in range(len(teams))] # holder with new score
		scoreHolder = {team.id: 0.0 for team in teams}
		for team in teams:
			for match in team.matches:
				if (match["team"].score > 0):
					# matchScore = (match["wins"] * match["team"].score) - (match["losses"] * match["team"].score)
					matchScore = (match["wins"] - match["losses"]) * match["team"].score
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

def sortTeams(teams):
	return sorted(teams, key=lambda team: -team.score)

def jsonOut(teams, filename):
	with open(filename, 'w') as f:
		f.write('{"ranking": [')
		for i in range(len(teams)):
			team = teams[i]
			outLine = "{ \"team\": \"" + team.name + "\", \"wins\": " + str(team.wins) + ", \"losses\": " + str(team.losses) + ", \"score\": " + str(team.score) + " }" #.format(team.name, team.wins, team.losses, team.score)
			if(i < len(teams) - 1):
				outLine = outLine + ","
			f.write(outLine)
		f.write("]}")
	print("Wrote out to : {}".format(filename))

def printTeams(teams):
	for x in range(len(teams)):
		team = teams[x]
		#outLine = "{0}. {1}	{2}-{3} ({4:.2f})\n".format(i, team.name, team.wins, team.losses, team.score)
		#print("{0}. {1} ({2:.2f})".format(x+1, team.name, team.score))
		print("    {0}. {1:22} have won {2:2} maps and lost {3:2} maps after playing {4:2} matches. Their score is {5:.2f}".format(x+1, team.name, team.wins, team.losses, len(team.matches), team.score))

def weekByWeek(teams):
	week1 = open("week1.txt", "r")
	playGames(teams, week1)
	pageRank(teams)
	print("Week 1 Standings:")
	week1ranking = sortTeams(teams)
	jsonOut(week1ranking, "week1ranking.json")
	week1.close()

	week2 = open("week2.txt", "r")
	playGames(teams, week2)
	pageRank(teams)
	print("Week 2 Standings:")
	week2ranking = sortTeams(teams)
	jsonOut(week2ranking, "week2ranking.json")
	week2.close()

	week3 = open("week3.txt", "r")
	playGames(teams, week3)
	pageRank(teams)
	print("Week 3 Standings:")
	week3ranking = sortTeams(teams)
	jsonOut(week3ranking, "week3ranking.json")
	week3.close()

	week4 = open("week4.txt", "r")
	playGames(teams, week4)
	pageRank(teams)
	print("Week 4 Standings:")
	week4ranking = sortTeams(teams)
	jsonOut(week4ranking, "week4ranking.json")
	week4.close()

def main():
	# Setup teams
	teams = [ Team("Los Angeles Valiant", "val"), Team("Houston Outlaws", "hou"), Team("San Francisco Shock", "sfs"), Team("Los Angeles Gladiators", "gla"), Team("Seoul Dynasty", "seo"), Team("London Spitfire", "ldn"), Team("New York Excelsior", "nye"), Team("Philadelphia Fusion", "phi"), Team("Boston Uprising", "bos"), Team("Dallas Fuel", "dal"), Team("Florida Mayhem", "fla"), Team("Shanghai Dragons", "shd") ]

	weekByWeek(teams)

	

if __name__ == "__main__":
    main()



