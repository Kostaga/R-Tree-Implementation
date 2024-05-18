import random

prefixes = ["Spring", "Twin", "Lake", "Sunny", "Golden", "George's", "Kostas's"]
suffixes = ["ville", "field", "port", "cave", "statue", "tavern", "inn", "house", "dungeon"]

def location_name_generator():
    return random.choice(prefixes) + " " + random.choice(suffixes)
