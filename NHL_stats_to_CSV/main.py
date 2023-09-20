import csv
import requests
from urllib.parse import urljoin

# Public API for pulling back NHL Data
# Team standings for the 2021-2022 season https://statsapi.web.nhl.com/api/v1/standings?season=20212022

baseUrl = "https://statsapi.web.nhl.com"
standingsEndpoint = "/api/v1/standings"
queryParams = {"season": 20212022, "expand": "standings.record"}

request = requests.models.PreparedRequest()
request.prepare_url(url=urljoin(baseUrl,standingsEndpoint), params=queryParams)

print('REQUEST url:', request.url)
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}
print('REQUEST Headers: ', headers)

response = requests.request("GET", url=request.url, headers=headers,data={})
results = response.json()
print('REQUEST status:', response.status_code)

# CSV Table data
csvHeaders = ['YEAR', 'DIVISION', 'TEAM NAME', 'POINTS', 'WINS', 'LOSSES', 'OT']
teamsData = []

# Extract Data from response JSON
for record in results['records']:
    for teamRecord in record[tuple(filter(lambda i: (i == 'teamRecords'), record))[0]]:
        year = '2021-2022'
        division = record['division']['name']
        teamName = teamRecord['team']['name']
        points = teamRecord['points']
        wins = teamRecord['leagueRecord']['wins']
        losses = teamRecord['leagueRecord']['losses']
        ot =  teamRecord['leagueRecord']['ot']
        teamsData.append([year, division, teamName, points, wins, losses, ot])

# Write to CSV File
with open('NHL Stats 2021-2022.csv', 'w', encoding='UTF8', newline='') as f:
    print('Writing to CSV...')
    writer = csv.writer(f)

    writer.writerow(csvHeaders)
    writer.writerows(teamsData)
    print('Done Writing to CSV..')

print('Done')