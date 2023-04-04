#installing required packages
from googletrans import Translator
from spacy.lang.xx import MultiLanguage
from util import S3Storage
import ocr

class NoteTranslator:
  #Adding sentence recognizer pipeline 
  #Constructor
  def __init__(self,src,filePath,storage) -> None:
    self.nlp = MultiLanguage()
    self.nlp.add_pipe("sentencizer")
    self.src = src
    self.translator = Translator()
    self.filePath = filePath
    self.translatedText = ""
    self.userStorage = storage

  #method to read txt/jpg file.
  def __readFile(self):
    if self.filePath.endswith(".txt"):
      datatext,dataFile = self.userStorage.loadTxt(self.filePath)
      return datatext

  def __extractText(self, keyFile):
    response = ocr.textract(keyFile)
    extractedText = ocr.extract_text(response)
    return extractedText

  # Method to translate the text.
  # text: input text to translate into destination langugage.
  # dest: destination language code example English -> "en".
  def translate(self, dest):
    text = self.__readFile() if self.filePath.endswith(".txt") else self.__extractText(self.filePath)
    ttext=text.read()
    # A generator object is generated using spacy consits of meaningful sentences.
    for sentence in self.nlp(ttext.decode()).sents:
      try:
        self.translatedText = self.translatedText + self.translator.translate(str(sentence), dest=dest).text + " "
      except Exception as e:
        try :
          self.translatedText = self.translatedText + self.translator.translate(str(sentence), dest=dest).text + " "  
        except:
          self.translatedText = self.translatedText + str(sentence) + " "
    return self.translatedText  # returns the translated text.
  def readFile(self):
    text= self.__readFile()
    contents=text.read()
    return contents.decode()