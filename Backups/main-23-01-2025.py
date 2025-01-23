
import os
import numpy as np
import match_words
import image_procces
from database_manager import DatabaseManager

# Todo 1: Kunne være der skulle laves en databaser/fil hvor ord med ens betydning kan gruppers.
# F.eks.: rugbrød: "detgodesolsikkerugbrød","gulerodsrugbrød", "brians rugbrød" Hvis programmet bedømmer at der fås nogen af dem
# ses det blot som rugbrød. Dog kræver det at de overstående indskrives i madvarer_mk1 filen.

# Todo 2: optionalt bool der styrer om man vil havde automatisk indstilling af f.eks tolerencen i image_processing filen. Dvs den
# starter med en lav tolerence og kører match_products_with_database og regner en samlet score for hele kvittering, dvs et gennemsnit
# af alle scores i kvitteringen. Dette gemmes sammen med tolerencen. Dernæst prøves en større tolerence. Hvis det nye gennemsnit er 
# højere end det forrige så hæves tolerence indtil den bliver lavere. 


#-------------------------------------------
#-
#-------------------------------------------
def main():
    image_folder_path: str = os.path.join(os.getcwd(),"images")
    file_count: int = len([f for f in os.listdir(image_folder_path) if os.path.isfile(os.path.join(image_folder_path, f))])
    
    for picture_number in range(1,file_count+1):
        
        # Choose image from 1 to x
        image_name: str = "picture"+str(picture_number)+".jpg"
        image_path: str = os.path.join(os.getcwd(),"images", image_name) 
        
        # Load image
        image: np.ndarray = image_procces.load_image(image_path)
        
        # Make image black and white
        enhanced_image: np.ndarray = image_procces.image_processing(image, tolerance=100, showImage=False)
        
        # Save enchanced image for testing
        folder: str = "proccessed_images"
        image_procces.save_image(enhanced_image, folder, image_name)

        # Extract text from image with tesseract
        extracted_text: str = image_procces.extract_text_from_image(enhanced_image)
        
        # Filter the extracted text further
        filtered_products: list[tuple] = image_procces.text_filter1(extracted_text)
        
        # Loop over each product in filtered_products and return list of tuple of the word matches in database [(productname,price)]
        data_products: list[tuple] = match_products_with_database(image_name, filtered_products)
        
        # Initiate database
        database_file_path: str = os.path.join(os.getcwd(),"data","bought_db.db")
        database_bought_products: DatabaseManager = DatabaseManager(database_file_path)
        
        # Goes over each product and adds them to the database
        for product in data_products:
            print(f"{product[0]} has price: {product[1]/float(100)} kr")
            database_bought_products.add_or_update_item(product[0], product[1]/100)
        
        database_bought_products.close()
        
        
#-------------------------------------------
#-
#-------------------------------------------
def match_products_with_database(image_name: str, products_list: list[tuple], blacklist_threshhold: int = 50) -> list[tuple]:
    print(f"Picture: {image_name} -------------------------")
    
    products: list[tuple] = []
    
    for product in products_list:
        print(f"Product: {product}")
        
        # Exstract name of product
        target_product: str = product[0]
        
        # Get database path
        database_file_path: str = os.path.join(os.getcwd(),"data",'madvarer_mk1.txt')
        blacklist_path: str = os.path.join(os.getcwd(),"data",'blacklist.txt')

        # Load blacklist
        blacklist: list[str] = match_words.load_database_to_list(blacklist_path)

        # Return a list of words and a score for the match
        black_list_score: list[tuple] = match_words.check_words(blacklist, target_product)

        # If word is over threshold and deemed a blacklisted word then skip
        if (black_list_score[0][1] > blacklist_threshhold):
            print("BLACKLISTED")
            continue
    
        # Load product/food database
        database: list[str] = match_words.load_database_to_list(database_file_path)

        # Return a list of words and a score for the match
        database_list_score: list[tuple] = match_words.check_words(database, target_product)
        print(f"Likely matches: 1: ('{database_list_score[0][0]}') 2: ('{database_list_score[1][0]}') 3: ('{database_list_score[2][0]}')")

        product_name: str = database_list_score[0][0]
        temp_price_list: list[str] = product[1].split(",")
        
        # Make the price in ører
        product_price: int = int(temp_price_list[0])*100 + int(temp_price_list[1])
            
        products.append((product_name, product_price))
        
    return products

if __name__ == "__main__":
    main()