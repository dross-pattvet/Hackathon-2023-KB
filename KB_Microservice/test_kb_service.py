import os
import requests
import json
from pprint import pprint as pp



def test_create_endpoint():
    text = input("Enter the text for the new KB article: ")
    payload = {"input": text}
    response = requests.post("http://localhost:999/create", json=payload)
    print('\n\n\n', response.json())



def test_search_endpoint(useChromaDB):
    query = input("Enter the search query: ")
    payload = {"query": query}

    endpoint = "search"
    if (useChromaDB):
        endpoint = "searchChromaDB"
    url = f"http://localhost:999/{endpoint}"
    response = requests.post(url, json=payload)
    print('\n\n\n')
    response_json = response.json()
    pp(response_json)
    print('\nTotal: ', len(response_json))



def test_update_endpoint():
    title = input("Enter the title of the KB article to update: ")
    text = input("Enter the new text for the KB article: ")
    payload = {"title": title, "input": text}
    response = requests.post("http://localhost:999/update", json=payload)
    print('\n\n\n', response.json())

def test_mass_create():
    folder_path = input("Enter the folder path: ")
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):  # Process only text files
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = filename+'\n\n'+file.read()            
                payload = {"input": text}
                response = requests.post("http://localhost:999/create", json=payload)
                print('\n\n\n', filename)

def main():
    while True:
        print("\n\n\n1. Create KB article")
        print("2. Search KB articles")
        print("3. Update KB article")
        print("4. Mass Create KB article")
        print("5. Search KB articles (v2)")
        print("6. Exit")
        choice = input("\n\nEnter your choice: ")
        if choice == '1':
            test_create_endpoint()
        elif choice == '2':
            test_search_endpoint()
        elif choice == '3':
            test_update_endpoint()
        elif choice == '4':
            test_mass_create()
        elif choice == '5':
            test_search_endpoint(True)                        
        elif choice == '6':
            break                    
        else:
            print("\n\n\nInvalid choice. Please enter a number between 1 and 4.")




if __name__ == "__main__":
    main()