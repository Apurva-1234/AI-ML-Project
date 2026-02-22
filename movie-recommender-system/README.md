# Movie Recommender System 🎬

A content-based movie recommender system that suggests movies similar to the one selected by the user. The system uses a similarity matrix calculated from movie metadata (genres, keywords, cast, and crew) and fetches movie posters using the TMDb API.

##  Features
- **Accurate Recommendations**: Suggests top 5 similar movies based on content.
- **Visual Appeal**: Fetches and displays movie posters in real-time.
- **Interactive UI**: Simple and intuitive interface built with Streamlit.
- **Data-Driven**: Powered by the TMDb 5000 Movies Dataset.

## Tech Stack
- **Language**: Python
- **Frontend**: Streamlit
- **Data Analysis**: Pandas, NumPy
- **Machine Learning**: Scikit-learn (Cosine Similarity)
- **API**: TMDb API (for posters)

##  Project Structure
```text
movie-recommender-system/
├── Movie_Recomder_frontend/     # Streamlit application
│   ├── app.py                   # Main application script
│   ├── requirements.txt         # Python dependencies
│   ├── movie_dict.pkl          # Processed movie data
│   ├── similarity.pkl           # Pre-calculated similarity matrix
│   └── ...
├── tmdb_5000_movies.csv         # Raw movie dataset
├── tmdb_5000_credits.csv        # Raw credits dataset
└── movie-recommander-system.ipynb # Data processing & Model building notebook
```

## Getting Started

### Prerequisites
- Python 3.7 or higher
- A TMDb API Key (optional, a default one is included in `app.py`)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/movie-recommender-system.git
   cd movie-recommender-system
   ```

2. **Navigate to the frontend directory**:
   ```bash
   cd Movie_Recomder_frontend
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

1. **Start the Streamlit server**:
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**:
   The app will typically be available at `http://localhost:8501`.

##  How it Works
1. **Data Preprocessing**: The system processes the TMDb 5000 dataset, creating "tags" for each movie by combining genres, keywords, cast (top 3), and director.
2. **Vectorization**: Text data is converted into vectors using `CountVectorizer` (or similar techniques).
3. **Similarity Calculation**: Cosine similarity is used to calculate the distance between movie vectors.
4. **Recommendation**: When a user selects a movie, the system finds the top 5 movies with the highest similarity scores.

## License
This project is for educational purposes. Data provided by [TMDb](https://www.themoviedb.org/).

---

