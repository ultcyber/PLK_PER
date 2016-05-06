# Local modules imports
from algorithms import PERCalculator
from webscraper import cook_soup, parse, opponent_parse
# Packages
from bs4 import BeautifulSoup
from functools import reduce
import re
import requests

# Creating a blueprint that will later be an object holding soups for individual stats
# That helps limit the number of requests to the website

class StatSoup(object):
	def __init__(self):
		pass


def main():
	global team_soup
	global teamaverage_soup
	global lpoints 
	global lfieldgoals
	global lafieldgoals
	global lfreethrows
	global lafreethrows
	global lorebounds
	global ltrebounds
	global lassists
	global lpfouls
	global lturnovers
	global lpointspg
	global pot

	# Calculating the league stats

	team_soup = cook_soup(url = 'http://plk.pl/statystyki/xml/1.html', data = {'f':1, 's':18, 'o':'Pkt', 'wh':'g1', 'r':'0', 'nocontent':1, 'X-Requested-With': 'XMLHttpRequest'})
	teamaverage_soup = cook_soup(url = 'http://plk.pl/statystyki/xml/1.html', data = {'f':0, 's':18, 'o':'Pkt', 'wh':'g0', 'r':'0', 'nocontent':1})
	
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
	lpointspg = parse(teamaverage_soup, 4)

	# Setting object that holds soups for individual stats

	pot = StatSoup()
	def add_to_pot(wh, stat):
		soup = cook_soup(url = 'http://plk.pl/statystyki/xml/0.html', data = {'f':0, 's':18, 'o':0, 'wh':wh, 'r':'0', 'nocontent':0, 'X-Requested-With': 'XMLHttpRequest'})
		setattr(pot, stat, soup)

	add_to_pot("g0", "minutes")
	add_to_pot("g7", "assists")
	add_to_pot("g9", "steals")
	add_to_pot("g10", "blocks")
	add_to_pot("g8", "turnovers")
	add_to_pot("g11", "pfouls")
	add_to_pot("g4", "threepoints")
	add_to_pot("g2", "fieldgoals")
	add_to_pot("g2", "afieldgoals")
	add_to_pot("g5", "freethrows")
	add_to_pot("g5", "afreethrows")
	add_to_pot("g6", "orebounds")
	add_to_pot("g6", "trebounds")

	# Create a dictionary of player-team
	soup = cook_soup(url = 'http://plk.pl/statystyki/xml/0.html', data = {})
	p_t = player_team(soup)


	# ----------------------------- MAIN LOOP CREATING PER DICTIONARY ---------------------------
	
	# First we need to create an aPER dictionary
	aPERdict = {}
	
	for key, value in p_t.items():
		player = PERCalculator(key, value)
		CalculatePER(player)
		print("Calculated aPER for {} which is {}".format(player.name, player.aPER))
		aPERdict[player.name] = player.aPER
		count += 1
	
	# Then let's calculate the average league aPER

	def laPERcalc(dictionary):
		values = dictionary.values()
		return reduce(lambda x, y: x+y, values)/len(values)

	laPER = laPERcalc(aPERdict)

	# Finally, let's put up the PER!

	PERdict = {}

	for key, value in aPERdict.items():
		PERdict[key] = value * (15 / laPER)

	# Then write to file

	with open('PER.txt', 'w') as f:
		for key, value in PERdict.items():
			f.write('{},{} \n'.format(key, value))

	print("Done!")

def player_team(soup):

	player_team = {}

	players = soup("td", class_="zawodnik")
	teams = soup("td", class_="druzyna2")

	for i in range(len(players)):
		a = players[i].find("strong").string
		b = teams[i].find("a").string
		player_team[a] = b

	return player_team

def CalculatePER(player):

	global team_soup
	global teamaverage_soup
	global lpoints 
	global lfieldgoals
	global lafieldgoals
	global lfreethrows
	global lafreethrows
	global lorebounds
	global ltrebounds
	global lassists
	global lpfouls
	global lturnovers
	global lpointspg
	global pot

	# Calculate team stats

	player.tassists = parse(team_soup, 36, team = player.team)
	player.tfieldgoals = parse(team_soup, 18, team = player.team)
	player.tafieldgoals = parse(team_soup, 20, team = player.team)
	player.tafreethrows = parse(team_soup, 26, team = player.team)
	player.tturnovers = parse(team_soup, 42, team = player.team)
	player.tpointspg = parse(teamaverage_soup, 4, team=player.team)
	player.opointspg = opponent_parse(teamaverage_soup, 4, team=player.team)

	# Assigning league stats

	player.lpoints = lpoints
	player.lfieldgoals = lfieldgoals
	player.lafieldgoals = lafieldgoals
	player.lpointspg = lpointspg
	player.lfreethrows = lfreethrows
	player.lafreethrows = lafreethrows
	player.lorebounds = lorebounds
	player.ltrebounds = ltrebounds
	player.lassists = lassists
	player.lpfouls = lpfouls
	player.lturnovers = lturnovers

	# Calculate individual stats

	# Help function for assigning individual attributes
	def ass_ind_attr(stat, sib=6, pot=pot):
		soup = getattr(pot, stat)
		setattr(player, stat, parse(soup, sib, name=player.name))

	ass_ind_attr("minutes")
	ass_ind_attr("assists")
	ass_ind_attr("steals")
	ass_ind_attr("blocks")
	ass_ind_attr("turnovers")
	ass_ind_attr("pfouls")
	ass_ind_attr("threepoints")
	ass_ind_attr("fieldgoals")
	ass_ind_attr("afieldgoals", sib=8)
	ass_ind_attr("freethrows")
	ass_ind_attr("afreethrows", sib=8)
	ass_ind_attr("orebounds")
	ass_ind_attr("trebounds", sib=10)

	player.calculateDRBpct()
	player.calculateVOP()
	player.calculateFactor()
	player.calculateuPER()
	player.estimatePaceAdjustment()
	player.calculateaPER()


if __name__ == '__main__':
	main()