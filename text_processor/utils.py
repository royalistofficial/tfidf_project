import math
from collections import defaultdict

def calculate_tfidf(texts):
    tf = []
    df = defaultdict(int)
    total_documents = len(texts)

    for text in texts:
        words = text.lower().split()
        total_words = len(words)
        word_count = defaultdict(int)

        for word in words:
            word_count[word] += 1

        tf_doc = {}
        for word, count in word_count.items():
            tf_doc[word] = count / total_words
            df[word] += 1

        tf.append(tf_doc)

    idf = {}
    for word, count in df.items():
        idf[word] = math.log(total_documents / count)

    results = []
    for i in range(total_documents):
        result = {
            'document': i + 1,
            'tf': tf[i],
            'idf': {word: idf[word] for word in tf[i].keys()},
        }
        results.append(result)

    return results
