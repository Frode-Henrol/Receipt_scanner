import pytesseract
import cv2
import os
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
 
#-------------------------------------------
#-
#-------------------------------------------
def load_image(image_path: str) -> np.ndarray:
    image: np.ndarray | None = cv2.imread(image_path)

    if image is None:
        print("Failed to load image")
    return image
#-------------------------------------------
#-
#-------------------------------------------
def save_image(image: np.ndarray, folder: str, image_name: str) -> None:
    cv2.imwrite(os.path.join(os.getcwd(),folder,image_name),image)
#-------------------------------------------
#-
#-------------------------------------------
def image_processing(image: np.ndarray, tolerance: int = 100, showImage: bool = False) -> np.ndarray:
    target_color = np.array([0, 0, 0])

    # Create a mask for the specific color
    lower_bound = np.clip(target_color - tolerance, 0, 255)
    upper_bound = np.clip(target_color + tolerance, 0, 255)

    # Create a mask where the target color is found
    mask = cv2.inRange(image, lower_bound, upper_bound)

    # Create an output image with the target color filled with black and everything else white
    output_image = np.ones_like(image) * 255  # Create a white image
    output_image[mask != 0] = [0, 0, 0]  # Fill the target color regions with black

    # Apply Gaussian Blur to smooth edges and make text less blocky
    enhanced_image = cv2.GaussianBlur(output_image, (3, 3), 0)

    if showImage:
        # Show processed image (optional)
        cv2.imshow("Processed Image", enhanced_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return enhanced_image
#-------------------------------------------
#-
#-------------------------------------------
def extract_text_from_image(image: np.ndarray) -> str:
    # Use Tesseract to extract num
    custom_config: str = (r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,.')
    extracted_text: str = pytesseract.image_to_string(image, config=custom_config)
    
    return extracted_text
#-------------------------------------------
#-
#-------------------------------------------
def text_filter1(input_text: str) -> str:

    valid_chars: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZæøåÆØÅ"
    filtered_products: list[tuple] = []
    
    # Go through each line of the string read from the image
    for line in input_text.split("\n"):
        
        # If line is empty skip
        if not line:
            continue
        
        # If first char is not in the alfabet skip
        if line[0] not in valid_chars:
            continue
        
        # If the last and second digit are not numbers and third is not a comma skip
        if not (line[-1].isdigit() and line[-2].isdigit() and line[-3] == ","):
            continue
        
        # Split name and price at space (this could be improved in the future and use some other logic?)
        name_and_price: list[str] = line.split(" ")
        
        # This is for the case that we have a str like: "POELYAKE RULLEPOLSE 14,50" where there are more than 1 spaces. Then we combine the name and seperate the price
        if (len(name_and_price) > 2):
            price: str = name_and_price.pop(-1)
            name: str = " ".join(name_and_price)
            name_and_price[0] = name
            name_and_price[1] = price
        
        filtered_products.append((name_and_price[0],name_and_price[1]))
        
    return filtered_products
#-------------------------------------------
#-
#-------------------------------------------