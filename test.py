from fuzzywuzzy import fuzz

word = "EGE.ITALIENSKSALAT"
target =  "italiensksalat"

similarity_score: int = fuzz.ratio(word.lower(), target)

print(similarity_score)