from fastapi import FastAPI
from pydantic import BaseModel
import os

from scraper import scrape_reviews
from csv_to_json import csv_to_json
from preprocess_reviews import preprocess_reviews
from analyze_complaints import analyze_complaints

app = FastAPI()

class AnalysisRequest(BaseModel):
    url: str
    reviews_count: int

@app.post("/analyze")
def analyze(request: AnalysisRequest):
    urls = [request.url]
    reviews_count = request.reviews_count

    # Define file paths
    reviews_csv = "data/reviews.csv"
    reviews_json = "data/reviews.json"
    filtered_reviews_json = "data/filtered_reviews.json"
    complaints_analysis_md = "data/complaints_analysis.md"
    sample_filter_terms = "sample_filter_terms.txt"

    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # 1. Scrape reviews
    scraped_csv = scrape_reviews(urls, reviews_count, outpath=reviews_csv, source=True)

    # 2. Convert CSV to JSON
    converted_json = csv_to_json(scraped_csv, reviews_json)

    # 3. Preprocess reviews
    preprocessed_json = preprocess_reviews(converted_json, sample_filter_terms, filtered_reviews_json)

    # 4. Analyze complaints
    analysis_result = analyze_complaints(preprocessed_json, complaints_analysis_md)

    return {"analysis": analysis_result}

@app.get("/")
def read_root():
    return {"message": "Google Maps Scraper API"}
