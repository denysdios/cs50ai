import math
import os
import string
import nltk
import sys
from nltk import word_tokenize

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    docs = dict()
    for document in os.listdir(directory):
        with open(os.path.join(directory, document), encoding="utf8") as d:
            docs[document] = d.read()
    return docs


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    document = document.lower()
    tokenized = word_tokenize(document)
    for word in tokenized.copy():
        if word in string.punctuation or word in nltk.corpus.stopwords.words("english"):
            tokenized.remove(word)
    return tokenized


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    for maindoc in documents:
        for mainword in documents[maindoc]:
            if mainword in idfs.keys():
                continue
            counter = 0
            for litedoc in documents:
                if mainword in documents[litedoc]:
                    counter += 1
            if counter == 0:
                continue
            idfs[mainword] = math.log(len(documents.keys()) / counter)
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    filepoint = {doc: 0 for doc in files}
    for word in query:
        if word not in idfs:
            continue
        for doc in files:
            counter = 0
            for subword in files[doc]:
                if word == subword:
                    counter += 1
            filepoint[doc] += counter * idfs[word]
    return sorted(filepoint, key=lambda x: filepoint[x], reverse=True)[0:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_point = {sentence: [] for sentence in sentences}
    for sentence in sentences:
        point = 0
        for word in query:
            if word in sentences[sentence]:
                if word in idfs.keys():
                    point += idfs[word]
        dense = sum([sentences[sentence].count(x) for x in query]) / len(sentences[sentence])
        sentence_point[sentence] = [point, dense]
    return sorted(sentence_point, key=lambda x: sentence_point[x], reverse=True)[0:n]


if __name__ == "__main__":
    main()
