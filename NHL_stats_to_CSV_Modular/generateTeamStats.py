# Generate the rows 
def generateTeamStats(results, year):
    print('Generating Team Stats for the years: ', year)
    data = []
    # Extract Data from response JSON
    for record in results['records']:
        for teamRecord in record[tuple(filter(lambda i: (i == 'teamRecords'), record))[0]]:
            division = record['division']['name']
            teamName = teamRecord['team']['name']
            points = teamRecord['points']
            wins = teamRecord['leagueRecord']['wins']
            losses = teamRecord['leagueRecord']['losses']
            ot =  teamRecord['leagueRecord']['ot']
            data.append([year, division, teamName, points, wins, losses, ot])
    
    return data
