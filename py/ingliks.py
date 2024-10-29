import itertools
import re

dictionary = { 
  # long vowels
    
    "iːe‍": "ï'e", # prime fix
    "ɑː": "ä", # AHH
    "ɜː": "q'", # UHH
    "iː": "ï", # EE
    "ɔː": "ö", # OR
    "uː": "u", # OO
    
  # diphthong 

    "ʊə‍": "u'q", # prime fix
    "ɪə‍": "ï'q", # prime fix
    
    "e‍ə": "e'", # AIR
    "i‍ə": "i'", # ERE
    "a‍ɪ": "äï", # AI
    "ə‍ʊ": "qu", # O
    "a‍ʊ": "au", # AU
    "e‍ɪ": "eï", # EI
    "ɔɪ": "öï", # OI

    # double consonants

    "t‍ʃ": "c", # CH
    "d‍ʒ": "j", # J
    "tɹ": "cr", # TR

  # smiley face

    ":)": "[REDACTED]", # censoring stuff

  # short vowels

    "æ": "a", # A
    "ɛ": "e", # E
    "i": "ï", # EE
    "ɪ": "i", # I
    "ɒ": "o", # O
    "ɔ": "ö", # OR
    "ʌ": "y", # U
    "ʊ": "ü", # OUH
    "ə": "q", # UH
    "ɐ": "q", # UH

  # voiced opposites

    "p": "p", # P
    "b": "b", # B

    "k": "k", # K
    "ɡ": "g", # G

    "f": "f", # F
    "v": "v", # V

    "t": "t", # T
    "d": "d", # D

    "s": "s", # S
    "z": "z", # Z

    "θ": "þ", # TH
    "ð": "ð", # TH

    "ʃ": "x", # SH
    "ʒ": "z̈", # ZH

  # nasal sounds

    "m": "m", # M
    "n": "n", # N
    "ŋ": "ŋ", # NG

  # odd sounds

    "h": "h", # H
    "l": "l", # L
    "ɹ": "r", # R
    "w": "w", # W
    "j": "ë" # Y
}

class Translator:
    def __init__(self):
        self.dictionary = dictionary
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.lines = open("./py/lines.txt", "r").read().splitlines()
        for i,line in enumerate(self.lines):
            if line != '':
                self.lines[i] = [int(j) for j in line.split(",")] 
        self.dict_single = open("./py/en_UK_single.txt", "r", encoding="utf8").read().splitlines()

      
    def replace_substring(self, s, start, end, replacement):
        return s[:start] + replacement + s[end:]

    def translate(self, text):
        # Step 1: Convert to lowercase
        text = text.lower()

        # Step 2: Split the text, preserving punctuation and spaces as separate items
        split_text = re.findall(r"[a-zA-Z']+(?='[a-zA-Z])|[a-zA-Z']+|[^a-zA-Z']", text)

        print(split_text)

        # Step 3: Translate words and keep track of those not translatable
        not_in_dict = []

        for i, word in enumerate(split_text):
            if word[0].isalpha():
                translation, is_translatable = self.translate_word(word)
                split_text[i] = translation
    
                if not is_translatable:
                    not_in_dict.append(word)

        # Step 4: Join the list to form the final string
        translated_list = ''.join(split_text)

        return translated_list, not_in_dict

    def english_to_ipa(self, word):
        first_two = word[0:2]
        try:
            first_two_value = self.alphabet.index(first_two[0]) * 26 + self.alphabet.index(first_two[1])
        except:
            # less than 2 letters
            for entry in self.dict_single:
                match = re.search(r'(\w+)\s*/(.*)/', entry)
                if match:
                    dict_word = match.group(1)
                    if dict_word == word:
                        ipa = match.group(2)
                        return ipa
                else:
                    print("error")
            return ""

        if self.lines[first_two_value] == '': # first two not in dictionary  
            return ""
        else:
            lines = []
            ipa_dict = open("./py/en_UK.txt", "r", encoding="utf8")
            lines = itertools.islice(ipa_dict, self.lines[first_two_value][0] - 1, self.lines[self.lines[first_two_value][1]][0] - 1)
                
            # to IPA
            # print(first_two_value)
            # print(lines[lines[first_two_value][1]])
            for line in lines:
                match = re.search(r'(\w+)\s*/(.*)/', line)
                if match:
                    dict_word = match.group(1)
                    if dict_word == word:
                        ipa = match.group(2)
                        return ipa
                else:
                    print("error")
            return ""
    

    def ipa_to_ingliks(self, word):
        # if re.search(r'\*(.*?)\*', translated[i]):
            # continue
        word_copy = word
        for key in self.dictionary:
            while (pos := word_copy.find(key)) != -1:
                # print(key)
                # print(pos)
                key_length = len(key)
                print(word, key, pos, pos + key_length, dictionary[key])
                word = self.replace_substring(word, pos, pos + key_length, dictionary[key])
                # print(translated[i])
                filler = " " * len(dictionary[key])
                word_copy = word_copy.replace(key, filler, 1)
                
        word = word.replace("ˈ", "")
        word = word.replace("ˌ", "")
        return word
        
        
    def translate_word(self, word):
        ipa = self.english_to_ipa(word)
        if ipa == "":
            return '"'+word+'"', False
        
        return self.ipa_to_ingliks(ipa), True
