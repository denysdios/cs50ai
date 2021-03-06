import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    dict_data = dict()
    # If statement for checking if there is any link or not
    if corpus[page]:
        damp = (1 - damping_factor) / len(corpus.keys())
        not_damp = damping_factor / len(corpus[page])

        for i in corpus[page]:
            dict_data[i] = not_damp + damp

        for key in list(corpus.keys()):
            if key not in dict_data:
                dict_data[key] = damp
    else:
        for key in list(corpus.keys()):
            dict_data[key] = 1 / len(corpus.keys())

    return dict_data


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dict_pagerank = dict.fromkeys(corpus.keys(), 0)

    # First Sample
    initial = random.choice(list(dict_pagerank))
    dict_pagerank[initial] += 1 / n
    model = transition_model(corpus, initial, damping_factor)

    # Rest of Samples
    for i in range(n - 1):
        data = str(random.choices(list(model.keys()), weights=list(model.values())))[2:-2]
        dict_pagerank[data] += 1 / n
        model = transition_model(corpus, data, damping_factor)

    return dict_pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dict_damp = dict.fromkeys(corpus.keys(), 1 / len(corpus.keys()))

    # Calculate inverse dict of corpus
    amount = dict()
    for mainkey in corpus.keys():
        data = set()
        for key in corpus.keys():
            if corpus[key].__contains__(mainkey):
                data.add(key)
        amount[mainkey] = data

    # Main Algorithm to calculate pagerank
    while True:
        dummy = 0
        dummy_dic = dict_damp.copy()
        for key in corpus.keys():

            pr = (1 - damping_factor) / len(corpus.keys()) + \
                 (damping_factor * (sum(dummy_dic[i] / len(corpus[i]) for i in amount[key])))

            if -0.001 <= pr - dict_damp[key] <= 0.001:
                dummy += 1

            dict_damp[key] = pr
        if dummy == len(corpus.keys()):
            break

    return dummy_dic


if __name__ == "__main__":
    main()
