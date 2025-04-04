# Brute Force Attack Implementation
import itertools
import string

def brute_force_attack(target_hash, hash_function, min_length=4, max_length=8):
    char_set = string.ascii_letters + string.digits + string.punctuation
    for length in range(min_length, max_length + 1):
        for guess in itertools.product(char_set, repeat=length):
            password = ''.join(guess)
            if hash_function(password) == target_hash:
                return password
    return None
