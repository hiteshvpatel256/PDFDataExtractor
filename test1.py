import cv2
import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

# read your file
file = 'tmp-000035.png'
img = cv2.imread(file, 0)
img.shape
# thresholding the image to a binary image
thresh, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# inverting the image
img_bin = 255-img_bin
cv2.imwrite('cv_inverted.png', img_bin)

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
cv2.imwrite("vertical.jpg", vertical_lines)
# Plot the generated image
# plotting = plt.imshow(image_1,cmap='gray')
# plt.show()

# Use horizontal kernel to detect and save the horizontal lines in a jpg
image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)
cv2.imwrite("horizontal.jpg", horizontal_lines)
# Plot the generated image
# plotting = plt.imshow(image_2,cmap='gray')
# plt.show()

# Combine horizontal and vertical lines in a new third image, with both having same weight.
img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
# Eroding and thesholding the image
img_vh = cv2.erode(~img_vh, kernel, iterations=2)
thresh, img_vh = cv2.threshold(img_vh, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
cv2.imwrite("img_vh.jpg", img_vh)
bitxor = cv2.bitwise_xor(img, img_vh)
bitnot = cv2.bitwise_not(bitxor)
# Plotting the generated image
# plotting = plt.imshow(bitnot, cmap='gray')
# plt.show()

# Detect contours for following box detection
contours, hierarchy = cv2.findContours(img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

ROI_number = 0
for c in reversed(contours):
    area = cv2.contourArea(c)
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    x, y, w, h = cv2.boundingRect(approx)
    # if len(approx) == 4:
    ROI = img[y:y+h, x:x+w]
    print(str(ROI_number)+' '+str(area))
    cv2.imwrite('new/ROI_{}.png'.format(ROI_number), ROI)
    ROI_number += 1


# def sort_contours(cnts, method="left-to-right"):
#     # initialize the reverse flag and sort index
#     reverse = False
#     i = 0
#     # handle if we need to sort in reverse
#     if method == "right-to-left" or method == "bottom-to-top":
#     reverse = True
#     # handle if we are sorting against the y-coordinate rather than
#     # the x-coordinate of the bounding box
#     if method == "top-to-bottom" or method == "bottom-to-top":
#     i = 1
#     # construct the list of bounding boxes and sort them from top to
#     # bottom
#     boundingBoxes = [cv2.boundingRect(c) for c in cnts]
#     (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
#     key=lambda b:b[1][i], reverse=reverse))
#     # return the list of sorted contours and bounding boxes
#     return (cnts, boundingBoxes)

# # Sort all the contours by top to bottom.
# contours, boundingBoxes = sort_contours(contours, method=”top-to-bottom”)
