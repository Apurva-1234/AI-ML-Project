import numpy as np 
import pandas as pd 
from config import DATA_PATH
import re 
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import nltk
import pickle


try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
print(f"Loaded {len(stop_words)} stopwords")


columns_names = ['target', 'id', 'date', 'flag', 'user', 'text']


print("Loading dataset...")
try:
    twitter_data = pd.read_csv(
        DATA_PATH, 
        encoding='ISO-8859-1', 
        names=columns_names,
        engine='python'
    )
except Exception as e:
    print(f"Error loading dataset: {e}")
    # Try alternative approach
    twitter_data = pd.read_csv(
        DATA_PATH, 
        encoding='latin-1', 
        names=columns_names,
        engine='python'
    )


print(f"Dataset shape: {twitter_data.shape}")
print(f"First few rows:\n{twitter_data.head()}")


print(f"Missing values:\n{twitter_data.isnull().sum()}")


print(f"Original target distribution:\n{twitter_data['target'].value_counts()}")


twitter_data.replace({'target': {4: 1}}, inplace=True)
print(f"Updated target distribution:\n{twitter_data['target'].value_counts()}")


port_stem = PorterStemmer()

def stemming(content):
    """Clean and stem text content"""
    if pd.isna(content):  
        return ""
    
    if not isinstance(content, str):
        content = str(content)
    
    # Remove non-alphabetic characters
    stemmed_content = re.sub('[^a-zA-Z]', ' ', content)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split()
    
    # Stem and remove stopwords
    stemmed_content = [
        port_stem.stem(word) 
        for word in stemmed_content 
        if word not in stop_words and len(word) > 2  # Remove very short words
    ]
    
    stemmed_content = ' '.join(stemmed_content)
    return stemmed_content


print("Applying stemming to text...")
twitter_data['stemmed_content'] = twitter_data['text'].apply(stemming)

twitter_data = twitter_data[twitter_data['stemmed_content'].str.strip() != '']
print(f"Dataset shape after removing empty content: {twitter_data.shape}")

# Display sample results
print(f"Sample stemmed content:\n{twitter_data['stemmed_content'].head()}")
print(f"Sample targets:\n{twitter_data['target'].head()}")

# Separate data and labels - ensure they're regular Python lists/numpy arrays
x = twitter_data['stemmed_content'].tolist()  # Convert to list to avoid pandas indexing issues
y = twitter_data['target'].values

print(f"x type: {type(x)}, length: {len(x)}")
print(f"y shape: {y.shape}")

# Split the data
print("Splitting data into train/test sets...")
x_train, x_test, y_train, y_test = train_test_split(
    x, y, 
    test_size=0.2, 
    stratify=y, 
    random_state=2
)

print(f"Training set size: {len(x_train)}")
print(f"Test set size: {len(x_test)}")

# Convert textual data to numerical data using TF-IDF
print("Converting text to TF-IDF features...")
vectorizer = TfidfVectorizer(
    max_features=10000,
    min_df=5,  
    max_df=0.7  
)
x_train = vectorizer.fit_transform(x_train)
x_test = vectorizer.transform(x_test)

print(f"x_train shape after vectorization: {x_train.shape}")
print(f"x_test shape after vectorization: {x_test.shape}")

# Train logistic regression model
print("Training logistic regression model...")
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(x_train, y_train)

# Calculate accuracy on training data
x_train_prediction = model.predict(x_train)
training_data_accuracy = accuracy_score(y_train, x_train_prediction)
print(f'Accuracy score on training data: {training_data_accuracy:.4f}')

# Calculate accuracy on test data
x_test_prediction = model.predict(x_test)
test_data_accuracy = accuracy_score(y_test, x_test_prediction)
print(f'Accuracy score on test data: {test_data_accuracy:.4f}')


print("Saving model and vectorizer...")
try:
    
    with open('trained_model.sav', 'wb') as f:
        pickle.dump(model, f)
    
   
    import os
    os.makedirs('../model', exist_ok=True)
    
    with open('../model/trained_model.sav', 'wb') as f:
        pickle.dump(model, f)
    
    with open('../model/vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    
    print("Model and vectorizer saved successfully!")
except Exception as e:
    print(f"Error saving model: {e}")


if x_test.shape[0] > 0:
   
    sample_idx = min(200, x_test.shape[0] - 1)
    
    
    sample_tfidf = x_test[sample_idx:sample_idx+1]  # Keep as 2D array
    
    print(f"\nSample test - True label: {y_test[sample_idx]}")
    
    
    prediction = model.predict(sample_tfidf)
    print(f"Prediction: {prediction[0]}")
    
    if prediction[0] == 0:
        print('Predicted: Negative Tweet')
    else:
        print('Predicted: Positive Tweet')
    
    
    prediction_proba = model.predict_proba(sample_tfidf)
    print(f"Prediction probabilities: {prediction_proba[0]}")
   
    print(f"\nOriginal tweet sample: {twitter_data['text'].iloc[sample_idx]}")
    print(f"Stemmed content: {twitter_data['stemmed_content'].iloc[sample_idx]}")
else:
    print(f"\nNo test samples available.")