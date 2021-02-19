def spip_example():
    import xml.etree.ElementTree as ET
    from lxml.html import fromstring
    from lxml.etree import ParserError
    import argparse
    import requests
    import re
    from gemlog_from_rss.spip import MainPage, SinglePost, Page

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        default="",
        type=str,
        help="Local path on machine to output the *.gmi files to"
    )
    parser.add_argument(
        "--feed",
        default="",
        type=str,
        help="Feed to download the articles from"
    )

    args = parser.parse_args()

    main_page = MainPage(feed="http://lefaso.net/spip.php?page=backend")

    if main_page.feed is None:
        req = requests.get(str(args.feed))
        open('resources/all_posts.xml', 'wb').write(req.content)
    tree = ET.parse("resources/all_posts.xml")
    root = tree.getroot()
    main_page.root = root

    about_page = Page(content_class="article_content")
    about_page.download_html("https://lefaso.net/spip.php?article5736&rubrique17")
    about_page.fetch_content()

    main_page.add_page(about_page)

    main_page.add_posts()

    main_page.create_files()
    with open(f"{main_page.root_dir}/index.gmi", "w") as f:
        f.write(main_page.make_main_page())


def xml_example():
    return None
