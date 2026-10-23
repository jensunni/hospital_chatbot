import nltk # Natural Language Tool Kit
for pkg in ("punkt", "punkt_tab", "stopwords", "wordnet", "omw-1.4"):
    nltk.download(pkg, quiet=True)

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

_lemma = WordNetLemmatizer()
_stops = set(stopwords.words("english")) - {"not", "no"}

def preprocess(text: str) -> str:
    tokens = word_tokenize(text.lower())
    return " ".join(_lemma.lemmatize(t) for t in tokens
                    if t.isalnum() and t not in _stops)