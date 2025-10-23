// Google Maps configuration
// The API key is loaded from environment variables
// Make sure to set VITE_GOOGLE_MAPS_API_KEY in your .env file
export const GOOGLE_MAPS_API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || 'YOUR_GOOGLE_MAPS_API_KEY_HERE';

// Validate that the API key is set
if (!GOOGLE_MAPS_API_KEY || GOOGLE_MAPS_API_KEY === 'YOUR_GOOGLE_MAPS_API_KEY_HERE') {
  console.error('Google Maps API key not configured properly!');
  console.error('Please set NEXT_PUBLIC_GOOGLE_MAPS_API_KEY in your .env file');
  console.error('Current value:', GOOGLE_MAPS_API_KEY);
} else {
  console.log('Google Maps API key is configured');
}

// Make sure to enable the following APIs in your Google Cloud Console:
// - Maps JavaScript API
// - Places API
// - Geocoding API

export const ANALYSIS_API_ENDPOINT = process.env.NEXT_PUBLIC_ANALYSIS_API_ENDPOINT || 'http://localhost:5000/analyze';