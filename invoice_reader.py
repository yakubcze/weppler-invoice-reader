import pdftotext    #prevod pdf na text
import pandas       #export do csv
import ocr_reader   #druhy soubor s funkcemi souvisejicimi s OCR
import tqdm         #progress bar
import os           #prace se soubory, adresari, ...
import sys          #pro ukonceni programu
import text_reader  #dalsi soubor v adresari
import ocr_reader   #dalsi soubor v adresari

directory = input("Zadej cestu ke složce se soubory (např.: /home/user/pdf/ nebo ./pdf/): ")

files = []
try:
    for file in os.listdir(directory):
        files.append(file)
except FileNotFoundError as e:
    print("Špatně zadaný adresář!")
    sys.exit(1)

"""
Hlavni smycka pro zpracovani souboru
Pokusi se kazdy soubor ve slozce prevest na text, ziskat cisla ktera odpovidaji formatu pro ICO a vytvorit zaznam ve formatu:
0/1     <nazev_souboru>     <ico1>  <ico2>  <icoN>
kde 0/1 je priznak zda byli hodnoty ziskany pomoci bezneho prevodu PDF na txt (=0), nebo pomoci OCR (=1)

pokud se nepodarilo soubor otevrit, prida se zaznam ve formatu:
0       <nazev_souboru>     chyba
coz znamena ze soubor PDF nejde otevrit (pravdepodobne ZIP, PNG, JPG, ... soubory)
"""
fileObjects = []
chybneSoubory = []

progress_bar = tqdm.tqdm(total=len(files))#progress bar na terminal, 0 - pocet souboru v adresari
for file in files:
    with open(directory+file, "rb") as f:
        try:
            pdf = pdftotext.PDF(f)
            icoPdf = text_reader.returnIcoPdf(pdf, file)
            if len(icoPdf) > 1:
                pomList = [0] + icoPdf
                fileObjects.append(pomList)
            else:
                prevod = ocr_reader.returnInvoiceOcr(directory+file)
                ico = ocr_reader.returnIcoOcr(prevod, file)
                pomList = [1] + ico
                fileObjects.append(pomList)
        except pdftotext.Error: #chybne soubory ktere nejde otevrit (prilohy, apod...)
            chyba = "Chyba"
            chybneSoubory.append(file)
            fileObjects.append([0, file, chyba])
    progress_bar.update()

progress_bar.close()#restart progress baru

"""
Vytvoreni slozky pro export CSV souboru
"""
exportPath = "./export"
dirExists = os.path.exists(exportPath)
if not dirExists:
    try:
        original_umask = os.umask(0)
        os.makedirs(exportPath, mode=0o777)
    finally:
        os.umask(original_umask)

"""
Ulozi vsechny ziskane data do CSV souboru
"""
csv_file_name = directory.replace("/", "_")
table = pandas.DataFrame(fileObjects)
table.to_csv(f"{exportPath}/{csv_file_name}.csv")