import itertools
import re

dictionary = { 
  # long vowels

   "ɑː": "ä", # as in cA
   "ɜː": "q'", # as in bIRd
   "iː": "ï", # as in kEY
   "ɔː": "ö", # as in tOUR
   "uː": "u", # as in mOOn

  # diphthong 

   "e‍ə": "e'", # as in hAIR
   "a‍ɪ": "äï", # as in hIGH
   "ɪə‍": "ï'q", # as in serIAl
   "iə‍": "i'", # as in hERE
   "i‍ə": "i'", # as in hERE
   "ə‍ʊ": "qu", # as in bOAt
   "əʊ": "qu", # as in bOAt
   "aʊ": "au", # as in nOW
   "a‍ʊ": "au", # as in nOW
   "oʊ": "qu", # as in bOAt
   "e‍ɪ": "eï", # as in hEY
   "ɔɪ": "öï", # as in OIl
   "ʊə‍": "u'q", # as in tOUr (posh)

   # double consonants

   "t‍ʃ": "c", # as in CHat
   "d‍ʒ": "j", # as in Jug

  # smiley face

   ":)": "[REDACTED]", # censoring stuff

  # short vowels

   "æ": "a", # as in cAt
   "ɛ": "e", # as in bEd
   "i": "ï", # as in tEA
   "ɪ": "i", # as in tIp
   "ɒ": "o", # as in nOt
   "ɔ": "ö", # as in mORE
   "ʌ": "y", # as in sUn
   "ʊ": "ü", # as in bOOk
   "ə": "q", # as in Upon
   "ɐ": "q", # as in Upon 

  # voiced opposites

   "p": "p", # as in Pie
   "b": "b", # as in Buy

   "k": "k", # as in Cool
   "ɡ": "g", # as in Ghoul

   "f": "f", # as in Fine
   "v": "v", # as in Vine

   "t": "t", # as in Too
   "d": "d", # as in Do

   "s": "s", # as in Sue
   "z": "z", # as in Zoo

   "θ": "þ", # as in THink
   "ð": "ð", # as in THat

   "ʃ": "x", # as in SHy
   "ʒ": "z̈", # as in viSion

  # nasal sounds

   "m": "m", # as in Mine
   "n": "n", # as in Nice
   "ŋ": "ŋ", # as in siNG

  # odd sounds

   "h": "h", # as in Hello
   "l": "l", # as in veLar
   "ɹ": "r", # as in Race
   "w": "w", # as in WHen
   "j": "ë" # as in Yet
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
