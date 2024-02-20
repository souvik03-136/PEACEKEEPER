import google.generativeai as genai
from pdf2image import convert_from_path
import os
import pytesseract
import fitz

def summarize_pdf(pdf_path):
    print("Summarize PDF function called")  # Add this print statement for debugging

    text = ''
    images = convert_from_path(pdf_path)

    with fitz.open(pdf_path) as pdf_document:
        text_layers = sum(page.get_text("text") != "" for page in pdf_document)

        if text_layers > 0:
            print("The PDF contains text layers.")
            for i in range(pdf_document.page_count):
                page = pdf_document[i]
                page_text = page.get_text()
                text += f'\nPage {i + 1}:\n{page_text}'
        else:
            print("The PDF may be image-based.")
            for i, image in enumerate(images):
                image_path = f'page_{i + 1}.png'
                image.save(image_path, 'PNG')
                text += pytesseract.image_to_string(image, lang='eng')

                # Delete the image file after processing
                os.remove(image_path)

    genai.configure(api_key="AIzaSyCA_GcqeNw4J8VdduzqzqWgVd4sTMo6NyI")
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"{text} Generate a comprehensive summary of the legal document provided. Extract key details such as the parties involved, background information, legal arguments presented, and the court's decision. Highlight any jurisdictional issues, interpretation of legal clauses, and recommendations made by the court. Please provide a concise overview that captures the essential aspects of the document.")

    summary_text = response.text
    print("Summary text:", summary_text)  # Print the summary text for debugging
    return summary_text