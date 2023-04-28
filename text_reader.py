import pdftotext
import re
import os
import pandas
import ocr_reader

directory = "./pdf/"
files = []

for file in os.listdir(directory):
    files.append(file)

def testICO(input: str):
    #Zkontroluje jestli je cislo validni ICO
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
    #Zkontroluje jestli se cislo ktere bylo vyhodnocene jako ICO nevyskytuje v dokumentu dvakrat (prevedenim do SETu)
    uniqueSet = set(input)
    return(uniqueSet)

neprecteneSoubory = []

def returnIco(pdf):
    matchList = checkDuplicate(re.findall(r"(?<!\S)\d{8}\b(?!\S)|(?<!\S)\d{8}\b(?![^;,])", pdf[0]))
    icoList = [file] 

    for ico in matchList:
        if testICO(ico):
            icoList.append(ico)

    return(icoList)

fileObjects = []
chybneSoubory = []

#pokusi se kazdy soubor prevest na text, ziskat cisla ktera by mohli byt ico, zkontroluje jestli nejsou duplikatni cisla, zkontroluje
#jestli je cislo validni ico a vrati seznam ve formatu nazev souboru: ico1, ico2, icoN, ...
#
#chybne soubory ulozi do samstatného seznamu
for file in files:
    with open(directory+file, "rb") as f:
        try:
            pdf = pdftotext.PDF(f)
            ico = returnIco(pdf)
            if len(ico) == 1:
                neprecteneSoubory.append(file)#kdyz nebylo ze souboru vyctene zadne ico, tak tak se prida do seznamu neprectenesoubory a pozdeji se s nim pracuje pomocí ocr
            else:
                fileObjects.append(ico)
        except pdftotext.Error:
            soubor = file
            chyba = "Chyba"
            chybneSoubory.append(file)
            fileObjects.append([file, chyba])

#zpracovavani ocr souboru
for soubor in neprecteneSoubory:
    prevod = ocr_reader.returnInvoiceOcr(directory+soubor)
    returnIco(prevod)


#potom smazat
#for zaznam in fileObjects:
#    print(zaznam)

for soubor in neprecteneSoubory:
    print(soubor)

#Uložení do CSV
table = pandas.DataFrame(fileObjects)
table.to_csv("out.csv")