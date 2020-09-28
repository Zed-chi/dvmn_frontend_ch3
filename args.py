import argparse
from parse_tululu_category import (
    get_all_book_links_on_page,
    get_sfiction_list_books_page,
)

parser = argparse.ArgumentParser()
parser.add_argument("--start_page", default=1, type=int)
parser.add_argument("--end_page", type=int)
args = parser.parse_args()


def get_links_from_pages(start, end=None):
    links = []
    if end:
        for page_num in range(start, end):
            html = get_sfiction_list_books_page(page_num)
            links.extend(get_all_book_links_on_page(html))
    else:
        page_num = start
        while True:
            html = get_sfiction_list_books_page(page_num)
            if not html:
                break
            links.extend(get_all_book_links_on_page(html))
            page_num += 1
    return links


def main():
    start = args.start_page
    if not args.end_page:
        links = get_links_from_pages(start)
    elif args.end_page <= start:
        links = get_links_from_pages(start, start + 1)

    print(len(links))


if __name__ == "__main__":
    main()
