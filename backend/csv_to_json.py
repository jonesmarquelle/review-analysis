#!/usr/bin/env python3
"""
CSV to JSON Converter for Google Maps Reviews Data
Converts reviews.csv to reviews.json format
"""

import csv
import json
import sys
from pathlib import Path


def csv_to_json(csv_file_path, json_file_path=None):
    """
    Convert CSV file to JSON format
    
    Args:
        csv_file_path (str): Path to input CSV file
        json_file_path (str): Path to output JSON file (optional)
    
    Returns:
        str: Path to the created JSON file
    """
    csv_path = Path(csv_file_path)
    
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_file_path}")
    
    # Set default output path if not provided
    if json_file_path is None:
        json_file_path = csv_path.with_suffix('.json')
    else:
        json_file_path = Path(json_file_path)
    
    reviews_data = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            # Use csv.DictReader to automatically handle headers
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                # Convert numeric fields to appropriate types
                processed_row = {}
                for key, value in row.items():
                    # Convert rating to float
                    if key == 'rating':
                        try:
                            processed_row[key] = float(value) if value and value.strip() else None
                        except ValueError:
                            processed_row[key] = None
                    # Convert n_review_user and n_photo_user to int
                    elif key in ['n_review_user', 'n_photo_user']:
                        try:
                            processed_row[key] = int(value) if value and value.strip() else 0
                        except ValueError:
                            processed_row[key] = 0
                    # Keep other fields as strings
                    else:
                        processed_row[key] = value if value and value.strip() else None
                
                reviews_data.append(processed_row)
        
        # Write JSON file
        with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(reviews_data, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"Successfully converted {csv_path} to {json_file_path}")
        print(f"Converted {len(reviews_data)} reviews")
        
        return str(json_file_path)
        
    except Exception as e:
        print(f"Error converting CSV to JSON: {e}")
        raise


def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) < 2:
        print("Usage: python csv_to_json.py <csv_file> [json_file]")
        print("Example: python csv_to_json.py data/reviews.csv data/reviews.json")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    json_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        output_file = csv_to_json(csv_file, json_file)
        print(f"Conversion completed successfully!")
        print(f"Output file: {output_file}")
    except Exception as e:
        print(f"Conversion failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
