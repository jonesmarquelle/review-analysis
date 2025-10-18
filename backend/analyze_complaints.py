#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to analyze Google Maps reviews and identify common complaints using Gemini AI.
"""

import json
import os
from google import genai
from google.genai.types import HttpOptions
import argparse
import sys
import dotenv

dotenv.load_dotenv()

def load_reviews(json_file_path):
    """Load reviews from JSON file."""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            reviews = json.load(f)
        print(f"Loaded {len(reviews)} reviews from {json_file_path}")
        return reviews
    except FileNotFoundError:
        print(f"Error: File {json_file_path} not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {json_file_path}: {e}")
        sys.exit(1)


def filter_reviews_with_text(reviews):
    """Filter reviews that have actual text content (not null captions)."""
    filtered_reviews = [review for review in reviews if review.get('caption') is not None]
    print(f"Found {len(filtered_reviews)} reviews with text content out of {len(reviews)} total reviews")
    return filtered_reviews


def create_analysis_prompt(reviews):
    """Create a comprehensive prompt for Gemini to analyze common complaints."""
    
    # Extract review text and ratings
    review_texts = []
    for review in reviews:
        caption = review.get('caption', '')
        rating = review.get('rating', 0)
        username = review.get('username', 'Anonymous')
        
        # Only include reviews with actual text
        if caption.strip():
            review_texts.append(f"Rating: {rating}/5 - {username}: {caption}")
    
    # Create the prompt
    prompt = f"""
Please analyze the following Google Maps reviews and identify the most common complaints, issues, or negative feedback patterns. 

Focus on:
1. Recurring problems mentioned across multiple reviews
2. Service quality issues
3. Communication problems
4. Pricing concerns
5. Technical issues
6. Any other patterns of dissatisfaction

Please provide a structured analysis with:
- A summary of the most common complaints
- Specific examples from the reviews
- Frequency/patterns you observe
- Any positive aspects that stand out

Here are the reviews to analyze:

{chr(10).join(review_texts)}

Please provide a comprehensive analysis of common complaints and issues.
"""
    
    return prompt


def analyze_with_gemini(prompt, api_key=None):
    """Send the prompt to Gemini for analysis."""
    try:
        # Initialize Gemini client
        if api_key:
            client = genai.Client(api_key=api_key, http_options=HttpOptions(api_version="v1"))
        else:
            # Get api key from environment variable
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                print("Error: GEMINI_API_KEY environment variable is not set")
                sys.exit(1)
            client = genai.Client(api_key=api_key, http_options=HttpOptions(api_version="v1"))
        
        print("Sending analysis request to Gemini...")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        
        return response.text
        
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None


def save_analysis(analysis_text, output_file):
    """Save the analysis results to a file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(analysis_text)
        print(f"Analysis saved to {output_file}")
    except Exception as e:
        print(f"Error saving analysis: {e}")


def main():
    parser = argparse.ArgumentParser(description='Analyze Google Maps reviews for common complaints using Gemini AI')
    parser.add_argument('--input', '-i', type=str, default='data/reviews.json', 
                       help='Path to the JSON file containing reviews (default: data/reviews.json)')
    parser.add_argument('--output', '-o', type=str, default='complaints_analysis.txt',
                       help='Output file for the analysis results (default: complaints_analysis.txt)')
    parser.add_argument('--api-key', type=str, default=None,
                       help='Gemini API key (if not set in environment)')
    parser.add_argument('--min-rating', type=int, default=1,
                       help='Minimum rating to include in analysis (default: 1, includes all reviews)')
    
    args = parser.parse_args()
    
    # Load reviews
    reviews = load_reviews(args.input)
    
    # Filter reviews with text content
    reviews_with_text = filter_reviews_with_text(reviews)
    
    if not reviews_with_text:
        print("No reviews with text content found. Exiting.")
        sys.exit(1)
    
    # Filter by minimum rating if specified
    if args.min_rating > 1:
        reviews_with_text = [r for r in reviews_with_text if r.get('rating', 0) <= args.min_rating]
        print(f"Filtered to {len(reviews_with_text)} reviews with rating <= {args.min_rating}")
    
    # Create analysis prompt
    prompt = create_analysis_prompt(reviews_with_text)
    
    # Analyze with Gemini
    analysis = analyze_with_gemini(prompt, args.api_key)
    
    if analysis:
        print("\n" + "="*80)
        print("GEMINI ANALYSIS RESULTS")
        print("="*80)
        print(analysis)
        print("="*80)
        
        # Save analysis
        save_analysis(analysis, args.output)
    else:
        print("Failed to get analysis from Gemini")
        sys.exit(1)


if __name__ == '__main__':
    main()

