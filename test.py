import cv2
import pytesseract
import fitz
import os
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

png_link = 'test/images/breakingNews.png'
pdf_link = 'test/pdfs/breakingNews.pdf'

# print png
img = cv2.imread(png_link)
text = pytesseract.image_to_string(img)
print(text)

# print pdf
doc = fitz.open(pdf_link)
output_images = []
print("length of doc {}".format(len(doc)))
for page in range(len(doc)):
    for img in doc.getPageImageList(page):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        temp_png_link = 'test_png_outputs/p%s-%s.png' % (page, xref)
        if pix.n < 5:       # this is GRAY or RGB
            pix.writePNG(temp_png_link)
        else:               # CMYK: convert to RGB first
            pix1 = fitz.Pixmap(fitz.csRGB, pix)
            pix1.writePNG(temp_png_link)
            pix1 = None
        pix = None
        output_images.append(temp_png_link)
        img = cv2.imread(temp_png_link)
        text = pytesseract.image_to_string(img)
        print(text)

for img in output_images:
    os.remove(img)
