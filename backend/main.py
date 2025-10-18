import os

def main():
    print("Starting scraper...")
    scrape_result = os.system("python3 scraper.py --o reviews.csv --sort_by lowest_rating --N 50 --source")
    if scrape_result != 0:
        print(f"Error: scraper.py failed with exit code {scrape_result}")
        return
    print("Scraper successfully completed")
    print("Reviews saved to data/reviews.csv")
    
    print("Starting CSV to JSON...")
    convert_result = os.system("python3 csv_to_json.py data/reviews.csv data/reviews.json")
    if convert_result != 0:
        print(f"Error: csv_to_json.py failed with exit code {convert_result}")
        return
    print("CSV to JSON successfully completed")
    print("Reviews saved to data/reviews.json")

    print("Starting Preprocess reviews...")
    preprocess_result = os.system("python3 preprocess_reviews.py data/reviews.json sample_filter_terms.txt data/filtered_reviews.json")
    if preprocess_result != 0:
        print(f"Error: preprocess_reviews.py failed with exit code {preprocess_result}")
        return
    print("Preprocess reviews successfully completed")
    print("Filtered reviews saved to data/filtered_reviews.json")

    print("Starting Analyze complaints...")
    analyze_result = os.system("python3 analyze_complaints.py --input data/filtered_reviews.json --output data/complaints_analysis.md")
    if analyze_result != 0:
        print(f"Error: analyze_complaints.py failed with exit code {analyze_result}")
        return
    print("Analyze complaints successfully completed")
    print("Complaints analysis saved to data/complaints_analysis.md")

    print("All tasks successfully completed")

if __name__ == "__main__":
    main()
