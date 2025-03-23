# import the necessary packages
from pyimagesearch.transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
args = vars(ap.parse_args())

# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)
# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)

# Try different Canny parameters for better edge detection
edged = cv2.Canny(gray, 75, 200)
# show the original image and the edge detected image
print("STEP 1: Edge Detection")
cv2.imshow("Image", image)
cv2.imshow("Edged", edged)
cv2.waitKey(0)

# Improve edge detection with morphological operations
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
cv2.imshow("Closed Edges", closed)
cv2.waitKey(0)

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

# Debug: Draw all top contours
contour_img = image.copy()
for i, c in enumerate(cnts):
    cv2.drawContours(contour_img, [c], -1, (0, 255, 0), 2)
    # Add a label to identify each contour
    M = cv2.moments(c)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.putText(contour_img, f"{i+1}", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

cv2.imshow("All Contours", contour_img)
cv2.waitKey(0)

# initialize screenCnt
screenCnt = None
# Try different approximation parameters
for eps_factor in [0.02, 0.03, 0.05, 0.01]:
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, eps_factor * peri, True)
        
        # If we find a 4-point contour that's reasonably large
        if len(approx) == 4 and cv2.contourArea(approx) > (image.shape[0] * image.shape[1] / 20):
            screenCnt = approx
            print(f"Found contour with epsilon factor: {eps_factor}")
            break
    
    if screenCnt is not None:
        break

# Check if a valid contour was found
if screenCnt is None:
    print("No document contour found. Try with a different image.")
    cv2.destroyAllWindows()
    exit()

# show the contour (outline) of the piece of paper
print("STEP 2: Find contours of paper")
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# apply the four point transform to obtain a top-down
# view of the original image
pts = screenCnt.reshape(4, 2)
pts = pts * ratio  # Scale points back to original image size
warped = four_point_transform(orig, pts)
# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
cv2.imshow("Warped (Before Threshold)", imutils.resize(warped_gray, height=650))
cv2.waitKey(0)
T = threshold_local(warped_gray, 11, offset=10, method="gaussian")
thresh_mask = (warped_gray > T).astype("uint8") * 255
cv2.imshow("Threshold Mask", imutils.resize(thresh_mask, height=650))
cv2.waitKey(0)
warped = (warped_gray > T).astype("uint8") * 255
# show the original and scanned images
print("STEP 3: Apply perspective transform")
cv2.imshow("Original", imutils.resize(orig, height = 650))
cv2.imshow("Scanned", imutils.resize(warped, height = 650))
cv2.waitKey(0)