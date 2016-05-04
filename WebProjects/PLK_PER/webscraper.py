#Local
from algorithms import PERCalculator
#Packages
from bs4 import BeautifulSoup
import requests
from functools import reduce

# Initiate a new PERCalculator for a player
player = PERCalculator("Mateusz", "Trybulec")

# Define the league stats

# Team stats AJAX capture

def teamparse(headers, sibl_end):
	
	headers['X-Requested-With'] = 'XMLHttpRequest'
	r = requests.post('http://plk.pl/statystyki/xml/1.html', headers=headers)
	print(r.status_code)
	soup = BeautifulSoup(r.text, "lxml")
	
	# Find teams' rows
	rows = soup("td", class_="druzyna")
	
	# Create an array for the results
	results = []

	# For each row, calculate the appropriate next sibling (determined by the sibl_end parameter)
	for element in rows:
		count = 0
		while count < sibl_end:
			element = element.next_sibling
			count += 1
		results.append(element.string)

	average = reduce(lambda x, y: float(x)+float(y), results)/(len(results)+1)
	return round(average,2)


lfieldgoals = teamparse({ 'f':0, 's':18, 'o':'Pkt', 'wh':'g0', 'r':'0', 'nocontent':1}, 4)


# lassists
# ltrebounds
# lorebounds
# lafieldgoals
# lafreethrows
# lfreethrows
# lpfouls
# lafthrows
# lpoints
# lturnovers