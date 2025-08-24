import feedparser
import re


def get_xkcd_panel():
    feed = feedparser.parse("https://xkcd.com/atom.xml")
    try:
        element = feed.entries[0].description
    except IndexError:
        raise RuntimeError("Failed to retrieve latest comic.")

    return {
        "url": re.search(r'<img[^>]+src=["\']([^"\']+)["\']', element).group(1),
        "title": feed.entries[0].title,
        "caption": re.search(r'<img[^>]+alt=["\']([^"\']+)["\']', element).group(1),
    }


def get_cnh_panel():
    feed = feedparser.parse("https://explosm-1311.appspot.com/")
    try:
        element = feed.entries[0].description
    except IndexError:
        raise RuntimeError("Failed to retrieve latest comic.")

    return {
        "url": re.search(r'<img[^>]+src=["\']([^"\']+)["\']', element).group(1),
        "title": feed.entries[0].title.split(" - ")[1].strip(),
        "caption": "",
    }


def get_smbc_panel():
    feed = feedparser.parse("http://www.smbc-comics.com/comic/rss")
    try:
        element = feed.entries[0].description
    except IndexError:
        raise RuntimeError("Failed to retrieve latest comic.")

    return {
        "url": re.search(r'<img[^>]+src=["\']([^"\']+)["\']', element).group(1),
        "title": feed.entries[0].title.split("-")[1].strip(),
        "caption": re.search(r'Hovertext:<br />(.*?)</p>', element).group(1),
    }


def get_pbf_panel():
    feed = feedparser.parse("https://pbfcomics.com/feed/")
    try:
        element = feed.entries[0].description
    except IndexError:
        raise RuntimeError("Failed to retrieve latest comic.")

    return {
        "url": re.search(r'<img[^>]+src=["\']([^"\']+)["\']', element).group(1),
        "title": feed.entries[0].title,
        "caption": re.search(r'<img[^>]+alt=["\']([^"\']+)["\']', element).group(1),
    }


def get_qc_panel():
    feed = feedparser.parse("http://www.questionablecontent.net/QCRSS.xml")
    try:
        element = feed.entries[0].description
    except IndexError:
        raise RuntimeError("Failed to retrieve latest comic.")

    return {
        "url": re.search(r'<img[^>]+src=["\']([^"\']+)["\']', element).group(1),
        "title": "",
        "caption": "",
    }


def get_pdl_panel():
    feed = feedparser.parse("https://poorlydrawnlines.com/feed/")
    try:
        element = feed.entries[0].get('content', [{}])[0].get('value', '')
    except IndexError:
        raise RuntimeError("Failed to retrieve latest comic.")

    return {
        "url": re.search(r'<img[^>]+src=["\']([^"\']+)["\']', element).group(1),
        "title": feed.entries[0].title,
        "caption": "",
    }


def get_dinosaur_comics_panel():
    feed = feedparser.parse("https://www.qwantz.com/rssfeed.php")
    try:
        element = feed.entries[0].description
    except IndexError:
        raise RuntimeError("Failed to retrieve latest comic.")

    return {
        "url": re.search(r'<img[^>]+src=["\']([^"\']+)["\']', element).group(1),
        "title": feed.entries[0].title,
        "caption": re.search(r'title="(.*?)" />', element).group(1),
    }


COMICS = {
    "XKCD": get_xkcd_panel,
    "Cyanide & Happiness": get_cnh_panel,
    "Saturday Morning Breakfast Cereal": get_smbc_panel,
    "The Perry Bible Fellowship": get_pbf_panel,
    "Questionable Content": get_qc_panel,
    "Poorly Drawn Lines": get_pdl_panel,
    "Dinosaur Comics": get_dinosaur_comics_panel,
}
