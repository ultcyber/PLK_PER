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
	
	#print(results) <--- Just for testing
	
	# For each row, calculate the appropriate next sibling (determined by the sibl_end parameter)
	for element in rows:
		count = 0
		while count < sibl_end:
			element = element.next_sibling
			count += 1
		results.append(element.string)

	average = reduce(lambda x, y: float(x)+float(y), results)/(len(results)+1)
	return round(average,2)

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