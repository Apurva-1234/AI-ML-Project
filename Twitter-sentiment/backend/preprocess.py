import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
port_stem = PorterStemmer()

def preprocess_text(text: str) -> str:
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower().split()
    text = [port_stem.stem(word) for word in text if word not in stop_words]
    return ' '.join(text)
