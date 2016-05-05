#Local
from algorithms import PERCalculator
#Packages
from bs4 import BeautifulSoup
import requests
from functools import reduce
import re

# Capturing AJAX and parsing

def teamparse(headers, sibl_end, team=False):
	
	# Help function
	# Search for next sibling, i.e. column until the specified number (determined by the sibl_end parameter)
	def find_column(element):
		count = 0
		while count < sibl_end:
			element = element.next_sibling
			count += 1
		return element.string

	headers['X-Requested-With'] = 'XMLHttpRequest'
	r = requests.post('http://plk.pl/statystyki/xml/1.html', headers=headers)
	print(r.status_code)
	soup = BeautifulSoup(r.text, "lxml")
	
	# Find teams' rows
	rows = soup("td", class_="druzyna")

	# If the team parameter is specified - return team stats. If not, return League stats
	if team:
	# Find the team's row
		for ind, row in enumerate(rows):
			a = row.find("strong")
			print(a)
			if team in a.string:
				break
		return find_column(rows[ind])
	else:
		results = []
		for row in rows:
			results.append(find_column(row))
		#print(results) # Just for testing
		average = reduce(lambda x, y: float(x)+float(y), results)/(len(results)+1)
		return round(average,2)


# Calculating the league stats

lpoints = teamparse({ 'f':0, 's':18, 'o':'Pkt', 'wh':'g0', 'r':'0', 'nocontent':1}, 4)
lfieldgoals = teamparse({ 'f':0, 's':18, 'o':'Pkt', 'wh':'g0', 'r':'0', 'nocontent':1}, 6)
lafieldgoals = teamparse({ 'f':0, 's':18, 'o':'Pkt', 'wh':'g0', 'r':'0', 'nocontent':1}, 8)
lfreethrows = teamparse({ 'f':0, 's':18, 'o':'Pkt', 'wh':'g0', 'r':'0', 'nocontent':1}, 24)
lafreethrows = teamparse({ 'f':0, 's':18, 'o':'Pkt', 'wh':'g0', 'r':'0', 'nocontent':1}, 26)
lorebounds = teamparse({ 'f':0, 's':18, 'o':'Pkt', 'wh':'g0', 'r':'0', 'nocontent':1}, 30)
ltrebounds = teamparse({ 'f':0, 's':18, 'o':'Pkt', 'wh':'g0', 'r':'0', 'nocontent':1}, 34)
lassists = teamparse({ 'f':0, 's':18, 'o':'Pkt', 'wh':'g0', 'r':'0', 'nocontent':1}, 36)
lpfouls = teamparse({ 'f':0, 's':18, 'o':'Pkt', 'wh':'g0', 'r':'0', 'nocontent':1}, 38)
lturnovers = teamparse({ 'f':0, 's':18, 'o':'Pkt', 'wh':'g0', 'r':'0', 'nocontent':1}, 42)

# Initiate a new PERCalculator for a player

player = PERCalculator("Mateusz", "Trybulec")
player.tassists = teamparse({ 'f':0, 's':18, 'o':'Pkt', 'wh':'g0', 'r':'0', 'nocontent':1}, 36)
