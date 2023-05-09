import pdftotext    #prevod pdf na text
import re           #regexy
import os           #prace se soubory, adresari, ...
import pandas       #export do csv
import ocr_reader   #druhy soubor s funkcemi souvisejicimi s OCR
import tqdm         #progress bar

directory = "./pdf/"
files = []

for file in os.listdir(directory):
    files.append(file)

def testICO(input: str):
    """
    Kontrola jestli je ICO validni pomoci propoctu
    https://phpfashion.com/jak-overit-platne-ic-a-rodne-cislo
    https://overeni-ico.peckapc.cz/
    """

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
    """
    Kontrola jestli nebylo nalezeno vicekrat stejno ICO.
    Kontrola probiha prevedenim do python setu, ktery nepodporuje duplicitni hodnoty.
    """

    uniqueSet = set(input)
    return(uniqueSet)

def returnIcoPdf(pdf):
    """
    Vyfiltruje pomoci regexu ze ziskaneho textu vsechna cisla, ktera by svym formatem mohla byt povazovana za ICO ->
    pote odstrani duplicity pomoci funkce checkDuplicate -> pote zkontroluje zda je cislo validni ICO pomoci funkce testICO ->
    pokud ano, prida ho do seznamu icoList -> nakonec vrati list se vsemi nalezenymi ICO v souboru
    """
    matchList = checkDuplicate(re.findall(r"(?<!\S)\d{8}\b(?!\S)|(?<!\S)\d{8}\b(?![^;,])", pdf[0]))
    icoList = [file] 

    for ico in matchList:
        if testICO(ico):
            icoList.append(ico)

    return(icoList)

def returnIcoOcr(ocr):
    """
    Totez co returnIcoPdf, jen mirne zmeny
    """
    matchList = checkDuplicate(re.findall(r"(?<!\S)\d{8}\b(?!\S)|(?<!\S)\d{8}\b(?![^;,])", ocr))
    icoList = [file]

    for ico in matchList:
        if testICO(ico):
            icoList.append(ico)

    return(icoList)

fileObjects = []
chybneSoubory = []

progress_bar = tqdm.tqdm(total=len(files))#progress bar na terminal

"""
Pokusi se kazdy soubor ve slozce prevest na text, ziskat cisla ktera odpovidaji formatu pro ICO a vytvorit zaznam ve formatu:
0/1     <nazev_souboru>     <ico1>  <ico2>  <icoN>
kde 0/1 je priznak zda byli hodnoty ziskany pomoci bezneho prevodu PDF na txt (=0), nebo pomoci OCR (=1)

pokud se nepodarilo soubor otevrit, prida se zaznam ve formatu:
0       <nazev_souboru>     chyba
coz znamena ze soubor PDF nejde otevrit (pravdepodobne ZIP, PNG, JPG, ... soubory)
"""
for file in files:
    with open(directory+file, "rb") as f:
        try:
            pdf = pdftotext.PDF(f)
            icoPdf = returnIcoPdf(pdf)
            if len(icoPdf) > 1:
                pomList = [0] + icoPdf
                fileObjects.append(pomList)
            else:
                prevod = ocr_reader.returnInvoiceOcr(directory+file)
                ico = returnIcoOcr(prevod)
                pomList = [1] + ico
                fileObjects.append(pomList)
        except pdftotext.Error: #chybne soubory ktere nejde otevrit (prilohy, apod...)
            chyba = "Chyba"
            chybneSoubory.append(file)
            fileObjects.append([0, file, chyba])
    progress_bar.update()

progress_bar.close()#restart progress baru

"""
Ulozi vsechny ziskane data do CSV tabulky
"""
table = pandas.DataFrame(fileObjects)
table.to_csv("out.csv")