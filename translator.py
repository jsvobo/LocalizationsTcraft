import os

#!/usr/bin/env python3
import requests

TEMPLATE_PATH = './langs/en_us.lang'
LANGS_DIR = './langs'
GOOGLE_TRANSLATE_API_URL = 'https://translation.googleapis.com/language/translate/v2'
API_KEY = 'YOUR_GOOGLE_API_KEY'  # Replace with your actual API key

def read_template(path):
    translations = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                translations.append((key, value))
    return translations

def translate_text_batch(texts, target_lang):
    params = {
        'q': texts,
        'target': target_lang,
        'source': 'en',
        'key': API_KEY
    }
    response = requests.post(GOOGLE_TRANSLATE_API_URL, params=params)
    if response.status_code == 200:
        result = response.json()
        return [t['translatedText'] for t in result['data']['translations']]
    else:
        print(f"Batch translation error: {response.text}")
        return texts  # fallback to original

def write_translations(translations, target_lang):
    out_path = os.path.join(LANGS_DIR, f'{target_lang}.lang')
    with open(out_path, 'w', encoding='utf-8') as f:
        for key, value in translations:
            f.write(f"{key}={value}\n")

def main(target_lang):
    try:
        with open('./secrets', 'r', encoding='utf-8') as secret_file:
            global API_KEY
            API_KEY = secret_file.read().strip()
        print("the API key is", API_KEY)
    except FileNotFoundError:
        print("No API key found, please create a 'secrets' file with your Google \
Translate API key or delete this part of the code and copy API key directly \
into the code. Note, that you should not post API keys to git")
        return

    template = read_template(TEMPLATE_PATH)
    translated = []
    batch_size = 100
    for i in range(0, len(template), batch_size):
        batch = template[i:i+batch_size]
        keys = [k for k, v in batch]
        values = [v for k, v in batch]
        translated_values = translate_text_batch(values, target_lang)
        translated.extend(zip(keys, translated_values))
    write_translations(translated, target_lang)
    print(f"Translated file saved to {os.path.join(LANGS_DIR, f'{target_lang}_{target_lang}.lang')}")

if __name__ == '__main__':
    # major_languages = [ 'fr', 'ar',  'hi', 'ja', 'it', 'ko', 'tr', 'pl', 'cz']
    main(target_lang = "it")







