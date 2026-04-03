text, used = safe_read('assets/text_files/DutchDictionary.txt')
with open('assets/text_files/DutchDictionary.txt', 'w', encoding='utf-8') as f:
    f.write(text)
