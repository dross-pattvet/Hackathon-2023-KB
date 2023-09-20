# should need to ever run this. Its my script to convert existing kb articles into chroma db
import chromadb
from chromadb.config import Settings
from uuid import uuid4
import yaml
import os


persist_directory = "chromadb"
chroma_client = chromadb.Client(Settings(persist_directory=persist_directory,chroma_db_impl="duckdb+parquet",))
collection = chroma_client.get_or_create_collection(name="knowledge_base")

def open_yaml(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data
    
def save_yaml(filepath, data):
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            yamlOutput = yaml.dump(data, file, allow_unicode=True)
    except IOError:
        print("An error occurred while writing the file.")

# Directory path
dir_path = 'C:\Projects\Repos\Hackathon_2023_KnowledgeBase\KB_Microservice\kb'

# Loop through every file in the directory
for filename in os.listdir(dir_path):
    # Check if file is .yaml
    if filename.endswith('.yaml'):
        file_path = os.path.join(dir_path, filename)

        kb = open_yaml(file_path)
        
        if 'id' in kb:
            id = kb['id']
        else:
            id = str(uuid4())
            kb['id'] = id

        save_yaml(file_path, kb)
        
        collection.add(documents=[kb['body']],ids=[id],metadatas=[{"filename": filename}])
        
chroma_client.persist()