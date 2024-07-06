# Generated by Glenn Jocher (glenn.jocher@ultralytics.com) for https://github.com/ultralytics

import argparse
import time
from pathlib import Path

from flickrapi import FlickrAPI

from utils.general import download_uri

key = ""  # Flickr API key https://www.flickr.com/services/apps/create/apply
secret = ""


def get_urls(search="honeybees on flowers", n=10, download=False):
    """Fetch Flickr URLs for `search` term images, optionally downloading them; supports up to `n` images."""
    t = time.time()
    flickr = FlickrAPI(key, secret)
    license = ()  # https://www.flickr.com/services/api/explore/?method=flickr.photos.licenses.getInfo
    photos = flickr.walk(
        text=search,  # http://www.flickr.com/services/api/flickr.photos.search.html
        extras="url_o",
        per_page=500,  # 1-500
        license=license,
        sort="relevance",
    )

    if download:
        dir_path = Path.cwd() / "images" / search.replace(" ", "_")
        dir_path.mkdir(parents=True, exist_ok=True)

    urls = []
    for i, photo in enumerate(photos):
        if i <= n:
            try:
                url = photo.get("url_o")  # original size
                if url is None:
                    url = f"https://farm{photo.get('farm')}.staticflickr.com/{photo.get('server')}/{photo.get('id')}_{photo.get('secret')}_b.jpg"

                if download:
                    download_uri(url, dir_path)

                urls.append(url)
                print(f"{i}/{n} {url}")
            except Exception as e:
                print(f"{i}/{n} error...: {e}")

        else:
            print(f"Done. ({time.time() - t:.1f}s)" + (f"\nAll images saved to {dir_path}" if download else ""))
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--search", nargs="+", default=["honeybees on flowers"], help="flickr search term")
    parser.add_argument("--n", type=int, default=10, help="number of images")
    parser.add_argument("--download", action="store_true", help="download images")
    opt = parser.parse_args()

    print(f"nargs {opt.search}")
    help_url = "https://www.flickr.com/services/apps/create/apply"
    assert key and secret, f"Flickr API key required in flickr_scraper.py L11-12. To apply visit {help_url}"

    for search in opt.search:
        get_urls(search=search, n=opt.n, download=opt.download)
