from bs4 import BeautifulSoup
import requests
import re
from lxml.html import fromstring
from lxml.etree import ParserError
from gemlog_from_rss.spip import SinglePost


def localize(lang):
    if lang == "pl":
        return {
            "our_articles": "Nasze artykuły"
        }
    if lang == "fr":
        return {
            "our_articles": "Nos articles"
        }
    else:
        return {
            "our_articles": "Our articles"
        }


class Page:
    def __init__(self, title=None, content_class="article-texte"):
        self.content = None
        self.url = None
        self.title = title
        self.content_class = content_class

    def download_html(self, url):
        self.url = url
        req = requests.get(self.url)
        open(f'resources/{self.url.split("/")[-1].split("?")[0]}.html', 'wb').write(req.content)

    def fetch_content(self):
        file_content = open(f'resources/{self.url.split("/")[-1].split("?")[0]}.html', 'r').read()\
            .replace("<strong>", "\n**").replace("</strong>", "**")
        soup = BeautifulSoup(file_content, 'html.parser')
        if self.title is None:
            self.title = soup.title.get_text()
        self.content = soup.find("div", class_=re.compile(self.content_class)).get_text().split("Credits")[0]

    def output_gemini(self):
        uit = f"""
##{self.title}

{self.content}
"""


class MainPage:
    def __init__(self, post_list=None, root_dir="blog", title=None, pages_list=None, feed=None, lang="en"):
        if post_list is None:
            post_list = []
        if pages_list is None:
            pages_list = []
        if root_dir[-1] == "/":
            root_dir = root_dir[:-1]
        self.post_list = post_list
        self.title = title
        self.root_dir = root_dir
        self.pages_list = pages_list
        self.feed = feed
        if self.feed is not None:
            self.parse_feed()
        if self.title is None:
            import xml.etree.ElementTree as ET
            self.title = ET.parse("resources/all_posts.xml").getroot()[0].find("title").text
        self.lang = lang
        self.dict = localize(lang)
        self.root = None

    def parse_feed(self):
        req = requests.get(self.feed)
        open("resources/all_posts.xml", "wb").write(req.content)
        return req.content

    def add_posts(self):
        for child in self.root[0].findall('item'):
            if child.find('{http://purl.org/rss/1.0/modules/content/}encoded') is not None:
                substituting = re.sub(' class=".*?"', '',
                                      child.find('{http://purl.org/rss/1.0/modules/content/}encoded').text)
                substituting = re.sub('<h3>', '\n### ', substituting)
                substituting = re.sub('</h3>', '\n', substituting)
                substituting = re.sub('<img.*?>', '', substituting)
                try:
                    self.post_list.append(SinglePost(
                        child.find("title").text,
                        fromstring(substituting).text_content(),
                        child.find('{http://purl.org/dc/elements/1.1/}creator').text,
                        child.find('{http://purl.org/dc/elements/1.1/}date').text.split("T")[0])
                    )
                except ParserError:
                    continue

    def create_files(self):
        for post in self.post_list:
            with open(f'{self.root_dir}/{post.link}', 'w') as f:
                f.write(post.get_gemini(blog_name=self.title))

    def add_page(self, page):
        self.pages_list.append(page)

    def add_pages(self, pages):
        for page in pages:
            self.add_page(page)

    def add_pages_to_main(self):
        content = f""
        for page in self.pages_list:
            content += f"## {page.title}\n\n" \
                       f"{page.content}\n\n"
        return content

    def make_main_page(self):
        content = f"""

# {self.title}

{self.add_pages_to_main()}
## {self.dict["our_articles"]}:

"""
        for post in self.post_list:
            content += f"=> {post.link} {post.title}\n\n"

        return content
