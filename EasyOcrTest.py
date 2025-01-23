import easyocr
import os
import cv2
import image_procces

image_path = os.path.join(os.getcwd(),"images","picture1.jpg")
reader = easyocr.Reader(['en'], gpu=True)  # Specify languages
image = cv2.imread(image_path)


#b_image = image_procces.image_processing(image, tolerance=120)
#image_procces.save_image(b_image, os.path.join(os.getcwd(),"images"),"picture1.jpg")

result = reader.readtext(image_path)

for detection in result:
    
    print(f"Text: {detection[1]}, Confidence: {detection[2]}")
        
        
        
# Loop through detected text and bounding boxes
for (bbox, text, confidence) in result:
    # Unpack the bounding box coordinates
    (top_left, top_right, bottom_right, bottom_left) = bbox
    top_left = tuple(map(int, top_left))
    bottom_right = tuple(map(int, bottom_right))

    # Draw a rectangle around the text
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

    # Put the detected text above the rectangle
    cv2.putText(image, text, (top_left[0], top_left[1] - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

# Save or display the image
output_path = 'output.jpg'
cv2.imwrite(output_path, image)
print(f"Image saved with detection boxes: {output_path}")

# Optional: Display the image (if you're running locally)
# cv2.imshow('Detected Text', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()