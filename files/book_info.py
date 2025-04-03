import requests


# def string_compare(str1, str2):
#     """EXPERIMENTAL: Implementation of Levenshtein distance algorithm between given string text and self.title.
#     More info: https://en.wikipedia.org/wiki/Levenshtein_distance
#     Using it might lead to memory issues."""
#     print("Comparing strings:", str1, str2)
#     str1 = str1.lower()
#     str2 = str2.lower()
#     len_a = len(str1)
#     len_b = len(str2)
#     if len_a == 0:
#         return len_b
#     elif len_b == 0:
#         return len_a
#     elif str1[0] == str2[0]:
#         return string_compare(str1[1:], str2[1:])
#     else:
#         distance = min(string_compare(str1[1:], str2), string_compare(str1, str2[1:]))
#         distance = min(distance, string_compare(str1[1:], str2[1:]))
#         print(f"return {1+distance}")
#         return 1 + distance

class BookInfo:
    def __init__(self, title, language=''):
        self.title = title.replace('-', '+')
        self.author = ""
        self.isbn = ""
        self.description = ""
        self.language = language
        self.read_data()

    def read_data(self):
        if self.language:
            url = f"https://www.googleapis.com/books/v1/volumes?q={self.title}&langRestrict={self.language}"
            print(url)
        else:
            url = f"https://www.googleapis.com/books/v1/volumes?q=+intitle:{self.title}"
        response = requests.get(url)

        books = []
        for item in response.json()["items"]:
            title = item['volumeInfo']['title']
            subtitle = item['volumeInfo'].get('subtitle') if item['volumeInfo'].get('subtitle') else ""
            authors = item['volumeInfo'].get('authors') if item['volumeInfo'].get('authors') else ""
            publishedDate = item['volumeInfo'].get('publishedDate') if item['volumeInfo'].get('publishedDate') else ""
            book = {'title': title, 'subtitle': subtitle, 'authors': authors, 'publishedDate': publishedDate}
            books.append(book)

        #EXPERIMENTAL: Sorting books in similarity order
        #books.sort(key=lambda x: string_compare(self.title, x['title'] + " " + x['subtitle']))
        #string_compare('kitten', 'sitting')
        return books

