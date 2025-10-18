import { useState } from 'react';
import './App.css';

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
    <div className="App">
      <header className="App-header">
        <h1>Google Maps Reviews Analyzer</h1>
        <div className="input-container">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter Google Maps URL"
            className="url-input"
          />
          <div className="slider-container">
            <label htmlFor="reviews-count">Number of reviews: {reviewsCount}</label>
            <input
              type="range"
              id="reviews-count"
              min="0"
              max="100"
              value={reviewsCount}
              onChange={(e) => setReviewsCount(e.target.value)}
              className="slider"
            />
          </div>
          <button onClick={handleAnalyze} disabled={loading} className="analyze-button">
            {loading ? 'Analyzing...' : 'Analyze Reviews'}
          </button>
        </div>
        {analysis && (
          <div className="analysis-container">
            <h2>Analysis Results</h2>
            <pre>{analysis}</pre>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
