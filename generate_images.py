import os
import glob
import constants
import cv2
import numpy as np


def pdf_to_png(filepath):
    if os.name == 'nt':
        current_dir = constants.WINDOWS_CD
    else:
        current_dir = constants.LINUX_CD

    os.system(current_dir+'pdftopng -mono -r 300 "'+filepath+'" '+constants.PAGE_PNG_PATH+'tmp ')

    # Remove 2nd page png from directory
    for tmpfile in glob.glob(constants.PAGE_PNG_PATH+"*002.png"):
        os.remove(tmpfile)

    retrieve_voter_images()

    return


def retrieve_voter_images():
    listOfPng = os.listdir(constants.PAGE_PNG_PATH)
    listOfPng.sort()
    listOfPng.pop(0)

    voter_image_counter = 1
    for imageName in listOfPng:
        page_no = int(imageName[imageName.rfind('-')+1:-4])
        imagePath = constants.PAGE_PNG_PATH + imageName

        img = cv2.imread(imagePath, 0)
        img.shape
        # thresholding the image to a binary image
        thresh, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # inverting the image
        img_bin = 255-img_bin
        # cv2.imwrite('cv_inverted.png', img_bin)

        # Length(width) of kernel as 100th of total width
        kernel_len = np.array(img).shape[1]//100
        # Defining a vertical kernel to detect all vertical lines of image
        ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
        # Defining a horizontal kernel to detect all horizontal lines of image
        hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
        # A kernel of 2x2
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

        # Use vertical kernel to detect and save the vertical lines in a jpg
        image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
        vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)
        # cv2.imwrite("vertical.jpg", vertical_lines)

        # Use horizontal kernel to detect and save the horizontal lines in a jpg
        image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
        horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)
        # cv2.imwrite("horizontal.jpg", horizontal_lines)

        # Combine horizontal and vertical lines in a new third image, with both having same weight.
        img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
        # Eroding and thesholding the image
        img_vh = cv2.erode(~img_vh, kernel, iterations=2)
        thresh, img_vh = cv2.threshold(img_vh, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # cv2.imwrite("img_vh.jpg", img_vh)
        bitxor = cv2.bitwise_xor(img, img_vh)
        bitnot = cv2.bitwise_not(bitxor)

        # Detect contours for following box detection
        contours, hierarchy = cv2.findContours(img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for c in reversed(contours):
            area = cv2.contourArea(c)
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            if area > 215000 and area < 217000:
                ROI = img[y:y+h, x:x+w]
                cv2.imwrite(constants.VOTER_PNG_PATH+constants.PREFIX_VOTER_TEXTFILE+'_'+str(page_no)+'_'+str(voter_image_counter)+'.png', ROI)
                voter_image_counter += 1
            elif area > 212900 and area < 214000:
                ROI = img[y:y+h, x:x+w]
                cv2.imwrite(constants.VOTER_PNG_PATH+constants.PREFIX_VOTER_TEXTFILE_NEW+'_'+str(page_no)+'_'+str(voter_image_counter)+'.png', ROI)
                voter_image_counter += 1
            elif area > 212000 and area < 212900:
                ROI = img[y:y+h, x:x+w]
                cv2.imwrite(constants.VOTER_PNG_PATH+constants.PREFIX_VOTER_TEXTFILE_DELETED+'_'+str(page_no)+'_'+str(voter_image_counter)+'.png', ROI)
                voter_image_counter += 1

    return
