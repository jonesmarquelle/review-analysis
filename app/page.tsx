'use client';

import { useState } from 'react';

import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import {APIProvider, Map, MapMouseEvent} from '@vis.gl/react-google-maps';

import {GOOGLE_MAPS_API_KEY, ANALYSIS_API_ENDPOINT} from './config/maps';

import BusinessInfoCard from '../components/BusinessInfoCard';
import getPlaceDetails from '../components/PlaceSeach';

export default function Home() {
  const [url, setUrl] = useState('');
  const [reviewsCount, setReviewsCount] = useState(10);
  const [analysis, setAnalysis] = useState('');
  const [businessInfo, setBusinessInfo] = useState<google.maps.places.Place | null>(null);
  const [loading, setLoading] = useState(false);
  const [selectedLocation, setSelectedLocation] = useState<any>(null);
  const [inputMethod, setInputMethod] = useState('url'); // 'url' or 'map'

  const handleAnalyze = async () => {
    setLoading(true);
    setAnalysis('');
    
    // Determine which URL to use based on input method
    const targetUrl = inputMethod === 'url' ? url : selectedLocation;
    
    if (!targetUrl) {
      setAnalysis('Please provide a Google Maps URL or select a location on the map.');
      setLoading(false);
      return;
    }
    
    try {
      const response = await fetch(ANALYSIS_API_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: targetUrl,
          reviews_count: reviewsCount,
        }),
      });
      const data = await response.json();
      setAnalysis(data.analysis);
    } catch (error) {
      console.error('Error analyzing reviews:', error);
      setAnalysis('Failed to analyze reviews. Please check the console for details.');
    } finally {
      setLoading(false);
    }
  };

  const handleMapClick = async (event: MapMouseEvent) => {
    setInputMethod('map');

    const placeDetails = await getPlaceDetails(event.detail.placeId);
    console.log('Place Name:', placeDetails?.displayName);
    console.log('Place Address:', placeDetails?.formattedAddress);
    console.log('PlaceID:', placeDetails?.id);
    console.log('Place URL:', placeDetails?.googleMapsURI);

    setSelectedLocation(placeDetails?.googleMapsURI ?? null);
    setBusinessInfo(placeDetails ?? null);
  };

  return (
    <div className="text-center min-h-screen bg-gray-800">
      <div className="min-h-screen py-10 flex flex-col items-center justify-center">
      <header className="bg-gray-800 min-h-screen flex flex-col items-center justify-center text-white text-lg">
        <h1 className="text-5xl font-bold mb-4">Google Maps Reviews Analyzer</h1>
        <p className="text-center max-w-4xl mx-auto mb-8 px-4">
            This tool scrapes Google Maps reviews for a given URL, filters them for complaints, and performs an analysis to identify common issues.
        </p>
        <div className="flex flex-col items-center mb-5 w-full max-w-4xl">
          {/* Input Method Tabs */}
          <div className="flex mb-5 bg-gray-700 rounded-lg p-1">
            <button
              onClick={() => setInputMethod('url')}
              className={`px-4 py-2 rounded-md transition-colors ${
                inputMethod === 'url' 
                  ? 'bg-blue-600 text-white' 
                  : 'text-gray-300 hover:text-white'
              }`}
            >
              Enter URL
            </button>
            <button
              onClick={() => setInputMethod('map')}
              className={`px-4 py-2 rounded-md transition-colors ${
                inputMethod === 'map' 
                  ? 'bg-blue-600 text-white' 
                  : 'text-gray-300 hover:text-white'
              }`}
            >
              Select on Map
            </button>
          </div>

          {/* URL Input Method */}
          {inputMethod === 'url' && (
            <div className="w-full max-w-lg">
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Enter Google Maps URL"
                className="p-3 text-base w-full mb-5 rounded-lg border border-gray-300 bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          )}

          {/* Map Selection Method */}
          {inputMethod === 'map' && (
            <div className="w-full max-w-4xl mb-5 h-96">
              <APIProvider apiKey={GOOGLE_MAPS_API_KEY}>
                <Map
                  defaultZoom={3}
                  defaultCenter={{lat: 22.54992, lng: 0}}
                  gestureHandling={'greedy'}
                  disableDefaultUI={true}
                  onClick={handleMapClick}
                />
              </APIProvider>
            </div>
          )}

          {/* Reviews Count Slider */}
          <div className="flex flex-col items-center mb-5">
            <label htmlFor="reviews-count" className="mb-2">Number of reviews to analyze: {reviewsCount}</label>
            <input
              type="range"
              id="reviews-count"
              min="10"
              max="50"
              value={reviewsCount}
              onChange={(e) => setReviewsCount(parseInt(e.target.value))}
              className="w-80"
            />
          </div>

          {/* Analyze Button */}
          <button 
            onClick={handleAnalyze} 
            disabled={loading || (!url && !selectedLocation)} 
            className="px-5 py-3 text-lg cursor-pointer rounded-lg border shadow-lg border-transparent bg-gray-700 text-white hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Analyzing...' : 'Analyze Reviews'}
          </button>
        </div>

        {businessInfo && (
          <BusinessInfoCard 
            businessInfo={businessInfo} 
          />
        )}

        {analysis && (
          <div className="mt-5 text-left bg-gray-700 p-5 rounded-lg w-4/5 max-w-4xl shadow-lg">
            <h2 className="text-2xl font-bold mb-4">Analysis Results</h2>
            <div className="text-sm prose prose-invert max-w-none">
              <ReactMarkdown rehypePlugins={[rehypeRaw]}>{analysis}</ReactMarkdown>
            </div>
          </div>
        )}
      </header>
      </div>
    </div>
  );
}
