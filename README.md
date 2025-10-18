# Google Maps Scraper

This project scrapes Google Maps reviews, preprocesses them, and analyzes them for common complaints using Gemini AI. It also provides a simple desktop-like frontend to interact with the scripts.

## Project Structure

- `backend/`: Contains all the Python scripts for scraping, preprocessing, and analysis, as well as the FastAPI backend.
- `frontend/`: Contains the React frontend application.

## Setup and Installation

### Backend

1.  Navigate to the `backend` directory:
    ```sh
    cd backend
    ```
2.  Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```
3.  Set up your Gemini API key by creating a `.env` file in the `backend` directory with the following content:
    ```
    GEMINI_API_KEY=your_api_key
    ```

### Frontend

1.  Navigate to the `frontend` directory:
    ```sh
    cd frontend
    ```
2.  Install the required npm packages:
    ```sh
    npm install
    ```

## Running the Application

### Backend

1.  Navigate to the `backend` directory:
    ```sh
    cd backend
    ```
2.  Run the FastAPI server:
    ```sh
    uvicorn main:app --reload
    ```
The backend server will be running at `http://localhost:8000`.

### Frontend

1.  Navigate to the `frontend` directory:
    ```sh
    cd frontend
    ```
2.  Run the React application:
    ```sh
    npm run dev
    ```
The frontend application will be running at `http://localhost:5173`.

## Usage

1.  Open your browser and navigate to the frontend application (usually `http://localhost:5173`).
2.  Enter a Google Maps URL in the text box.
3.  Use the slider to select the number of reviews to pull.
4.  Click the "Analyze Reviews" button to start the analysis.
5.  The analysis results will be displayed on the page.
