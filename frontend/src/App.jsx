import { useState } from 'react';
import React from 'react';

function App() {
  const [url, setUrl] = useState('');
  const [reviewsCount, setReviewsCount] = useState(50);
  const [analysis, setAnalysis] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    setAnalysis('');
    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: url,
          reviews_count: parseInt(reviewsCount),
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

  return (
    <div className="text-center">
      <header className="bg-gray-800 min-h-screen flex flex-col items-center justify-center text-white text-lg">
        <h1 className="text-5xl font-bold mb-4">Google Maps Reviews Analyzer</h1>
        <p className="text-center max-w-4xl mx-auto mb-8 px-4">
            This tool scrapes Google Maps reviews for a given URL, filters them for complaints, and performs an analysis to identify common issues.
        </p>
        <div className="flex flex-col items-center mb-5">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter Google Maps URL"
            className="p-3 text-base w-full max-w-lg mb-5 rounded-lg border border-gray-300 bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <div className="flex flex-col items-center mb-5">
            <label htmlFor="reviews-count" className="mb-2">Number of reviews: {reviewsCount}</label>
            <input
              type="range"
              id="reviews-count"
              min="0"
              max="1000"
              value={reviewsCount}
              onChange={(e) => setReviewsCount(e.target.value)}
              className="w-80"
            />
          </div>
          <button 
            onClick={handleAnalyze} 
            disabled={loading} 
            className="px-5 py-3 text-lg cursor-pointer rounded-lg border border-transparent bg-gray-700 text-white hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Analyzing...' : 'Analyze Reviews'}
          </button>
        </div>
        {analysis && (
          <div className="mt-5 text-left whitespace-pre-wrap bg-gray-700 p-5 rounded-lg w-4/5 max-w-4xl">
            <h2 className="text-2xl font-bold mb-4">Analysis Results</h2>
            <pre className="text-sm">{analysis}</pre>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
