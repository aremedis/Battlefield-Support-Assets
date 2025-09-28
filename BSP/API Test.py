import requests, csv, json


SPREADSHEET_ID = "1Jaap6i1qZYRc0teWCWSnlhN34XVutBTg8gL__TuXefI"
sheet_address=f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&id={SPREADSHEET_ID}&gid=0"

SheetName = "BSAs"


response = requests.get(sheet_address)

if response.status_code == 200:
    print("gotit")
else:
    print(f"Error: {response.status_code}")


open('BSP.csv', 'wb').write(response.content)

# Convert csv to json
def convert_to_json(csv_file_path, json_file_path):
    data = []
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            data.append(row)

    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)

csv_file_path = 'BSP.csv'
json_file_path = 'BSP.json'

convert_to_json(csv_file_path, json_file_path)



with open('BSP.json', 'r') as file:
    data = json.load(file)

#$data = open('BSP.json', 'r')
# entries = data["values"]
print (data[0]['Name'])
print(len(data))
# data[x]['Name']
# data[x]['Cost']
# data[x]['Skill']
# data[x]['MP']
# data[x]['TMM']
# data[x]['Range']
# data[x]['Damage']
# data[x]['Check']
# data[x]['Thresh']
# data[x]['Special']



