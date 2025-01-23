# Goal: rank inputstring compared to a database of items. For example. Input: pepsimax Database: pepsi max, cola, cheese, bread. Then it will rank what i most likely is closest to.
from fuzzywuzzy import fuzz

#-------------------------------------------
#-
#-------------------------------------------
def load_database_to_list(file_path: str) -> list[str]:
    database: list[str] = []
    with open(file_path, "r") as file:
        for word in file:
            database.append(word.strip())
    
    return database        
#-------------------------------------------
#-
#-------------------------------------------
def check_words(database: list[str], target: str) -> list[str]:
    """Ranks database content based on target word"""
    target: str = target.lower()
    word_and_score: list[tuple] = []
    
    # With fuzz find the edit distance for each word compared to target word
    for word in database:
        similarity_score: int = fuzz.ratio(word, target)
        word_and_score.append((word,similarity_score))
    
    # Sort the words based on edit distance, the higher the more likely it is a match
    words_sorted: list[tuple] = sorted(word_and_score, key=lambda x: x[1], reverse=True)

    return words_sorted
#-------------------------------------------
#-
#-------------------------------------------

# Code test example:
if __name__ == "__main__":
    input: str = "egelykkerullepolse"

    database_file_path: str = os.path.join(os.getcwd(),"data",'madvarer_mk1.txt')

    database: list[str] = load_database_to_list(database_file_path)

    list_test: list[tuple] = check_words(database, input)

    for line in list_test:
        print(line)
        
    print(f"Most likely: {list_test[0]}")
