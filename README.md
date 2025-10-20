# Google Maps Reviews Analyzer

A web application that allows you to analyze Google Maps reviews by either entering a URL directly or selecting a location on an interactive map.

## Features

- **Dual Input Methods**: Enter a Google Maps URL directly or select a location on an interactive map
- **Interactive Map**: Search for places and click to select locations
- **Review Analysis**: Scrapes and analyzes reviews to identify common complaints
- **Business Information**: Displays comprehensive business details

## Setup Instructions

### 1. Google Maps API Key Setup

To use the map functionality, you need to set up a Google Maps API key:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - **Maps JavaScript API**
   - **Places API**
   - **Geocoding API**
4. Create credentials (API Key)
5. Restrict the API key to your domain for security

### 2. Configure the API Key

1. Copy the example environment file:
   ```bash
   cd frontend
   cp .env.example .env
   ```

2. Open `/frontend/.env` and replace `YOUR_GOOGLE_MAPS_API_KEY_HERE` with your actual API key:
   ```env
   VITE_GOOGLE_MAPS_API_KEY=your-actual-api-key-here
   ```

   **Note**: The `.env` file is already included in `.gitignore` to keep your API key secure.

### 3. Install Dependencies

```bash
# Frontend dependencies
cd frontend
npm install

# Backend dependencies
cd ../backend
pip install -r requirements.txt
```

### 4. Run the Application

```bash
# Start the backend server
cd backend
python main.py

# Start the frontend development server (in a new terminal)
cd frontend
npm run dev
```

## Usage

1. **URL Method**: 
   - Click "Enter URL" tab
   - Paste a Google Maps business URL
   - Click "Analyze Reviews"

2. **Map Method**:
   - Click "Select on Map" tab
   - Search for a business or click anywhere on the map
   - Select the number of reviews to analyze
   - Click "Analyze Reviews"

## API Endpoints

- `POST /analyze` - Analyze reviews for a given URL
  - Body: `{"url": "string", "reviews_count": number}`
  - Returns: Analysis results and business information

## Technologies Used

- **Frontend**: React, Tailwind CSS, @vis.gl/react-google-maps
- **Backend**: FastAPI, Python
- **Maps**: Google Maps JavaScript API, Places API

## Environment Variables

The application uses environment variables for configuration:

- `VITE_GOOGLE_MAPS_API_KEY`: Your Google Maps API key (required for map functionality)

## Security Notes

- Always restrict your Google Maps API key to specific domains
- The `.env` file is automatically ignored by git to keep your API key secure
- Consider implementing rate limiting for production use
- The scraper respects Google's terms of service and implements delays between requests