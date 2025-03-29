import json

import requests


class BookInfo:
    def __init__(self, title):
        self.title = title.replace('-', '+')
        self.author = ""
        self.isbn = ""
        self.description = ""
        self.read_data()

    def read_data(self):
        print(type(self.title))
        url = "https://www.googleapis.com/books/v1/volumes?q=+intitle:" + self.title
        response = requests.get(url)
        return response.json()