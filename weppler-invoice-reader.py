import pdftotext
import re

with open("vzorek18.pdf", "rb") as f:
    pdf = pdftotext.PDF(f)

def testICO(input: str):
    #Zkontroluje jestli je ICO validni
    chars = list(input)
    soucet = 0

    for i in range(7):
        soucet += int(chars[i]) * (8 - i)

    zbytek = soucet % 11
        
    if zbytek == 0:
        posledni_cislo = 1
    elif zbytek == 1:
        posledni_cislo = 0
    else:
        posledni_cislo = 11 - zbytek

    return(int(chars[7]) == posledni_cislo)

def checkDuplicate(input: list):
    uniqueSet = set(input)
    return(uniqueSet)

matchList = checkDuplicate(re.findall(r"(?<!\S)\d{8}\b(?!\S)|(?<!\S)\d{8}\b(?![^;,])", pdf[0]))

for ico in matchList:
    if testICO(ico):
        print(ico)

