def spip_example():
    import xml.etree.ElementTree as ET
    from pathlib import Path
    from gemlog_from_rss.spip import MainPage, Page
    import shutil

    Path("resources").mkdir(parents=False, exist_ok=True)

    main_page = MainPage(feed="http://lefaso.net/spip.php?page=backend")

    Path(main_page.root_dir).mkdir(parents=False, exist_ok=True)

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

    # Remove temporary resources directory
    try:
        shutil.rmtree('resources')
    except OSError as e:
        print("Error: %s : %s" % ('resources', e.strerror))


def xml_example():
    return None
