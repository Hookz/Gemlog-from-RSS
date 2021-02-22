# Gemlog-from-RSS
A simple RSS to Gemlog (Gemini log) converter. 

The original version is developed for [SPIP](https://www.spip.net/en_rubrique25.html), but I am going to also work on a
version for WordPress. 

## Usage (SPIP)
A working example for the SPIP version of this library can be ran
using the [example.py](example.py) class. It also allows for a quick preview of the code without having to go into
[gemlog_from_rss/examples.py](gemlog_from_rss/examples.py).

### (Main) file structure - minimum working code

To run this code the following structure is required:
```python
from gemlog_from_rss.spip import MainPage, Page
import xml.etree.ElementTree as ET
import shutil

from pathlib import Path
Path("resources").mkdir(parents=False, exist_ok=True)
main_page = MainPage(feed="https://url.to.feed")
Path(main_page.root).mkdir(parents=True, exist_ok=True)

tree = ET.parse("resources/all_posts.xml")
root = tree.getroot()
main_page.root = root

# Adding those pages is optional!
page = Page()
page.download_html("http://url.to.html.resource/file.html")
page.fetch_content()

page_2 = Page()
page_2.download_html("http://url.to.html.resource/file.html")
page_2.fetch_content()

main_page.add_page(page)
main_page.add_page(page_2)
# alternatively:
main_page.add_pages([page, page_2])

main_page.add_posts()

main_page.create_files()
with open(f"{main_page.root_dir}/index.gmi", "w") as f:
    f.write(main_page.make_main_page())

    # Remove temporary resources directory
try:
    shutil.rmtree('resources')
except OSError as e:
    print("Error: %s : %s" % ('resources', e.strerror))
```

### Running the server
To run the Gemini server, please use Gemini server software. 
This package doesn't come with a Gemini server, but I recommend [agate](https://github.com/mbrubeck/agate). 
It is super easy to install and run, and you can make this library work with it by outputting the articles and index.gmi
to a directory used by agate. 

Please make sure that the files outputted by *gemlog_from_rss* are either located in the root directory of your Gemini 
server or that they are linked to from your main Gemini page.

## Contributing and further development

This library **will** be developed further. If you want to contribute to development, please fork this repository
and start a pull request when you are ready to submit. 
