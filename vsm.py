import math
import nltk
from stemmer import stem


def stopWordList(filename="Stopword-List.txt"):
    stop_words = []
    with open(filename, 'r') as file:
        text = file.read()
        stop_words = text.split()
    return stop_words


def preprocess(text, stop_words):

    tokens = nltk.word_tokenize(text.lower())

    tokens = [token for token in tokens if token.isalpha() and (',') not in token
              and token not in stop_words]
    tokens = [stem(token) for token in tokens]
    return tokens


def get_document_extracts(n):
    extracts = []
    for i in range(1, n+1):
        filename = f"Dataset/{i}.txt"
        with open(filename, 'r') as file:
            document = file.read()
            words = document.split()
            extract_words = words[:10]
            extract = ' '.join(extract_words)
            if len(words) > 10:
                extract += '...'
            extracts.append(extract)
    return extracts


def documentTokenizer(n, stopWords):
    docs_tokens = []
    for i in range(1, n+1):
        with open(f"Dataset/{i}.txt", "r") as file:
            text = file.read()
            table = str.maketrans('', '', '-.\':[,](),')
            text = text.translate(table)

            tokens = preprocess(text, stopWords)
            doc_tokens = {"doc_id": i, "tokens": tokens}
            docs_tokens.append(doc_tokens)
    return docs_tokens

def queryProcessing(q,stopWords):
    table = str.maketrans('', '', '-.\':[,](),')
    q= q.translate(table)
    tokens= preprocess(q, stopWords)
    return tokens

def invertedIndex(docs_tokens):
    inverted_index = {}
    for doc in docs_tokens:
        doc_id = doc['doc_id']
        for pos, token in enumerate(doc['tokens']):
            if token not in inverted_index:
                inverted_index[token] = []
            inverted_index[token].append((doc_id, pos))
    sorted_index = dict(sorted(inverted_index.items()))
    return inverted_index





# Create query vector
def queryVector(query,stop_words,inverted_index):
    query_tokens = queryProcessing(query, stop_words)
    query_vector = {}
    for token in query_tokens:
        if token in inverted_index:
            doc_freq = len(inverted_index[token])
            query_vector[token] = math.log(3/doc_freq, 10)
    return query_vector

# Calculate document vectors
def documnetVector(docs_tokens,inverted_index):
    doc_vectors = {}
    for doc in docs_tokens:
        doc_id = doc['doc_id']
        tokens = doc['tokens']
        tfidf = {}
        for token in set(tokens):
            tf = tokens.count(token) / len(tokens)
            doc_freq = len(inverted_index[token])
            idf = math.log(3/doc_freq, 10)
            tfidf[token] = tf * idf
        doc_vectors[doc_id] = tfidf
    return doc_vectors


# Calculate cosine similarity
def cosineSimalirity(doc_vectors, query_vector, query_tokens):
    results = {}
    for doc_id, vec in doc_vectors.items():
        dot_product = 0
        for token, weight in query_vector.items():
            dot_product += vec.get(token, 0) * weight
        if(len(query_tokens)==0):
            continue
        score = dot_product / (len(query_tokens) * math.sqrt(sum(weight**2 for weight in vec.values())))
        results[doc_id] = score
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    return sorted_results
