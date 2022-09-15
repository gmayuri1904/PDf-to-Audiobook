import streamlit as st
import base64
#from pdf2image import convert_from_path
import tempfile
from pathlib import Path
import pyttsx3
import PyPDF2
from gtts import gTTS


def show_pdf(file_path:str):

    with open(file_path,'rb') as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
        
        



def main():
    st.title("PDF to audio")
    uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
    
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            st.markdown("## Original PDF file")
            fp = Path(tmp_file.name)
            fp.write_bytes(uploaded_file.getvalue())
            show_pdf(tmp_file.name)
            texttoaudio(tmp_file.name)
            download_audio(tmp_file.name)
            #imgs = convert_from_path(tmp_file.name)
            #st.markdown(f"Converted images from PDF")
            #st.image(imgs)
        
       


def texttoaudio(file_path:str):
    with open(file_path,'rb') as f:
        pdfReader = PyPDF2.PdfFileReader(f)
        pages = pdfReader.numPages
        page =pdfReader.pages[0]
        text = page.extractText()
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        gender=st.radio('Voice', ['Male','Female'])
        if gender=="Male":
            engine.setProperty('voice', voices[0].id)
        if gender=="Female":
            engine.setProperty('voice', voices[1].id)
        st.subheader('Speed')
        speed=st.slider("",min_value=0.25,max_value=2.0, step=0.25, value=1.0)    
        rate = engine.getProperty('rate') 
        engine.setProperty('rate', rate*speed)
        a=st.number_input("Start index", min_value=0, max_value=pages, value=1, step=1)
        if st.button("Play"):
            for num in range(a-1, pages):
                page = pdfReader.getPage(num)
                text = page.extractText()
                engine.say(text)
                engine.runAndWait()
                
def download_audio(file_path:str):
    with open(file_path,'rb') as f:
        pdfReader = PyPDF2.PdfFileReader(f)
        pages = pdfReader.numPages
        complete_text=" "
        for num in range(0, pages):
            page = pdfReader.getPage(num)
            text = page.extractText()
            complete_text=complete_text+text
    final_file=gTTS(text=complete_text,lang="en")     
    #audio=final_file.save("Audiobook.mp3")      
    st.download_button("Download",data=final_file, file_name="Audiobook",mime="mp3")
     
 
if __name__=="__main__":
   main()