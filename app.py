import requests
import os
import argparse
from utils import (
    save_image,
    print_book_details,
    get_output_filename,
    save_book,
    get_text_from_url,
    get_book_details,
    get_id_from_book_url,
    download_image,
    download_txt,
    make_description,
)
from parse_tululu_category import (
    get_all_book_links_on_page,
    get_sfiction_list_books_page,
    get_links_from_pages,
)


BASE_URL = "http://tululu.org"
BASE_BOOK_PAGE = "http://tululu.org/b"
BOOK_URL = "http://tululu.org/txt.php?id="


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_page", default=1, type=int)
    parser.add_argument("--end_page", type=int)
    parser.add_argument("--dest_folder", default="./")
    parser.add_argument("--skip_imgs", action="store_true", default=False)
    parser.add_argument("--skip_txt", action="store_true", default=False)
    parser.add_argument("--json_path")
    return parser.parse_args()


def download_10_books():
    for id in range(1, 11):
        download_txt_from_tululu_by_id(id)


def download_txt_from_tululu_by_id(id):
    book_url = f"{BOOK_URL}{id}"
    book_details_page = f"{BASE_BOOK_PAGE}{id}"
    txt = get_text_from_url(book_url)
    html = get_text_from_url(book_details_page, allow_redirects=True)
    info = get_book_details(html)
    if info and txt:
        filename = f"{id}.{info['title']}.txt"
        filepath = get_output_filename(filename)
        save_book(filepath, txt)
    print(f"{id} done")


def get_name_from_url_or_id(url, id):
    ext = url.split(".")[-1]
    if "nopic" in url:
        return f"nopic.{ext}"
    else:
        return f"{id}.{ext}"


def get_images_from_10_books():
    for id in range(1, 11):
        book_details_page = f"{BASE_BOOK_PAGE}{id}"
        html = get_text_from_url(book_details_page, allow_redirects=True)
        info = get_book_details(html)
        if not info or info["img_url"] is None:
            return None
        name = get_name_from_url_or_id(info["img_url"], id)
        res = requests.get(info["img_url"])
        if res.status_code == 200:
            print_book_details(info)
            save_image(os.path.join("./", name), res.content)


def download_100_books():
    books_path = os.path.join("./", "books")
    images_path = os.path.join("./", "images")
    links = []
    description = []
    for id in range(1, 5):
        html = get_sfiction_list_books_page(id)
        links.extend(get_all_book_links_on_page(html))
        print(f"Chunk {id} processed")
    for id, link in enumerate(links):
        html = get_text_from_url(link, allow_redirects=True)
        info = get_book_details(html)
        if "nopic" in info["img_url"]:
            name = "nopic"
        else:
            name = f"{id}"
        if requests.head(info["img_url"]).status_code == 200:
            ext = info["img_url"].split(".")[-1]
            image_filename = f"{name}.{ext}"
            book_filename = f"{id}.{info['title']}.txt"
            info["img_src"] = os.path.normcase(
                os.path.join(images_path, image_filename)
            )
            info["book_path"] = os.path.normcase(
                os.path.join(books_path, book_filename)
            )
            book_id = get_id_from_book_url(link)
            txt_link = f"{BOOK_URL}{book_id}"
            download_image(from_=info["img_url"], to=info["img_src"])
            download_txt(from_=txt_link, to=info["book_path"])
            description.append(info)
    make_description({"books": description})


def main():
    args = get_args()
    books_path = os.path.join(args.dest_folder, "books")
    images_path = os.path.join(args.dest_folder, "images")
    json_filepath = args.json_path or os.path.join(
        args.dest_folder, "books.json"
    )
    links = get_links_from_pages(args.start_page, args.end_page)
    description = []
    for id, link in enumerate(links):
        html = get_text_from_url(link, allow_redirects=True)
        info = get_book_details(html)
        if not args.skip_imgs:
            image_filename = get_name_from_url_or_id(info["img_url"], id)
            info["img_src"] = os.path.normcase(
                os.path.join(images_path, image_filename)
            )
            download_image(from_=info["img_url"], to=info["img_src"])
        if not args.skip_txt:
            book_filename = f"{id}.{info['title']}.txt"
            info["book_path"] = os.path.normcase(
                os.path.join(books_path, book_filename)
            )
            book_id = get_id_from_book_url(link)
            txt_link = f"{BOOK_URL}{book_id}"
            download_txt(from_=txt_link, to=info["book_path"])
        description.append(info)

    make_description({"books": description}, json_filepath)


if __name__ == "__main__":
    main()
