from azure.storage.blob import BlobServiceClient
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField
from pptx import Presentation
import os
import re  
import requests
import concurrent.futures  
from functools import partial  
import pathlib

# Image processing via GPT-4o  
from IPython.display import Markdown, display

# Utils
import doc2md_utils

# Configuration
BLOB_CONNECTION_STRING = ""
BLOB_CONTAINER_NAME = ""
BLOB_NAME = ""
SEARCH_SERVICE_NAME = ""
SEARCH_API_KEY = ""
SEARCH_INDEX_NAME = ""
IMAGE_PATH = ""
MARKDOWN_PATH = ""
JSON_PATH = ""

# Extraire le contenu du fichier PowerPoint pour une indexation par slide
def convert_slides_to_markdown(file_path):
    # Convert file to PDF
    pdf_path = doc2md_utils.convert_to_pdf(file_path)
    # Extract PDF pages to images
    doc_id = doc2md_utils.extract_pdf_pages_to_images(pdf_path, IMAGE_PATH)
    pdf_images_dir = os.path.join(IMAGE_PATH, doc_id)
    print ('Images saved to:', pdf_images_dir)
    print ('Doc ID:', doc_id)
    files = doc2md_utils.get_all_files(pdf_images_dir)  
    total_files = len(files)
    print ('Total Image Files to Process:', total_files)
    # Convert the images to markdown using GPT-4o 
    # Process pages in parallel - adjust worker count as needed
    max_workers = 10
    markdown_out_dir = os.path.join(MARKDOWN_PATH, doc_id)
    doc2md_utils.ensure_directory_exists(markdown_out_dir)
    # Using ThreadPoolExecutor with a limit of max_workers threads  
    partial_process_image = partial(doc2md_utils.process_image, markdown_out_dir=markdown_out_dir)  
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Map the partial function to the array of items  
        results = list(executor.map(partial_process_image, files))
    print('Total Processed:', len(results))
    return doc_id

# Markdown dans Azure Search et indexation par slide
def slide_index_to_azure_ai_search(markdown_dir, doc_id):
    # Load the Index Schema and re-create Index
    doc2md_utils.create_index()
    # Retrieve all the markdown files and doc_id
    doc_id = doc2md_utils.get_doc_id(MARKDOWN_PATH)
    markdown_out_dir = os.path.join(MARKDOWN_PATH, doc_id)
    files = os.listdir(markdown_out_dir)
    # Filter out non-txt files (optional)  
    txt_files = [f for f in files if f.endswith('.txt')]  
    total_files = len(files)
    print ('Total Markdown Files:', total_files)
    # Vectorize the JSON Content in parallel
    max_workers = 15
    json_out_dir = os.path.join(JSON_PATH, doc_id)
    doc2md_utils.ensure_directory_exists(json_out_dir)
    partial_process_json = partial(doc2md_utils.process_json, doc_id=doc_id, markdown_out_dir=markdown_out_dir, json_out_dir=json_out_dir)  
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:  
        results = list(executor.map(partial_process_json, files))
    print(results)
    json_files = doc2md_utils.get_all_files(json_out_dir)
    total_files = len(json_files)
    print ('Total JSON Files:', total_files)
    # Index content to Azure AI Search
    doc2md_utils.index_content(json_files)

def convert_doc_to_markdown(file_path):
    # Convert file to PDF
    pdf_path = doc2md_utils.convert_to_pdf(file_path)

    # Configurer le parser d'arguments
   

# Main function
def main():
    try:
        file_path = r'C:\Users\ehemmer\Dev\INSEAD_POC\PPT-Indexation-POC\backend\HK_Company X_Mission 1.5 - Sustainability Offerings_29Aug2023.pptx'
        
        # Vérifie si le fichier existe
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Le fichier spécifié est introuvable : {file_path}")
        
        # Par slide
        # Extraire le contenu du fichier PowerPoint
        doc_id = convert_slides_to_markdown(file_path)
        # Indexation du contenu dans Azure AI Search
        slide_index_to_azure_ai_search(MARKDOWN_PATH, doc_id)

        # Document complet


        print("Pipeline terminé avec succès.")
    except Exception as e:
        print(f"Erreur dans le pipeline : {e}")

if __name__ == "__main__":
    main()