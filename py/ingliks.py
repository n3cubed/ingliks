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


   def translate(self, sentence):
      not_in_dict = []

      def word_not_in_dict(self, word, translated):
        translated.append('"' + word + '"')
        not_in_dict.append(word)
        return translated

      words = sentence.lower().split()
      translated = []

      for word in words:
         first_two = word[0:2]
         try:
            first_two_value = self.alphabet.index(first_two[0]) * 26 + self.alphabet.index(first_two[1])
         except:
            # less than 2 letters
            matched = False
            for entry in self.dict_single:
               match = re.search(r'(\w+)\s*/(.*)/', entry)
               if match:
                  dict_word = match.group(1)
                  if dict_word == word:
                     ipa = match.group(2)
                     translated.append(ipa)
                     matched = True
                     break
               else:
                  print("error")
            if not matched:
               translated = word_not_in_dict(self, word, translated)
            continue

         if self.lines[first_two_value] == '': # first two not in dictionary  
            translated = word_not_in_dict(self, word, translated)
         else:
            with open("./py/en_UK.txt", "r", encoding="utf8") as ipa_dict:
               # to IPA
               matched = False
               # print(first_two_value)
               # print(lines[lines[first_two_value][1]])
               for line in itertools.islice(ipa_dict, self.lines[first_two_value][0] - 1, self.lines[self.lines[first_two_value][1]][0] - 1):
                  match = re.search(r'(\w+)\s*/(.*)/', line)
                  if match:
                     dict_word = match.group(1)
                     if dict_word == word:

                        ipa = match.group(2)
                        translated.append(ipa)
                        matched = True
                        break
                  else:
                     print("error")
               if not matched:
                  translated = word_not_in_dict(self, word, translated)
               continue

      ipa = " ".join(translated)

      for i in range(len(translated)):
         if re.search(r'\*(.*?)\*', translated[i]):
            continue
         translated[i] = translated[i].replace("ˈ", "")
         translated[i] = translated[i].replace("ˌ", "")
         word = translated[i]
         # print(translated)
         for key in dictionary:
            pos = word.find(key)
            while pos != -1:
               # print(key)
               # print(pos)
               key_length = len(key)
               print(translated[i], key, pos, pos + key_length, dictionary[key])
               translated[i] = self.replace_substring(translated[i], pos, pos + key_length, dictionary[key])
               # print(translated[i])
               filler  = ""
               for j in range(len(dictionary[key])):
                  filler += " "
               word = word.replace(key, filler, 1)
               pos = word.find(key)

      translated = " ".join(translated)
      # with open("./py/output.txt","a", encoding="utf8") as f:
      #    f.write(translated + "\n")
      #    f.write(ipa+"\n")
      return translated, not_in_dict
