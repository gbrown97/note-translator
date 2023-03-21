from tranlsate import NoteTranslator

objectTrans =  NoteTranslator('en')
inputText = "안녕하세요. How are you?"
destinationLang = 'hi'
print(objectTrans.translate(inputText, destinationLang))
print(objectTrans.translatedText)