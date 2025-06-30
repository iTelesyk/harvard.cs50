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
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus: dict[str], page: str, damping_factor: float):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    total_pages = len(corpus)
    # the set of link in the given page
    links = corpus[page]
    # If no outgoing links, treat as linking to all pages
    if not links:
        links = set(corpus.keys())

    num_links = len(links)
    # Probability for any page from random jump
    prob_random = (1 - damping_factor) / total_pages
    # Probability for linked pages from following a link
    prob_link = damping_factor / num_links
    # Build probability distribution
    trans_model = {}
    for pg in corpus:
        # If page is linked, add link probability
        if pg in links:
            trans_model[pg] = prob_random + prob_link
        else:
            trans_model[pg] = prob_random
    return trans_model


def sample_pagerank(corpus: dict, damping_factor: float, n: int):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # pre-calucate transition_model for each page
    tmodels = dict()
    for page in corpus:
        tmodels[page] = transition_model(
            corpus=corpus, page=page, damping_factor=damping_factor
        )

    # copy keys from corpus to counter, values should be 0
    counter = {page: 0 for page in corpus}

    # pick a random page in rank
    picked_page = random.choice(list(corpus.keys()))

    for i in range(n):

        # adds occurance to a counter
        counter[picked_page] += 1
        # get the transition_model for this page
        tmodel = tmodels[picked_page]

        population = list(tmodel.keys())
        weights = list(tmodel.values())

        # random.choices picks taking in account the weight of population
        picked_page = random.choices(population, weights=weights, k=1)[0]

    # normalize counter to sample value
    rank = dict()
    for page in corpus:
        page_rank = counter[page] / n
        rank[page] = page_rank

    return rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
