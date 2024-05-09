import re
import string
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

def remove_single_quotes(text):
    pattern = r"'[^ ]*"
    text = re.sub(pattern, '', text)
    return text

# Función para reemplazar caracteres especiales
def replace_text(text):
    text = text.replace('â€™', "'")
    text = text.replace('â€‹.', "")
    text = text.replace('â€‹', "")
    text = text.replace('â€“', "")
    text = text.replace('Â®', "")
    text = text.replace('â€¦', " ")
    text = text.replace('â€˜', "")
    text = text.replace('â„¢', "")
    text = text.replace('â€ ”', "")
    text = text.replace('â “', "")
    text = text.replace('.â€', "")
    text = text.replace('â€', "")
    text = text.replace('â€¢', "")
    text = text.replace('â€œ', "")
    text = text.replace('...', "")
    text = remove_single_quotes(text)
    return text

# Función para preprocesar el texto
def preprocess_text(text):
    replaced_text = replace_text(text)
    tokens = word_tokenize(replaced_text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words and token not in string.punctuation]
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    stemmed_tokens = [stemmer.stem(token) for token in lemmatized_tokens]
    return ' '.join(stemmed_tokens)