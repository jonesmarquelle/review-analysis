import { useState } from 'react';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [reviewsCount, setReviewsCount] = useState(50);
  const [analysis, setAnalysis] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    // I will implement the API call here in the next step
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
