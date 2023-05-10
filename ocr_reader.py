from PIL import Image                       #potrebne pro OCR
import pytesseract                          #prace s tesseract enginem
from pdf2image import convert_from_path     #prevod pdf na obrazek
import os                                   #prace se soubory, adresari, ...
import re
import text_reader

"""
Vytvoreni slozky pro prevod PDF souboru na obrazky pro pozdejsim zpracovani tesseract enginem
"""
ocrTempPath = "./ocr_temp"
dirExists = os.path.exists(ocrTempPath)
if not dirExists:
    try:
        original_umask = os.umask(0)
        os.makedirs(ocrTempPath, mode=0o777)
    finally:
        os.umask(original_umask)

def returnIcoOcr(ocr, file):
    """
    Totez co returnIcoPdf, jen mirne zmeny
    """
    matchList = text_reader.checkDuplicate(re.findall(r"(?<!\S)\d{8}\b(?!\S)|(?<!\S)\d{8}\b(?![^;,])", ocr))
    icoList = [file]

    for ico in matchList:
        if text_reader.testICO(ico):
            icoList.append(ico)

    return(icoList)

"""
Prevod PDF na obrazek/ky, prevedeni obrazku do textu pomoci OCR tesseract
"""
def returnInvoiceOcr(file):
    images = convert_from_path(file)

    for i in range(len(images)):
        images[i].save(f"{ocrTempPath}/ocr_strana{str(i)}.jpg", "JPEG")

    ocrPrevod = pytesseract.image_to_string(Image.open(ocrTempPath + "/ocr_strana0.jpg")) #zpracovava se jen prvni stranka prevedeneho dokumentu
    return(ocrPrevod)