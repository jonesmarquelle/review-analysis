# -*- coding: utf-8 -*-
from .googlemaps import GoogleMapsScraper
from datetime import datetime, timedelta
import argparse
import csv
from termcolor import colored
import time


ind = {'most_relevant' : 0 , 'newest' : 1, 'highest_rating' : 2, 'lowest_rating' : 3 }
HEADER = ['id_review', 'caption', 'relative_date', 'retrieval_date', 'rating', 'username', 'n_review_user', 'n_photo_user', 'url_user']
HEADER_W_SOURCE = ['id_review', 'caption', 'relative_date','retrieval_date', 'rating', 'username', 'n_review_user', 'n_photo_user', 'url_user', 'url_source']

def csv_writer(source_field, ind_sort_by, outpath):
    targetfile = open(outpath, mode='w', encoding='utf-8', newline='\n')
    writer = csv.writer(targetfile, quoting=csv.QUOTE_MINIMAL)

    if source_field:
        h = HEADER_W_SOURCE
    else:
        h = HEADER
    writer.writerow(h)

    return writer


def scrape_reviews(urls, n, outpath='output.csv', sort_by='lowest_rating', place=False, debug=False, source=False):
    writer = csv_writer(source, sort_by, outpath)
    ind_sort_by = ind[sort_by]

    with GoogleMapsScraper(debug=debug) as scraper:
        for url in urls:
            if place:
                print(scraper.get_account(url))
            else:
                error = scraper.sort_by(url, ind_sort_by)

                if error == 0:
                    count = 0
                    while count < n:
                        print(colored(f'[Review {count}]', 'cyan'))
                        reviews = scraper.get_reviews(count)
                        if not reviews:
                            break

                        for r in reviews:
                            row_data = list(r.values())
                            if source:
                                row_data.append(url.strip())
                            writer.writerow(row_data)
                        
                        count += len(reviews)
    return outpath

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Maps reviews scraper.')
    parser.add_argument('--N', type=int, default=100, help='Number of reviews to scrape')
    parser.add_argument('--i', type=str, default='urls.txt', help='target URLs file')
    parser.add_argument('--o', type=str, default='output.csv', help='output directory')
    parser.add_argument('--sort_by', type=str, default='lowest_rating', help='most_relevant, newest, highest_rating or lowest_rating')
    parser.add_argument('--place', dest='place', action='store_true', help='Scrape place metadata')
    parser.add_argument('--debug', dest='debug', action='store_true', help='Run scraper using browser graphical interface')
    parser.add_argument('--source', dest='source', action='store_true', help='Add source url to CSV file (for multiple urls in a single file)')
    parser.set_defaults(place=False, debug=False, source=False)

    args = parser.parse_args()

    # store reviews in CSV file
    with open(args.i, 'r') as urls_file:
        urls = [line.strip() for line in urls_file]
    
    scrape_reviews(urls, args.N, args.o, args.sort_by, args.place, args.debug, args.source)
