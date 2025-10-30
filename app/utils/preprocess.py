import re
import spacy
import unidecode

nlp = spacy.load("pt_core_news_sm")

def remove_usernames(text):
    return re.sub(r'@\w+', '', text)


def remove_hashtags(text):
    return re.sub(r'@\w+', '', text)

def remove_urls(text):
        return re.sub(r'https?://\S+|www\.\S+', '', text)
    
def remove_extra_whitespace(text):
    return re.sub(r'\s+', ' ', text).strip()

def remove_numbers(text):
    return re.sub(r'\d+', '', text)


def remove_accents(text):
    return unidecode.unidecode(text)

def remove_emoticons(text):
    emoticon_pattern = r'[:;=8][\-o\*\']?[\)\]\(\[dDpP/:\}\{@\|\\]'
    return re.sub(emoticon_pattern, '', text)


def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)

def remove_stopwords(text):
    doc = nlp(text)
    filtered_tokens = [token.text for token in doc if not token.is_stop]
    return ' '.join(filtered_tokens)


def lemmatize_text(text):
    doc = nlp(text)
    lemmatized = ' '.join([token.lemma_ for token in doc])
    return lemmatized