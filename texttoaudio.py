import PyPDF2
import pyttsx3
def texttoaudio(file_path:str):
    with open(file_path,'rb') as f:
        pdfReader = PyPDF2.PdfFileReader(f)
        pages = pdfReader.numPages
        speaker = pyttsx3.init()
        for num in range(12, pages):
            page = pdfReader.getPage(num)
            text = page.extractText()
            speaker.say(text)
            speaker.runAndWait()