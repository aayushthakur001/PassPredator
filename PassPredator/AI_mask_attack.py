# AI-Powered Mask Attack Implementation
import itertools
import os
import openai

def load_leaked_passwords(file_path):
    """
    Load leaked passwords from a file into a set for quick lookup.
    """
    if not os.path.exists(file_path):
        print(f"Leaked passwords file not found: {file_path}")
        return set()
    
    with open(file_path, "r", encoding="utf-8") as file:
        return set(line.strip() for line in file)

def generate_ai_suggestions(prompt, api_key):
    """
    Use OpenAI's GPT to generate additional password suggestions.
    """
    openai.api_key = api_key
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50,
            n=5,
            stop=None,
            temperature=0.7,
        )
        suggestions = [choice['text'].strip() for choice in response.choices]
        return suggestions
    except Exception as e:
        print(f"Error generating AI suggestions: {e}")
        return []

def generate_passwords(name, birthdate, phone, email, vehicle, leaked_passwords_file=None, openai_api_key=None):
    common_suffixes = ["123", "!", "@", "#", "2024", "01", "99"]
    special_chars = ["!", "@", "#", "$", "_"]
    
    name_variations = [name, name.lower(), name.upper(), name.capitalize(), name[:3], name[-3:]]
    birth_variations = [birthdate, birthdate[-4:], birthdate[:4], birthdate.replace("-", "")] if birthdate else []
    phone_variations = [phone[-4:], phone[-6:], phone[:6]] if phone else []
    email_variations = [email.split("@")[0]] if email else []
    vehicle_variations = [vehicle, vehicle[-4:]] if vehicle else []
    
    base_words = name_variations + birth_variations + phone_variations + email_variations + vehicle_variations
    base_words = [word for word in base_words if word]  # Remove empty values
    
    generated_passwords = set()
    
    for word in base_words:
        for suffix in common_suffixes:
            generated_passwords.add(word + suffix)
            generated_passwords.add(suffix + word)
        for special in special_chars:
            generated_passwords.add(word + special)
            generated_passwords.add(special + word)
    
    # Generate combinations
    for combo in itertools.permutations(base_words, 2):
        generated_passwords.add("".join(combo))
    
    ai_suggestions = []
    if openai_api_key:
        prompt = (
            f"Generate creative password variations based on the following details:\n"
            f"Name: {name}\nBirthdate: {birthdate}\nPhone: {phone}\n"
            f"Email: {email}\nVehicle: {vehicle}\n"
        )
        ai_suggestions = generate_ai_suggestions(prompt, openai_api_key)
    
    # Combine AI suggestions with generated passwords
    generated_passwords.update(ai_suggestions)
    
    leaked_passwords = load_leaked_passwords(leaked_passwords_file) if leaked_passwords_file else set()
    
    # Prioritize leaked passwords
    prioritized_passwords = [pw for pw in generated_passwords if pw in leaked_passwords]
    non_prioritized_passwords = [pw for pw in generated_passwords if pw not in leaked_passwords]
    
    # Combine prioritized and non-prioritized passwords
    final_passwords = prioritized_passwords + non_prioritized_passwords
    return final_passwords[:100]  # Limit to 100 guesses for performance

if __name__ == "__main__":
    # Example test
    leaked_passwords_path = "leaked_passwords.txt"  # Path to leaked passwords file
    openai_api_key = "your_openai_api_key_here"  # Replace with your OpenAI API key
    passwords = generate_passwords(
        "John", "1990-05-23", "9876543210", "john.doe@gmail.com", "AB1234XY",
        leaked_passwords_file=leaked_passwords_path, openai_api_key=openai_api_key
    )
    for pw in passwords:
        print(pw)
