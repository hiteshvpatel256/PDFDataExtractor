from PIL import Image
import pytesseract
import os
import constants


def generate_text():

    # Getting first page from list of pages and ocr it
    listofpages = os.listdir(constants.PAGE_PNG_PATH)
    listofpages.sort()
    commonVoterpng = listofpages.pop(0)
    imagePath = constants.PAGE_PNG_PATH+commonVoterpng
    outputPath = '.'+os.path.sep+constants.COMMON_VOTER_DETAIL_TEXTFILE
    do_ocr(imagePath, outputPath, constants.TESS_LANGAUGE_COMMON_DETAIL, '4')

    # Getting all voters from directory and do ocr for each
    listOfPng = os.listdir(constants.VOTER_PNG_PATH)
    listOfPng.sort()

    for imageName in listOfPng:
        imagePath = constants.VOTER_PNG_PATH + imageName
        outputPath = constants.VOTER_PNG_PATH + imageName[0:-4]+'.txt'
        do_ocr(imagePath, outputPath, constants.TESS_LANGAUGE_VOTER_DETAIL, '6')

    return


def do_ocr(imagePath, outputPath, tess_language, psm):
    img = Image.open(imagePath)

    if os.name == 'nt':
        pytesseract.pytesseract.tesseract_cmd = './tesseract/tesseract'

    # applying ocr using pytesseract for python
    text = pytesseract.image_to_string(img, lang=tess_language, config='--psm '+psm+' --oem 1')

    # saving the  text for every image in a separate .txt file
    file1 = open(outputPath, "w", encoding='utf-8')
    file1.write(text)
    file1.close()
    return
