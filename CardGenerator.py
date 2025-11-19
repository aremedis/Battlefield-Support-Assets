from tempfile import tempdir

from PIL import Image, ImageDraw, ImageFont
import requests, csv, json, shutil, os, re, textwrap


#SPREADSHEET_ID = "1Jaap6i1qZYRc0teWCWSnlhN34XVutBTg8gL__TuXefI"

#test spreadsheet
SPREADSHEET_ID = "1hXHWGjTCoqOLVbnWopZSgtz-Peo3BRwmZUGQzBsE8mU"
sheet_address=f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&id={SPREADSHEET_ID}&gid=0"

SheetName = "BSAs"


response = requests.get(sheet_address)

if response.status_code == 200:
    print("gotit")
else:
    print(f"Error: {response.status_code}")


open('BSP.csv', 'wb').write(response.content)

csv_file_path = 'BSP.csv'
json_file_path = 'BSP.json'

PrinterFriendlyBackground=(255,255,255)
DarkGrey = (25,25,25)
Background = PrinterFriendlyBackground
YellowText = (95,74,27)
LightYellowText = (97,95,63)
BlackText = (0,0,0)
WhiteText = (255,255,255)
LightGrey = (69,73,74)
font_path = "Assets/SairaStencilOne-Regular.ttf"

CardWidth = 3.5
CardHeight = 2.5

CostPosition = (45,35)
NamePosition = (630, 90)
VariantPosition = (630, 115)
mpPos = (472,180)
tmmPos = (440,226)
RangePos = (33,299)
SkillPos = (206,299)
DMGPos = (360,299)
CheckPos = (490,299)
SpecialsPos = (29, 400)
MPpos = (572, 180)
TMMpos = (572, 226)
wtRangePos = (33,342)
wtSkillPos = (206, 342)
wtDMGPos = (360, 342)
wtCheckPos = (490, 342)
wtSpecialPos = (194 ,400)

#Aerospace Card locations
AeroSkillPos = RangePos
AeroDMGPos = SkillPos
AeroCheckPos = DMGPos
AerowtSkillPos = wtRangePos
AerowtDMGPos = wtSkillPos
AerowtCheckPos = wtDMGPos

AeroThrPos = mpPos
AeroFuelPos = tmmPos

def split_name_and_variant(name):
    delimiter = "("
    parts = name.split(delimiter, 1)
    # print(parts)
    return parts

def sanitize_name_text(text):
    #pattern = r'[^a-zA-Z0-9/s]'
    #cleaned_txt = re.sub(pattern, '', text)
    cleaned_txt = text.replace("/", "")
    return cleaned_txt

def convert_to_json(csv_file_path, json_file_path):
    data = []
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            data.append(row)

    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)


def ImageDimensions(width_inches, height_inches):
    dpi = 200
    width_pixels = int(width_inches * dpi)
    height_pixels = int(height_inches * dpi)
    # print(width_pixels, height_pixels)
    return (width_pixels, height_pixels)
#
# def AddBorder(image):
#     border_size = ""
#     border_color = YellowText
#     img = Image.open(image)
#     bordered_img = ImageOps.expand(image,border=border_size,fill=border_color)


# Image.new('RGB', (682,474), color = Background).save('img.jpg')
# Image.new('RGB', (682,474), color = YellowText).save('Yellow.jpg')
# Image.new('RGB', (682,474), color = LightGrey).save('lgrey.jpg')
def AddSpecialsText (text, font_size, color, position, draw, anchor):
    font = ImageFont.truetype(font_path, font_size)
    if (len(text) > 48):
        font = ImageFont.truetype(font_path, font_size - 3)
        templist = list(position)
        templist[1] -= 30
        position = tuple(templist)
        text = textwrap.fill(text, width=48)
        draw.multiline_text(position, text, font=font, fill=color, spacing=6)
    else:
        draw.text(position, text, fill=color, font=font, anchor=anchor)

def AddText(text, font_size, color, position, draw, anchor):
    font = ImageFont.truetype(font_path, font_size)
    draw.text(position, text, fill=color, font=font, anchor=anchor)

def ThresholdBox(draw):
    shape = [(538,302), (628,348)]
    draw.rectangle(shape, fill=(100,100,100))

def FuelBox(draw, fuel):
    BoxesPerRow = 4
    margin = 2
    initX = 490
    initY = 299
    current_x = initX
    current_y = initY
    boxSize = 10
    for i in (range(8)):
        x0 = current_x
        y0 = current_y
        x1 = current_x + boxSize
        y1 = current_y + boxSize

        draw.rectangle([(x0,y0), (x1, y1)], outline = 'black')

        if (i+1) % BoxesPerRow == 0:
            current_x = initX 
            current_y += boxSize + margin
        else: 
            current_x += boxSize + margin
        
