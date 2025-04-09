#!/usr/bin/env python3
import signal
import sys
from urllib import request
import json
import os
import webbrowser

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
# This script fetches book details from Open Library API using a 13-digit ISBN number.
def fetch_book_details(isbn):
    url = f"http://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=details&format=json"
    with request.urlopen(url) as response:
        if response.status != 200:
            return f"HTTP Error: {response.status}"
        else:
            details = json.loads(response.read().decode())
            if details.get(f"ISBN:{isbn}"):
                return details[f"ISBN:{isbn}"]
            else:
                return {}

def display_book_value(isbn):
    url = f"https://isbnsearch.org/isbn/{isbn}"
    webbrowser.open(url, new=0)
    return

def print_book_details(book_details):
    if not book_details:
        print("!!WARNING!! No details found. Unable to print details.")
    else:
        print(f"Title: {book_details['details']['title']}")
        print(f"Author: {book_details['details']['authors'][0]['name']}")
        print(f"Publisher: {book_details['details']['publishers'][0]}")
        print(f"Classification: {book_details['details']['lc_classifications']}")
        save_book_details(book_details)
    
def save_book_details(book_details):
    if not book_details:
        print("!!WARNING!! No details found. Unable to save details.")
        return
    db_dir = WORKING_DIR
    file_path = f'{db_dir}/library.json'
    new_data = book_details
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f, indent=4) 
    
    with open(file_path, 'r+') as file:
        try:
            file_data = json.load(file)
        except json.JSONDecodeError:
            file_data = []
        if isinstance(file_data, list):
            file_data.append(new_data)
        elif isinstance(file_data, dict):
             if isinstance(new_data, list):
                for item in new_data:
                    file_data.update(item)
             elif isinstance(new_data, dict):
                file_data.update(new_data)

        file.seek(0)
        json.dump(file_data, file, indent=4)
        file.truncate()    

def get_input_from_user():
    isbn = input("Enter the 13-digit ISBN number: ")
    if len(isbn) != 13 or not isbn.isdigit():
        print("Please provide a valid 13-digit ISBN number.")
    return isbn

def signal_handler(sig, frame): 
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    print("Welcome to the book cataloger. \n\nPress Ctrl+C at anytime to exit the program.")
    
    while True:
        isbn = get_input_from_user()
        book_details = fetch_book_details(isbn)
        print_book_details(book_details)
        display_book_value(isbn)
        print("--------------------------------------------------------")

if __name__ == "__main__":
    main()