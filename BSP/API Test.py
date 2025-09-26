import os
import requests

SPREADSHEET_ID =  os.environ['SPREADSHEET_ID']
API_KEY = os.environ['API_KEY']

SheetName = "BSAs"

sheet_address = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{SheetName}?key={API_KEY}"


response = requests.get(sheet_address)

if response.status_code == 200:
    print("gotit")
else:
    print(f"Error: {response.status_code}")

data = response.json()
entries = data["values"]
# print (data["values"])

column_header = data["values"][0]
print (column_header)
for row in range(1, len(entries)):
    # print (entries[row])
    BSP_NAME = entries[row][0]
    BSP_COST = entries[row][1]
    BSP_SKILL = entries[row][2]
    BSP_MOVE = entries[row][3]
    BSP_TMM = entries[row][4]
    BSP_RANGE = entries[row][5]
    BSP_DMG = entries[row][6]
    BSP_THRESH = entries[row][7]
    BSP_SPECIAL = entries[row][8]


# data["values"][x][0] == "Name"
# data["values"][x][1] == "Cost"
# data["values"][x][2] == "Skill"
# data["values"][x][3] == "MovementPoints"
# data["values"][x][4] == "TMM"
# data["values"][x][5] == "Range"
# data["values"][x][6] == "Damage"
# data["values"][x][7] == "Threshold"
# data["values"][x][8] == "Special"
