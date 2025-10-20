#!/usr/bin/env python3
"""
Review Preprocessing Script

This script filters reviews based on specified words or phrases from a JSON file.
It reads filter terms from a text file and can either:
- Blacklist mode (default): Remove reviews containing those terms
- Whitelist mode (--whitelist): Keep only reviews containing those terms

Usage:
    python preprocess_reviews.py input.json filter_terms.txt output.json
    python preprocess_reviews.py input.json filter_terms.txt output.json --whitelist
    python preprocess_reviews.py --help
"""

import json
import argparse
import sys
import os
from typing import List, Dict, Any


def load_filter_terms(filter_file: str) -> List[str]:
    """
    Load filter terms from a text file.
    
    Args:
        filter_file: Path to the text file containing filter terms
        
    Returns:
        List of filter terms (stripped of whitespace)
    """
    try:
        with open(filter_file, 'r', encoding='utf-8') as f:
            terms = [line.strip() for line in f if line.strip()]
        return terms
    except FileNotFoundError:
        print(f"Error: Filter file '{filter_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading filter file: {e}")
        sys.exit(1)


def load_reviews(input_file: str) -> List[Dict[str, Any]]:
    """
    Load reviews from a JSON file.
    
    Args:
        input_file: Path to the JSON file containing reviews
        
    Returns:
        List of review dictionaries
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reviews = json.load(f)
        return reviews
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)


def contains_filter_terms(text: str, filter_terms: List[str], case_sensitive: bool = False) -> bool:
    """
    Check if text contains any of the filter terms.
    
    Args:
        text: Text to search in
        filter_terms: List of terms to search for
        case_sensitive: Whether to perform case-sensitive matching
        
    Returns:
        True if any filter term is found, False otherwise
    """
    if not text:
        return False
    
    search_text = text if case_sensitive else text.lower()
    
    for term in filter_terms:
        search_term = term if case_sensitive else term.lower()
        if search_term in search_text:
            return True
    
    return False


def filter_reviews(reviews: List[Dict[str, Any]], filter_terms: List[str], 
                  case_sensitive: bool = False, text_field: str = 'caption', 
                  whitelist: bool = False) -> List[Dict[str, Any]]:
    """
    Filter reviews based on specified terms.
    
    Args:
        reviews: List of review dictionaries
        filter_terms: List of terms to filter by
        case_sensitive: Whether to perform case-sensitive matching
        text_field: Field name containing the review text
        whitelist: If True, keep only reviews containing terms; if False, exclude reviews containing terms
        
    Returns:
        List of filtered reviews
    """
    filtered_reviews = []
    excluded_count = 0
    
    for review in reviews:
        review_text = review.get(text_field, '') or ''
        contains_terms = contains_filter_terms(review_text, filter_terms, case_sensitive)
        
        if whitelist:
            # Whitelist mode: keep only reviews that contain the terms
            if contains_terms:
                filtered_reviews.append(review)
            else:
                excluded_count += 1
                preview_text = review_text[:100] if review_text else "[No text content]"
                print(f"Excluded review (not in whitelist): {preview_text}...")
        else:
            # Blacklist mode: exclude reviews that contain the terms
            if contains_terms:
                excluded_count += 1
                preview_text = review_text[:100] if review_text else "[No text content]"
                print(f"Excluded review (contains blacklisted terms): {preview_text}...")
            else:
                filtered_reviews.append(review)
    
    mode = "whitelist" if whitelist else "blacklist"
    print(f"\nFiltering complete ({mode} mode):")
    print(f"Original reviews: {len(reviews)}")
    print(f"Excluded reviews: {excluded_count}")
    print(f"Remaining reviews: {len(filtered_reviews)}")
    
    return filtered_reviews


def save_reviews(reviews: List[Dict[str, Any]], output_file: str) -> None:
    """
    Save filtered reviews to a JSON file.
    
    Args:
        reviews: List of review dictionaries to save
        output_file: Path to the output JSON file
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(reviews, f, indent=2, ensure_ascii=False)
        print(f"Filtered reviews saved to: {output_file}")
    except Exception as e:
        print(f"Error saving output file: {e}")
        sys.exit(1)


def preprocess_reviews(input_file, filter_file, output_file, case_sensitive=False, text_field='caption', preview=False, whitelist=False):
    # Validate input files exist
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)
    
    if not os.path.exists(filter_file):
        print(f"Error: Filter file '{filter_file}' does not exist. Skipping filter.")
        return input_file
    
    # Load filter terms
    print(f"Loading filter terms from: {filter_file}")
    filter_terms = load_filter_terms(filter_file)
    print(f"Loaded {len(filter_terms)} filter terms")
    
    # Load reviews
    print(f"Loading reviews from: {input_file}")
    reviews = load_reviews(input_file)
    print(f"Loaded {len(reviews)} reviews")
    
    # Filter reviews
    mode = "whitelist" if whitelist else "blacklist"
    print(f"Filtering reviews ({mode} mode)...")
    print(f"Case sensitive: {case_sensitive}")
    print(f"Text field: {text_field}")
    
    filtered_reviews = filter_reviews(reviews, filter_terms, case_sensitive, text_field, whitelist)
    
    # Save or preview results
    if preview:
        print(f"Preview mode - not saving to file")
        print(f"Would save {len(filtered_reviews)} reviews to: {output_file}")
    else:
        save_reviews(filtered_reviews, output_file)

    return output_file


def main():
    """Main function to handle command line arguments and execute filtering."""
    parser = argparse.ArgumentParser(
        description="Filter reviews containing specified words or phrases",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Blacklist mode (default): exclude reviews containing filter terms
  python preprocess_reviews.py data/reviews.json filter_terms.txt data/filtered_reviews.json
  
  # Whitelist mode: keep only reviews containing filter terms
  python preprocess_reviews.py data/reviews.json filter_terms.txt data/filtered_reviews.json --whitelist
  
  # Case-sensitive filtering
  python preprocess_reviews.py data/reviews.json filter_terms.txt data/filtered_reviews.json --case-sensitive
  
  # Preview mode
  python preprocess_reviews.py data/reviews.json filter_terms.txt data/filtered_reviews.json --preview
        """
    )
    
    parser.add_argument('input_file', help='Path to input JSON file containing reviews')
    parser.add_argument('filter_file', help='Path to text file containing filter terms (one per line)')
    parser.add_argument('output_file', help='Path to output JSON file for filtered reviews')
    parser.add_argument('--case-sensitive', action='store_true', 
                       help='Perform case-sensitive matching (default: case-insensitive)')
    parser.add_argument('--text-field', default='caption', 
                       help='Field name containing review text (default: caption)')
    parser.add_argument('--preview', action='store_true',
                       help='Preview filtering without saving output file')
    parser.add_argument('--whitelist', action='store_true',
                       help='Whitelist mode: keep only reviews containing filter terms (default: blacklist mode)')
    
    args = parser.parse_args()
    
    preprocess_reviews(args.input_file, args.filter_file, args.output_file, args.case_sensitive, args.text_field, args.preview, args.whitelist)


if __name__ == "__main__":
    main()
