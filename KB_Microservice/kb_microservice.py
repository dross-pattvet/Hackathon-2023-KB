import os
import flask
import logging
import json
import yaml
import threading
import re
from flask import request
import openai
from time import time, sleep
import chromadb
from chromadb.config import Settings
from uuid import uuid4



log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = flask.Flask('KB Articles')

# ChromaDB setup
persist_directory = "chromadb"
chroma_client = chromadb.Client(Settings(persist_directory=persist_directory,chroma_db_impl="duckdb+parquet",))
collection = chroma_client.get_or_create_collection(name="knowledge_base")

###     file operations

def clean_filename(filename):
    # Remove invalid characters from the filename
    valid_chars = r"[^a-zA-Z0-9_.-]"
    cleaned_filename = re.sub(valid_chars, "", filename)
    return cleaned_filename

def save_yaml(filepath, data):
        print('save_yaml: ', filepath, data)
        with open(filepath, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, allow_unicode=True)

def open_yaml(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data

def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()



###     chatbot functions



# def chatbot(messages, model="gpt-4-0613", temperature=0):
# def chatbot(messages, model="gpt-3.5-turbo-0613", temperature=0):
#     openai.api_key = open_file('key_openai.txt')
def chatbot(messages, model="gpt35turbo16k", temperature=0):
    openai.api_key = open_file("key_openai_azure.txt")
    openai.api_base = open_file(
        "endpoint_openai_azure.txt"
    )  # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
    openai.api_type = "azure"
    openai.api_version = "2023-05-15"  # this may change in the future
    max_retry = 7
    retry = 0
    while True:
        try:
            response = openai.ChatCompletion.create(engine=model, messages=messages, temperature=temperature)
            text = response['choices'][0]['message']['content']
            return text, response['usage']['total_tokens']
        except Exception as oops:
            print(f'\n\nError communicating with OpenAI: "{oops}"')
            if 'maximum context length' in str(oops):
                a = messages.pop(1)
                print('\n\n DEBUG: Trimming oldest message')
                continue
            retry += 1
            if retry >= max_retry:
                print(f"\n\nExiting due to excessive errors in API: {oops}")
                exit(1)
            print(f'\n\nRetrying in {2 ** (retry - 1) * 5} seconds...')
            sleep(2 ** (retry - 1) * 5)



###     KB functions



def update_directory():
    kb_dir = 'kb/'
    directory = ''
    for filename in os.listdir(kb_dir):
        if filename.endswith('.yaml'):
            filepath = os.path.join(kb_dir, filename)
            kb = open_yaml(filepath)
            directory += '\n%s - %s - %s - %s\n' % (filename, kb['title'], kb['description'], kb['keywords'])
    save_file('directory.txt', directory.strip())



def search_kb(query):
    directory = open_file('directory.txt')
    system = open_file('system_search.txt').replace('<<DIRECTORY>>', directory)
    messages = [{'role': 'user', 'content': query}, {'role': 'system', 'content': system}]
    response, tokens = chatbot(messages)
    print('search_kb response: ', response)
    jsonResponse = json.loads(response)
    if "results" in jsonResponse:
        return jsonResponse['results']
        
    return jsonResponse

def search_kb_chromadb(query):
    results = collection.query(query_texts=[query], n_results=5)
    
    test = results['metadatas'][0]
    print('article found: ', test)
    distance = results["distances"][0][0]
    print('distance: ', distance)
    if (distance > 1):
        filenames = ""
    else:
        kb_metadata = results['metadatas'][0]
        filenames = [item['filename'] for item in kb_metadata]
        
    return filenames



def create_article(text):
    print('Creating article...')
    system = open_file('system_create.txt')
    messages = [{'role': 'system', 'content': system}, {'role': 'user', 'content': text}]
    response, tokens = chatbot(messages)  # response should be JSON string
    
    kb = json.loads(response)
    kb['id'] = str(uuid4())
    # Extract the title property from the JSON object
    title = kb.get('title', 'default')

    # Clean the title to create a valid filename
    filename = clean_filename(title)

    # Update the title property with the new filename
    kb['title'] = filename
    
    filenameWithExtension = '%s.yaml' % kb['title']

    save_yaml('kb/%s.yaml' % kb['title'], kb)

    # add to chroma db 
    collection.add(documents=[kb['body']],ids=[kb['id']],metadatas=[{"filename": filenameWithExtension}])

    # chroma_client.persist()


def update_article(payload):
    kb = open_yaml('kb/%s.yaml' % payload['title'])
    json_str = json.dumps(kb, indent=2)
    system = open_file('system_update.txt').replace('<<KB>>', json_str)
    messages = [{'role': 'system', 'content': system}, {'role': 'user', 'content': payload['input']}]
    response, tokens = chatbot(messages)  # response should be JSON string
    kb_updated = json.loads(response)
    kb_updated['id'] = kb['id']
    save_yaml('kb/%s.yaml' % kb_updated['title'], kb_updated)
    filenameWithExtension = '%s.yaml' % kb_updated['title']
    # Update 
    collection.update(documents=[kb_updated['body']],ids=[kb_updated['id']],metadatas=[{"filename": filenameWithExtension}])


###     flask routes



@app.route('/search', methods=['post'])
def search_endpoint():
    update_directory()
    payload = request.json  # payload should be {"query": "{query}"}
    print(payload)
    files = search_kb(payload['query'])  # this will always be a list of files, though it may be empty
    print('Files: ', files)
    result = list()
    for f in files:
        data = open_yaml(f'kb/{f}')
        result.append(data)
    return flask.Response(json.dumps(result), mimetype='application/json')

@app.route('/searchChromaDB', methods=['post'])
def searchChromaDb_endpoint():
    # update_directory()
    payload = request.json  # payload should be {"query": "{query}"}
    print(payload)
    files = search_kb_chromadb(payload['query'])  # this will always be a list of files, though it may be empty
    print('Files: ', files)
    result = list()
    for f in files:
        print("File: ", f)
        data = open_yaml(f'kb/{f}')
        result.append(data)
    return flask.Response(json.dumps(result), mimetype='application/json')



@app.route('/create', methods=['post'])
def create_endpoint():
    payload = request.json  # payload should be {"input": "{text}"}
    threading.Thread(target=create_article, args=(payload['input'],)).start()
    # threading.Thread(target=create_article, args=(payload,)).start()
    return flask.Response(json.dumps({"status": "success"}), mimetype='application/json')



@app.route('/update', methods=['post'])
def update_endpoint():
    payload = request.json  # payload should be {"title": "{KB title to update}", "input": "{text}"}
    threading.Thread(target=update_article, args=(payload,)).start()
    return flask.Response(json.dumps({"status": "success"}), mimetype='application/json')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=999)