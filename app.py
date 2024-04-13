import streamlit as st 
import pandas as pd
import docx2txt 
import re  
import pandas as pd 
from openpyxl.workbook import Workbook
from docx import Document  # For processing DOCX files
from PyPDF2 import PdfReader  # For processing PDF files
from io import BytesIO



def main():
    st.title("CV Parser Application")
    
    uploaded_files = st.file_uploader("Upload CVs", type=['docx', 'pdf'], accept_multiple_files=True)
    textual_data = []
    if uploaded_files:
        with st.spinner("Processing..."):
            for uploaded_file in uploaded_files:
                text = extract_text_from_cv(uploaded_file)
                if text:
                    textual_data.extend(text)
    
    df = pd.DataFrame(textual_data)
    # st.write(df)
    
    # Create a BytesIO object
    output = BytesIO()
    excel_file_name = 'data.xlsx'

    # Write DataFrame to the BytesIO object
    df.to_excel(output, index=False)

    # Retrieve the data from the BytesIO object as bytes
    excel_file = output.getvalue()

    # Add a button to download the Excel file
    if st.download_button(label="Download Excel", data=excel_file, file_name=excel_file_name, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
        st.success("Excel file created successfully: {}".format(excel_file_name))

    
def extract_text_from_cv(cv):
    data_list = []
    
    # Extract text from the CV
    if cv.name.endswith('.docx'):
        # Read the DOCX file
        doc = Document(cv)
        text = '\n'.join([para.text for para in doc.paragraphs])
    elif cv.name.endswith('.pdf'):
        # Read the PDF file
        reader = PdfReader(cv)
        text = ''.join([reader.pages[page_num].extract_text() for page_num in range(len(reader.pages))])
    
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b(?:\+\d{1,2}\s)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    
    emails = re.findall(email_pattern,text)
    phones  = re.findall(phone_pattern, text)
    
    # Add overall text
    overall_text = text
    
    data_list.append({"Email": ', '.join(emails), "Phone": ', '.join(phones), "Overall Text": overall_text})
   
    return data_list


if __name__ == '__main__':
    main()