def CreateAeroCard(cost, name, variant, fuel, skill, damage, check, threshold, specials, thrust, dimensions):
    image_path = "cards/"+name+variant+".jpg"
    Image.new('RGB', dimensions, color = Background).save(image_path)
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    anchor = 'lb'
    AddText("SKILL", 34, YellowText, AeroSkillPos, draw, anchor)
    AddText("DMG", 34, YellowText, AeroDMGPos, draw, anchor)
    AddText("CHECK", 34, YellowText, AeroCheckPos, draw, anchor)
    AddText("SPECIALS:", 28, YellowText,SpecialsPos, draw, anchor)
    AddText("THR", 34, YellowText, AeroThrPos, draw, anchor)
    AddText("Fuel", 34, YellowText, AeroFuelPos, draw, anchor)
    img.save(image_path)
    img.show()

def CreateCard(cost, name, variant, mp, tmm, range, skill, damage, check, threshold, specials, dimensions):
    image_path = "cards/"+name+variant+".jpg"
    Image.new('RGB', dimensions, color = Background).save(image_path)
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    anchor = 'lb'
    #Write Header Templates:
    AddText("RANGE", 34, YellowText, RangePos, draw, anchor)
    AddText("SKILL", 34, YellowText, SkillPos, draw, anchor)
    AddText("DMG", 34, YellowText, DMGPos, draw, anchor)
    AddText("CHECK", 34, YellowText, CheckPos, draw, anchor)
    AddText("MP:", 40, YellowText, mpPos, draw, anchor)
    AddText("TMM:", 40, YellowText, tmmPos, draw, anchor)
    AddText("SPECIALS:", 28, YellowText,SpecialsPos, draw, anchor)
    # Write Cost to card:

    AddText(cost, 34, YellowText, CostPosition, draw, anchor)

    # Write Asset Name to Card:
    AddText(name, 34, YellowText, NamePosition, draw, 'rb')
    # Write Variant to Card:
    AddText(variant, 24, LightGrey, VariantPosition, draw, 'rb')
    # Write MP to card
    AddText(mp, 40, LightYellowText, MPpos, draw, anchor)
    # Write TMM to card
    AddText(tmm, 40, LightYellowText, TMMpos, draw, anchor)
    # White Text
    # Range
    color = BlackText
    AddText(range, 34, color, wtRangePos, draw, anchor)
    # Skill
    AddText(skill, 34, color, wtSkillPos, draw, anchor)
    # damage
    AddText(damage, 34, color, wtDMGPos, draw, anchor)
    # check
    AddText(check, 34, color, wtCheckPos, draw, anchor)
    # threshold
    AddText(threshold, 20, color, (607,370), draw, anchor)
    # specials
    AddSpecialsText(specials, 20, color, wtSpecialPos, draw, anchor)
    ThresholdBox(draw)






    img.save(image_path)
#   img.show()

convert_to_json(csv_file_path, json_file_path)
os.makedirs('cards', exist_ok=True)

with open('BSP.json', 'r') as file:
    data = json.load(file)

# print(data)
# print(data[1]['Name'])
# print(data[len(data)-1])

for i in range(len(data)-1):
#     entry = data[i]
#     cost = entry['Cost']
#     name = entry['Name']
#     skill = entry['Skill']
#     mp = entry['MP']
#     tmm = entry['TMM']
#     range = entry['Range']
#     damage = entry['Damage']
#     check = entry['Check']
#     threshold = entry['Thresh']
#     specials = entry['Special']

    variant=""
    entry = data[i]
    name = sanitize_name_text(str(entry['Name']))
    if "(" in name:
        tempname = split_name_and_variant(name)
        name = tempname[0]
        variant = "("+tempname[1]
    # print(name)
    #Remove abbreviation for Conventional Infantry
    if (name == "CI "):
        name = "Conventional Infantry "
    # Begin Card Creation
    print(entry['Fuel'])
    print(name)
    if (str(entry['Fuel']) != ""):
        CreateAeroCard(
            str(entry['Cost']),
            name,
            variant,
            str(entry['Fuel']),
            str(entry['Skill']),
            str(entry['Damage']),
            str(entry['Check']),
            str(entry['Thresh']),
            str(entry['Special']),
            str(entry['Thrust']),
            ImageDimensions(CardWidth,CardHeight)
            )
    else:    
        CreateCard(
        str(entry['Cost']),
        name,
        variant,
        str(entry['MP']),
        str(entry['TMM']),
        str(entry['Range']),
        str(entry['Skill']),
        str(entry['Damage']),
        str(entry['Check']),
        str(entry['Thresh']),
        str(entry['Special']),
        ImageDimensions(CardWidth,CardHeight))



#CreateCard("58", "LRM Carrier", "Arrow IV Carrier", "3t", "+1", "Arrow", "6", "--", "7", "5", "Arrow2" )


######
# Create .zip archive from 'cards/' directory
######
shutil.make_archive('BSP_Cards','zip', 'cards')
print(f"Successfully created ZIP file")