import os
import argparse
from utils import (
    get_text_from_url,
    get_book_details,
    get_id_from_book_url,
    download_image,
    download_txt,
    make_description,
)
from parse_tululu_category import (
    get_links_from_pages,
)


BASE_URL = "http://tululu.org"
BASE_BOOK_PAGE = "http://tululu.org/b"
BASE_TXT_URL = "http://tululu.org/txt.php?id="


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_page", default=1, type=int)
    parser.add_argument("--end_page", type=int)
    parser.add_argument("--dest_folder", default="./")
    parser.add_argument("--skip_imgs", action="store_true", default=False)
    parser.add_argument("--skip_txt", action="store_true", default=False)
    parser.add_argument("--json_path")
    return parser.parse_args()


def get_name_from_url_or_id(url, id):
    ext = url.split(".")[-1]
    if "nopic" in url:
        return f"nopic.{ext}"
    else:
        return f"{id}.{ext}"


def main():
    args = get_args()
    ###
    books_dir = os.path.join(args.dest_folder, "books")
    images_dir = os.path.join(args.dest_folder, "images")
    json_filepath = args.json_path or os.path.join(
        args.dest_folder, "books.json"
    )
    ###
    links = get_links_from_pages(args.start_page, args.end_page)
    description = []
    for id, link in enumerate(links):
        try:
            html = get_text_from_url(link, allow_redirects=True)
            details = get_book_details(html)
            if not args.skip_imgs:
                image_filename = get_name_from_url_or_id(
                    details["img_url"], id
                )
                details["img_src"] = os.path.normcase(
                    os.path.join(images_dir, image_filename)
                )
                download_image(from_=details["img_url"], to=details["img_src"])
            if not args.skip_txt:
                book_filename = f"{id}.{details['title']}.txt"
                details["book_path"] = os.path.normcase(
                    os.path.join(books_dir, book_filename)
                )
                txt_id = get_id_from_book_url(link)
                txt_link = f"{BASE_TXT_URL}{txt_id}"
                download_txt(from_=txt_link, to=details["book_path"])
            description.append(details)
        except Exception as e:
            print(e)
    make_description({"books": description}, json_filepath)


if __name__ == "__main__":
    main()
