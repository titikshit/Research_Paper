import streamlit as st
import requests
from lxml import etree
import csv
import io  

def grobid_process_pdf(file_obj, timeout=30):
    url = 'http://localhost:8070/api/processHeaderDocument'
    try:
        files = {'input': (file_obj.name, file_obj, 'application/pdf')}
        response = requests.post(url, files=files, timeout=timeout)
        if response.status_code == 200:
            return response.content.decode('utf-8')
        else:
            st.error(f"GROBID returned status code {response.status_code}")
            return None
    except requests.Timeout:
        st.error("Request to GROBID timed out. Try again or use a smaller file.")
        return None
    except requests.ConnectionError:
        st.error("Could not connect to the GROBID service. Please ensure it is running.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

def parse_tei_xml(tei_xml):
    try:
        tei_xml_bytes = tei_xml.encode('utf-8')
        tree = etree.fromstring(tei_xml_bytes)
        
        title_elements = tree.xpath('//*[local-name()="titleStmt"]/*[local-name()="title"]')
        title = title_elements[0].text.strip() if title_elements and title_elements[0].text else "Not Found"

        pers_name_elements = tree.xpath('.//*[local-name()="persName"]')
        authors = []
        for pers in pers_name_elements:
            full_name = ' '.join(pers.xpath('.//text()')).strip()
            if full_name:
                authors.append(full_name)
        
        if not authors:
            org_name_elements = tree.xpath('.//*[local-name()="orgName"]')
            for org in org_name_elements:
                org_name = ' '.join(org.xpath('.//text()')).strip()
                if org_name:
                    authors.append(org_name)
        
        authors = list(dict.fromkeys(authors))
        
        date_elements = tree.xpath('.//*[local-name()="date"]')
        dates = []
        for date in date_elements:
            date_text = date.text.strip() if date.text else ''
            if date_text and any(char.isdigit() for char in date_text):
                dates.append(date_text)
        year = dates[0] if dates else "Not Found"
        
        return {
            "Title": title, 
            "Authors": ", ".join(authors) if authors else "Not Found", 
            "Year": year
        }
    except etree.XMLSyntaxError as e:
        st.error(f"Failed to parse the XML returned by GROBID: {e}")
        return {"Title": "Not Found", "Authors": "Not Found", "Year": "Not Found"}
    except Exception as e:
        st.error(f"An error occurred while parsing the XML: {e}")
        return {"Title": "Not Found", "Authors": "Not Found", "Year": "Not Found"}

st.title("Research Paper Extractor")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    try:
        with st.spinner('Processing...'):
            extracted_metadata = grobid_process_pdf(uploaded_file, timeout=30)
        
        if extracted_metadata:
            st.subheader("Extracted Metadata:")

            parsed_data = parse_tei_xml(extracted_metadata)
            st.write(f"**Title:** {parsed_data['Title']}")
            st.write(f"**Authors:** {parsed_data['Authors']}")
            st.write(f"**Year of Publication:** {parsed_data['Year']}")

            output = io.StringIO()
            writer = csv.writer(output)

            writer.writerow(['Title', 'Authors', 'Year'])
            writer.writerow([parsed_data['Title'], parsed_data['Authors'], parsed_data['Year']])

            csv_content = output.getvalue()
            output.close()

            st.download_button(
                label="Download Metadata as CSV",
                data=csv_content,
                file_name='metadata.csv',
                mime='text/csv'
            )

        else:
            st.error("Failed to process the PDF. Please try again.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")