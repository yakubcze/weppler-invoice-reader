import re   #regexy

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

def returnIcoPdf(pdf, file):
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



