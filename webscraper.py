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
			#print(a) # Just for testing
			if team in a.string:
				break
		return float(find_column(trows[ind]))
	elif name:
		for ind, row in enumerate(prows):
			a = row.find("strong")
			#print(a) # Just for testing
			if name in a.string:
				break
		try:	# minutes are given in mmm:sss format, so gotta check for that, f%#$ annoying
			return float(find_column(prows[ind]))
		except ValueError:
			mo = re.search('(\d+):(\d+)', find_column(prows[ind]))
			return float( float(mo.group(1)) + (float(mo.group(2))/60) )
	else:
		results = []
		for row in trows:
			results.append(find_column(row))
		#print(results) # Just for testing
		average = reduce(lambda x, y: float(x)+float(y), results)/(len(results)+1)
		return round(average,2)

# Unfortunately need to make a very similar function, but for opponent stats
def opponent_parse(soup, sibl_end, team):

	# Help function
	# Search for next sibling, i.e. column until the specified number (determined by the sibl_end parameter)
	def find_column(element):
		count = 0
		while count < sibl_end:
			element = element.next_sibling
			count += 1
		return element.string
	
	trows = soup("td", class_="druzyna")

	results = []
	for ind, row in enumerate(trows):
		a = row.find("strong")
		#print(a) # Just for testing
		if team in a.string:
			continue
		else: 
			results.append(find_column(row))
	#print(results) # Just for testing
	average = reduce(lambda x, y: float(x)+float(y), results)/(len(results)+1)
	return round(average,2)	




