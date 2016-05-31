# Local modules imports
from algorithms import PERCalculator
from webscraper import cook_soup, parse, opponent_parse
# Packages
from bs4 import BeautifulSoup
from functools import reduce
import re
import requests
import sqlite3

# Creating a blueprint that will later be an object holding soups for individual stats
# That helps drastically limit the number of requests to the website

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

	# Create a database file with appropriate columns

	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	c.execute('DROP TABLE IF EXISTS players')
	c.execute('''CREATE TABLE players (
				id INTEGER PRIMARY KEY,
				name TEXT,
				team TEXT,
				VOP REAL,
				threepoints REAL,
				afreethrows REAL,
				lpointspg REAL,
				uPER REAL,
				pfouls REAL,
				freethrows REAL,
				afieldgoals REAL,
				fieldgoals REAL,
				lpfouls REAL,
				orebounds REAL,
				ePA REAL,
				lfreethrows REAL,
				lfieldgoals REAL,
				lturnovers REAL,
				lorebounds REAL,
				turnovers REAL,
				lassists REAL,
				assists REAL,
				tafieldgoals REAL,
				lpoints REAL,
				factor REAL,
				tpointspg REAL,
				aPER REAL,
				lafreethrows REAL,
				tafreethrows REAL,
				trebounds REAL,
				blocks REAL,
				opointspg REAL,
				lafieldgoals REAL,
				minutes REAL,
				ltrebounds REAL,
				tfieldgoals REAL,
				tassists REAL,
				tturnovers REAL,
				DRBpct REAL,
				steals REAL
									);''')

	# for testing
	# Calculate the initial PERs and insert the values into the database
	for name, team in p_t.items():

		player = PERCalculator(name, team)
		CalculatePERs(player)
		print("Calculated PERs for {}".format(player.name))

		player = vars(player)
		data = [
			player.get("name"),
			player.get("team"),
			player.get("VOP"),
			player.get("threepoints"),
			player.get("afreethrows"),
			player.get("lpointspg"),
			player.get("uPER"),
			player.get("pfouls"),
			player.get("freethrows"),
			player.get("afieldgoals"),
			player.get("fieldgoals"),
			player.get("lpfouls"),
			player.get("orebounds"),
			player.get("ePA"),
			player.get("lfreethrows"),
			player.get("lfieldgoals"),
			player.get("lturnovers"),
			player.get("lorebounds"),
			player.get("turnovers"),
			player.get("lassists"),
			player.get("assists"),
			player.get("tafieldgoals"),
			player.get("lpoints"),
			player.get("factor"),
			player.get("tpointspg"),
			player.get("aPER"),
			player.get("lafreethrows"),
			player.get("tafreethrows"),
			player.get("trebounds"),
			player.get("blocks"),
			player.get("opointspg"),
			player.get("lafieldgoals"),
			player.get("minutes"),
			player.get("ltrebounds"),
			player.get("tfieldgoals"),
			player.get("tassists"),
			player.get("tturnovers"),
			player.get("DRBpct"),
			player.get("steals")
		]

		c.execute("INSERT INTO players VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", tuple(data))	
		conn.commit()
		print("Inserted into the database!")
	

	# Then wee need to calculate the average league aPER (adjusted PER)

	# First let's create an aPER dictionary by fetching the data from the database
	c.execute('SELECT name, aPER from players')
	aPERdict = {num[0]:num[1] for num in c.fetchall()}
	# Then let's calculate the league average aPER
	aPERvalues = aPERdict.values()
	laPER = reduce(lambda x, y: x+y, aPERvalues)/len(aPERvalues)
	print("Finished making aPER dictionary!")

	# Finally, let's put up the PER!

	# Let's add a PER column to the database
	c.execute('ALTER TABLE players ADD COLUMN PER REAL')
	conn.commit()

	# Then let's calculate PER for each player and update the database
	for name, value in aPERdict.items():
		PER = value * (15 / laPER)
		c.execute('UPDATE players SET PER=? WHERE name=?;', (PER, name))
		conn.commit()
		print("Updated PER for {}".format(name))

	conn.close()
	print("Done!")


	#  ----------- The version below was changed on 30.05.2016 ----------------

	# # First we need to create an aPER dictionary

	# aPERdict = {}
	
	# for key, value in p_t.items():
	# 	player = PERCalculator(key, value)
	# 	CalculatePERs(player)
	# 	print("Calculated aPER for {} which is {}".format(player.name, player.aPER))
	# 	aPERdict[player.name] = player.aPER
	
	# # Then let's calculate the average league aPER

	# def laPERcalc(dictionary):
	# 	values = dictionary.values()
	# 	return reduce(lambda x, y: x+y, values)/len(values)

	# laPER = laPERcalc(aPERdict)

	# # Finally, let's put up the PER!

	# PERdict = {}

	# for key, value in aPERdict.items():
	# 	PERdict[key] = value * (15 / laPER)

	# # Then write to file

	# with open('PER.txt', 'w') as f:
	# 	for key, value in PERdict.items():
	# 		f.write('{},{} \n'.format(key, value))

	# print("Done!")

def player_team(soup):

	player_team = {}

	players = soup("td", class_="zawodnik")
	teams = soup("td", class_="druzyna2")

	for i in range(len(players)):
		a = players[i].find("strong").string
		b = teams[i].find("a").string
		player_team[a] = b

	return player_team

def CalculatePERs(player):

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
	main()# We can also close the connection if we are done with it.
