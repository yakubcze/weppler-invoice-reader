
# Invoice Reader

- napsáno v Python 3.10.6
- vytvořeno a otestováno v prostředí OS Linux Ubuntu 22.04 LTS (WSL2)

## Účel skriptu

Skript vytvořený pro hledání IČO čísel z velkého množství faktur v PDF formátu. Export do CSV souboru viz. níže. 

- první sloupec: pořadové číslo 
- druhý sloupec: 1 = převod proveden pomocí OCR, 0 = převod proveden z textové podoby
- třetí sloupec: název souboru
- čtvrtý až n-tý sloupec: IČO

![screenshot](/invoice_reader_print_screen.png)



## Instalace a spouštění



Vytvoření virtuálního prostředí Python a přepnutí do něj:

        user@pc:~$ python -m venv venv
        user@pc:~$ source venv/bin/activate

Instalace Tesseract enginu pro převod naskenovaných faktur:

        user@pc:~$ sudo apt install tesseract-ocr

Instalace závislostí:

        user@pc:~$ pip install -r requirements.txt

Spouštění:

        user@pc:~$ python invoice-reader.py

## Funkce skriptu

Skript po spuštění zobrazí výzvu pro zadání adresáře, kde se nachází PDF soubory (nemusí mít koncovku .pdf). Po zadání adresáře projde všechny soubory po jednom a získá z nich čísla IČO. Pokud je PDF soubor v textovém formátu (tzn. jde manipulovat přímo s textem), převede PDF soubor do textu pomocí knihovny *pdftotext*. Pokud je PDF soubor v obrázkovém formátu (tzn. naskenovaný) převede soubor do textu pomocí OCR enginu *tesseract* a knihovny *pytesseract*.

Ze samotného textu jsou poté získána čísla pomocí regulárního výrazu, která formátem odpovídají IČO číslu. Ověřením validity pomocí propočtu (https://overeni-ico.peckapc.cz/, https://phpfashion.com/jak-overit-platne-ic-a-rodne-cislo) a odstraněním duplicitních čísel je provedeno zpřesnění výsledků. I přes to, ale u některých souborů skript najde více než dvě IČO čísla a je nutné výsledky manuálně zkontrolovat. Rovněž se (zřídka) stává že někdy skript najde pouze jedno či žádné IČO, i přes to, že se v dokumentu tyto mohou vyskytovat.