# Dictionary Attack Implementation
def dictionary_attack(target_hash, hash_function, wordlist_path):
    try:
        with open(wordlist_path, "r", encoding="utf-8") as file:
            for word in file:
                word = word.strip()
                if hash_function(word) == target_hash:
                    return word
    except FileNotFoundError:
        print("Wordlist not found.")
    return None
