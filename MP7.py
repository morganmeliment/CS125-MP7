import csv
import requests
from math import sin, cos, sqrt, atan2, radians
 
#ifile = open('Voters Table.csv', 'r', encoding = 'utf-16')
ifile = open('Voted-in-2017-Local-Elections-Democrats.csv', 'r', encoding = 'utf-8')
reader = csv.reader(ifile)

dicty = {"lat": [], "lon": [], "closer": []}
listy = []

address1 = "1012 W. Illinois St., Urbana, IL"#input("What is the first address? ")
address2 = "4011 Schiller Pl, Saint Louis, MO"#input("What is the second address? ") 

d1 = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + address1.replace(" ", "+") + "&key=AIzaSyBYVyJa27GSQfdDWLIMYuBHwZBZxILWxfw")
d2 = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + address2.replace(" ", "+") + "&key=AIzaSyBYVyJa27GSQfdDWLIMYuBHwZBZxILWxfw")

lat1 = d1.json()['results'][0]['geometry']['location']['lat']
lat2 = d2.json()['results'][0]['geometry']['location']['lat']
lon1 = d1.json()['results'][0]['geometry']['location']['lng']
lon2 = d2.json()['results'][0]['geometry']['location']['lng']

# Radius of the earth.
R = 6373.0

lat1 = radians(lat1)
lon1 = radians(lon1)
lat2 = radians(lat2)
lon2 = radians(lon2)

#print(lat1, lon1, lat2, lon2)

def getDistance(la1, la2, lo1, lo2):
	dla = la2 - la1
	dlo = lo2 - lo1
	a = sin(dla / 2) ** 2 + cos(la1) * cos(la2) * sin(dlo / 2) ** 2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	return R * c

def getCloser(la, lo):
	dist1 = getDistance(lat1, la, lon1, lo)
	#print(la, lo, dist1)
	dist2 = getDistance(lat2, la, lon2, lo)
	#print(la, lo, dist2)
	if abs(dist1) < abs(dist2):
		return 1
	return 2

rownum = 0
for row in reader:
	# Save header row.
	if rownum == 0:
		for col in row:
			dicty[col] = []
			listy.append(col)
			#print(col, end = " ")
	else:
		ii = 0
		add = ""
		lat = 0
		lon = 0
		for col in row:
			if col:
				#print(col, ii)
				if ii == 18:
					add = add + col.replace(" ", "+") + ",+"
					#data = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + col.replace(" ", "+") + "&key=AIzaSyBYVyJa27GSQfdDWLIMYuBHwZBZxILWxfw")
					#print("https://maps.googleapis.com/maps/api/geocode/json?address=" + col.replace(" ", "+") + "&key=AIzaSyBYVyJa27GSQfdDWLIMYuBHwZBZxILWxfw")
				elif ii == 19:
					add = add + col.replace(" ", "+") + ",+"
				elif ii == 20:
					add = add + col.replace(" ", "+")
				elif ii == 21:
					data = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + add + "&key=AIzaSyBYVyJa27GSQfdDWLIMYuBHwZBZxILWxfw")
					lat = data.json()['results'][0]['geometry']['location']['lat']
					lon = data.json()['results'][0]['geometry']['location']['lng']
				dicty[listy[ii]].append(col)
			else:
				dicty[listy[ii]].append(0)
			ii += 1
		dicty["lat"].append(radians(lat))
		dicty["lon"].append(radians(lon))
		dicty["closer"].append(getCloser(radians(lat), radians(lon)))

	rownum += 1
	if rownum >= 25:
		break

ifile.close()

print("")
print('Voters closer to "' + address1 + '":')
print("")

io = 0
for ui in dicty["FirstName"]:
	last = dicty["LastName"][io]
	if dicty["closer"][io] == 1:
		print("    " + ui + " " + last + ', Address: "' + dicty["VoteAddress"][io] + ', ' + dicty["VoteCity"][io] + ', ' + dicty["VoteState"][io] + '"')
	io += 1

print("")
print('Voters closer to "' + address2 + '":')
print("")

io = 0
for ui in dicty["FirstName"]:
	last = dicty["LastName"][io]
	if dicty["closer"][io] == 2:
		print("    " + ui + " " + last + ', Address: "' + dicty["VoteAddress"][io] + ', ' + dicty["VoteCity"][io] + ', ' + dicty["VoteState"][io] + '"')
	io += 1

print("")










