# https://towardsdatascience.com/read-text-from-image-with-one-line-of-python-code-c22ede074cac
# https://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python
# https://stackoverflow.com/questions/56467667/how-do-i-resolve-no-module-named-frontend-error-message
# https://www.geeksforgeeks.org/extract-text-from-pdf-file-using-python/
import sys
import cv2
import fitz
import PyPDF2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def found_str_in_png(str, png_link):
    img = cv2.imread(png_link)
    img_text = pytesseract.image_to_string(img)

    return img_text.find(str) >= 0

# Search Images
def search_images(search_str, pdf_link):
    all_image_links = []
    doc = fitz.open(pdf_link)
    for page in range(len(doc)):
        for img in doc.getPageImageList(page):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            # increment page number for 1-index readability
            page_idx = page + 1
            image_link = 'png_outputs/p%s-%s.png' % (page_idx, xref)
            if pix.n < 5:       # this is GRAY or RGB
                pix.writePNG(image_link)
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.writePNG(image_link)
                pix1 = None
            pix = None

            all_image_links.append((image_link, page_idx))

    found_str_images = []
    for (image, page) in all_image_links:
        if found_str_in_png(search_str, image):
            found_str_images.append((image, page))

    return found_str_images

# Search normal text in pdf
def search_text(search_str, pdf_link):
    pdf_file = open(pdf_link, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    num_pages = pdf_reader.numPages

    pages_with_text = []
    for page in range(num_pages):
        page_obj = pdf_reader.getPage(page)
        page_text = page_obj.extractText()
        if (page_text.find(search_str) >= 0):
            pages_with_text.append(page)

    return pages_with_text

def increment_list_eles(list):
    return [i+1 for i in list]

def take_inputs(args):
    print(args)
    if len(args) == 3:
        search_str = args[1]
        input_pdf = args[2]
    else:
        search_str = input("String to search for: ")
        input_pdf = input("PDF name: ")

    if not '.' in input_pdf:
        input_pdf += '.pdf'
    print(input_pdf)

    return search_str, input_pdf

# ------------------------------------------------------------------

search_str, input_pdf = take_inputs(sys.argv)
print("---------------------------------------------")
found_in_img_page = search_images(search_str, input_pdf)
found_in_txt_page = search_text(search_str, input_pdf)

# print which pages found in text
# increment values for readability
found_in_txt_page = increment_list_eles(found_in_txt_page)
print("Found on following pages in text")
print(found_in_txt_page)

print("---------------------------------------------")
# print which pages found in images
print("Found in the following images")
for (image, page) in found_in_img_page:
    # page increment by 1 for readability
    print("Page {}, image {}".format(page, image))
