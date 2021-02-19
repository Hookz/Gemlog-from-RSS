import random
import re


def localize(lang):
    if lang == "pl":
        return {
            "authors": "Autor(zy)",
            "title": "Tytuł",
            "date": "Data",
            "content": "Treść"
        }
    if lang == "fr":
        return {
            "authors": "Auteur(e)(s)",
            "title": "Titre",
            "date": "Date",
            "content": "Contenu"
        }
    else:
        return {
            "authors": "Author(s)",
            "title": "Title",
            "date": "Date",
            "content": "Content"
        }


class SinglePost:
    def __init__(self, title, content, author, date=None, lang="en"):
        self.lang = lang
        self.dict = localize(self.lang)
        self.title = title
        self.content = content
        self.date = date
        self.author = author
        self.link = f"{date}-{re.sub('[^a-zA-Z0-9-]', '', '-'.join(title.replace(' ','-').split('-')[0:5]))}.gmi"

    def print(self):
        print(f"{self.dict['title']}:", self.title)
        print(f"{self.dict['content']}:", self.content)
        print(f"{self.dict['date']}:", self.date)

    def get_gemini(self, blog_name=""):
        return f"""# {self.title} --- {self.date}

## {blog_name}
        
{self.dict['authors']}: {self.author}

{self.content}
"""
