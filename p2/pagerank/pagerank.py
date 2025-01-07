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

    # corpus = {
    #     "1.html": {"2.html", "3.html"},
    #     "2.html": {"3.html"},
    #     "3.html": {"2.html"}
    # }
    # transition_model(corpus, "1.html", DAMPING)

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


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    this_damping = round((1 - damping_factor) / len(corpus), 3)
    prob_dist = {}

    for key in corpus:
        prob_dist[key] = 0

    if len(corpus[page]) == 0:
        for key in prob_dist:
            prob_dist[key] = round(1 / len(corpus), 3)
        return prob_dist

    for key, links in corpus.items():
        prob_dist[key] += this_damping

        if key == page:
            temp_len = len(links)
            temp_damping = round(damping_factor / temp_len, 3)
            for link in links:
                prob_dist[link] += temp_damping

    # print("Transition Model")
    # for key, value in prob_dist.items():
    #     print(f"key: {key}")
    #     print(f"value: {value} \n")

    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    page_rank = {page: 0 for page in corpus}

    pages = list(page_rank.keys())
    current_page = random.choice(pages)
    page_rank[current_page] += 1

    for i in range(n):
        transition = transition_model(corpus, current_page, damping_factor)
        pages_list = list(transition.keys())
        prob_dist_list = list(transition.values())

        current_page = random.choices(pages_list, weights=prob_dist_list, k=1)[0]
        page_rank[current_page] += 1

    for key in page_rank:
        page_rank[key] = page_rank[key] / n

    page_rank = {k: round(v, 3) for k, v in page_rank.items()}

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n = len(corpus)
    page_rank = {page: 1 / n for page in corpus}
    alpha = (1 - damping_factor) / n

    corpus = {
        page: links if links else set(corpus.keys()) for page, links in corpus.items()
    }

    while True:
        temp_rank = {}
        for page, page_links in corpus.items():
            links_sum = 0
            for link in page_links:
                links_sum += page_rank[link] / len(corpus[link])
            temp_rank[page] = alpha + (damping_factor * links_sum)

        if all(abs(temp_rank[page] - page_rank[page]) < 0.001 for page in page_rank):
            break

        page_rank = temp_rank

    total_rank = sum(page_rank.values())
    for page in page_rank:
        page_rank[page] /= total_rank

    return page_rank


if __name__ == "__main__":
    main()
