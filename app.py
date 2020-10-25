import argparse
import logging
import os

from xml.etree.ElementTree import ParseError

from parse_tululu_category import get_links_from_pages

from requests import HTTPError

from utils import (
    EmptyBookError,
    EmptyHTMLError,
    EmptyImageError,
    URLParseError,
    download_image,
    download_txt,
    get_book_details,
    get_id_from_book_url,
    get_text_from_url,
    make_description,
)

logging.basicConfig(level=logging.INFO)
BASE_URL = "https://tululu.org"
BASE_BOOK_PAGE = "https://tululu.org/b"
BASE_TXT_URL = "https://tululu.org/txt.php"


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_page", default=1, type=int)
    parser.add_argument("--end_page", type=int)
    parser.add_argument("--dest_folder", default="./")
    parser.add_argument("--skip_imgs", action="store_true", default=False)
    parser.add_argument("--skip_txt", action="store_true", default=False)
    parser.add_argument("--json_path")
    return parser.parse_args()


def get_name_from_url(url):
    return url.split("/")[-1]


def main():
    args = get_args()

    books_dir = os.path.join(args.dest_folder, "books")
    images_dir = os.path.join(args.dest_folder, "images")
    json_filepath = args.json_path or os.path.join(
        args.dest_folder,
        "books.json",
    )

    links = get_links_from_pages(args.start_page, args.end_page)
    description = []

    if not links:
        logging.warning("No files to download :(")
        return None
    else:
        logging.info(f"Going to download {len(links)} files...")

    for id, link in enumerate(links):
        try:
            html = get_text_from_url(link, allow_redirects=True)
            if not html:
                raise EmptyHTMLError("Book Page html is empty")
            details = get_book_details(html, link)

            if not args.skip_imgs:
                image_filename = get_name_from_url(details["img_url"])

                details["img_src"] = os.path.normcase(
                    os.path.join(images_dir, image_filename),
                )
                download_image(from_=details["img_url"], to=details["img_src"])

            if args.skip_txt:
                continue
            book_filename = f"{id}.{details['title']}.txt"
            details["book_path"] = os.path.normcase(
                os.path.join(books_dir, book_filename),
            )
            txt_id = get_id_from_book_url(link)
            if not txt_id:
                continue
            download_txt(
                from_=BASE_TXT_URL,
                to=details["book_path"],
                urlparams={"id": txt_id},
            )

            logging.info(f"File '{book_filename}' has been saved")
            description.append(details)

        except (
            HTTPError,
            ParseError,
            AttributeError,
            TypeError,
            ConnectionError,
            LookupError,
            FileExistsError,
            EmptyBookError,
            EmptyImageError,
            EmptyHTMLError,
            URLParseError,
        ) as e:
            logging.error(e)

    make_description({"books": description}, json_filepath)
    logging.info(f"Files are downloaded, description in {json_filepath}")


if __name__ == "__main__":
    main()
