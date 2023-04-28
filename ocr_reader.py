from PIL import Image
import pytesseract
from pdf2image import convert_from_path

#images = convert_from_path("ocr_test.pdf")

#for i in range(len(images)):
#    images[i].save("page" + str(i) + ".jpg", "JPEG")

#print(pytesseract.image_to_string(Image.open('page0.jpg')))

def returnInvoiceOcr(file):
    images = convert_from_path(file)

    for i in range(len(images)):
        images[i].save(f"ocrPrevodStrana{str(i)}.jpg", "JPEG")

    ocrPrevod = pytesseract.image_to_string(Image.open("ocrPrevodStrana0.jpg")) #dodelat kdyz bude vice stranek nez jen jedna
    return(ocrPrevod)