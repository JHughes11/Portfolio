import csv

# Write to CSV File
def writeToCSV(**kwargs):    
    title = kwargs['title']
    headers = kwargs['headers']
    rows = kwargs['rows']
    with open("./csv/" + title, 'w', encoding='UTF8', newline='') as f:
        print('Writing to CSV...')
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print('Done Writing to CSV..')