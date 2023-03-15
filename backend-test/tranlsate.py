#installing required packages
from googletrans import Translator
from spacy.lang.xx import MultiLanguage

class NoteTranslator:
  #Adding sentence recognizer pipeline
  #Constructor
  def __init__(self,src) -> None:
    self.nlp = MultiLanguage()
    self.nlp.add_pipe("sentencizer")
    self.src = src
    self.translator = Translator()
    self.translatedText = ""

  # Method to translate the text.
  # text: input text to translate into destination langugage.
  # dest: destination language code example English -> "en".
  def translate(self,text, dest):
    # A generator object is generated using spacy consits of meaningful sentences.
    for sentence in self.nlp(text).sents:
      try:
        self.translatedText = self.translatedText + self.translator.translate(str(sentence), dest=dest).text + " "
      except Exception as e:
        try :
          self.translatedText = self.translatedText + self.translator.translate(str(sentence), dest=dest).text + " "  
        except:
          self.translatedText = self.translatedText + str(sentence) + " "
    return self.translatedText  # returns the translated text.
  
