import cv2

method = cv2.TM_SQDIFF_NORMED

# Read the images from the file
landing_zone = cv2.imread('landing_image.jpg')
large_image = cv2.imread('view.jpg')

result = cv2.matchTemplate(landing_zone, large_image, method)

# We want the minimum squared difference
mn, _, mnLoc, _ = cv2.minMaxLoc(result)

# Draw the rectangle:
# Extract the coordinates of our best match
MPx, MPy = mnLoc
print(MPx, MPy, "X and Y location of best match")

# Step 2: Get the size of the template. This is the same size as the match.
trows, tcols = landing_zone.shape[:2]

# Step 3: Draw the rectangle on large_image
cv2.rectangle(large_image, (MPx, MPy), (MPx+tcols, MPy+trows), (0, 255, 255), 20)

# Display the original image with the rectangle around the match.
cv2.imshow('output', large_image)

# The image is only displayed if we call this
cv2.waitKey(0)
cv2.destroyAllWindows()
quit()

