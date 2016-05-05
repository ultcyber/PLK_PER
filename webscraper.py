# Local modules imports
from algorithms import PERCalculator
# Packages
from bs4 import BeautifulSoup
from functools import reduce
import re
import requests

# Prepare the xml for parsing

def cook_soup(url, data):
	r = requests.post(url, data=data)
	print(r.status_code)
	return BeautifulSoup(r.text, "lxml")

# Make a dictionary of {Player : Team}

def player_team(soup):

	player_team = {}

	players = soup("td", class_="zawodnik")
	teams = soup("td", class_="druzyna2")

	for i in range(len(players)):
		a = players[i].find("strong").string
		b = teams[i].find("a").string
		player_team[a] = b

	return player_team

# Capturing AJAX and parsing

def parse(soup, sibl_end, team=False, name=False):

	# Help function
	# Search for next sibling, i.e. column until the specified number (determined by the sibl_end parameter)
	def find_column(element):
		count = 0
		while count < sibl_end:
			element = element.next_sibling
			count += 1
		return element.string
	
	# Find teams' rows
	trows = soup("td", class_="druzyna")
	# Find player's rows
	prows = soup("td", class_="zawodnik")

	# If the team parameter is specified - return team stats. If not, check for player's, else return League stats
	if team:
	# Find the team's row
		for ind, row in enumerate(trows):
			a = row.find("strong")
			# print(a) # Just for testing
			if team in a.string:
				break
		return float(find_column(trows[ind]))
	elif name:
		for ind, row in enumerate(prows):
			a = row.find("strong")
			# print(a) # Just for testing
			if name in a.string:
				break
		return float(find_column(prows[ind]))
	else:
		results = []
		for row in trows:
			results.append(find_column(row))
		#print(results) # Just for testing
		average = reduce(lambda x, y: float(x)+float(y), results)/(len(results)+1)
		return round(average,2)


# Calculating the league stats

team_soup = cook_soup(url = 'http://plk.pl/statystyki/xml/1.html', data = {'f':1, 's':18, 'o':'Pkt', 'wh':'g1', 'r':'0', 'nocontent':1, 'X-Requested-With': 'XMLHttpRequest'})

lpoints = parse(team_soup, 4)
lfieldgoals = parse(team_soup, 18)
lafieldgoals = parse(team_soup, 20)
lfreethrows = parse(team_soup, 24)
lafreethrows = parse(team_soup, 26)
lorebounds = parse(team_soup, 30)
ltrebounds = parse(team_soup, 34)
lassists = parse(team_soup, 36)
lpfouls = parse(team_soup, 38)
lturnovers = parse(team_soup, 42)


# Initiate a new PERCalculator for a player

player = PERCalculator("Danny Gibson")

# Calculate team stats

player.tassists = parse(team_soup, 36, team = "PGE Turów Zgorzelec")
player.tfieldgoals = parse(team_soup, 6, team = "PGE Turów Zgorzelec" )

# Assigning league stats
player.lpoints = lpoints
player.lfieldgoals = lfieldgoals
player.lafieldgoals = lafieldgoals
player.lfreethrows = lfreethrows
player.lafreethrows = lafreethrows
player.lorebounds = lorebounds
player.ltrebounds = ltrebounds
player.lassists = lassists
player.lpfouls = lpfouls
player.lturnovers = lturnovers

# Calculate individual stats

# Help function for assigning individual attributes
def ass_ind_attr(wh, stat, sib=6):
	soup = cook_soup(url = 'http://plk.pl/statystyki/xml/0.html', data = {'f':0, 's':18, 'o':0, 'wh':wh, 'r':'0', 'nocontent':0, 'X-Requested-With': 'XMLHttpRequest'})
	setattr(player, stat, parse(soup, sib, name=player.name))

ass_ind_attr("g0", "minutes")
ass_ind_attr("g7", "assists")
ass_ind_attr("g9", "steals")
ass_ind_attr("g10", "blocks")
ass_ind_attr("g8", "turnovers")
ass_ind_attr("g11", "pfouls")
ass_ind_attr("g4", "threepoints")
ass_ind_attr("g2", "fieldgoals")
ass_ind_attr("g2", "afieldgoals", sib=8)
ass_ind_attr("g5", "freethrows")
ass_ind_attr("g5", "afreethrows", sib=8)

player.calculateDRBpct()
player.calculateVOP()
player.calculateFactor()

print(vars(player))
player.calculateuPER()
