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

    # Create a new dictionary that will store the probability distribution to be returned
    probability_distribution = dict.fromkeys(corpus.keys())
    number_of_pages = len(probability_distribution)
    damping_factor_inverse = 1 - damping_factor

    # Add the inverse of the damping factor spread equally across each page
    single_page_dfi = damping_factor_inverse / number_of_pages
    for key in probability_distribution:
        probability_distribution[key] = single_page_dfi

    # Add the damping factor spread equally across each page that are links of page
    links_from_page = corpus[page]
    num_links = len(links_from_page)
    if num_links != 0:
        single_page_df = damping_factor / num_links
        for page in links_from_page:
            probability_distribution[page] += single_page_df

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {key: 0 for key in corpus}
    
    for i in range(n):
        if i == 0:
            current_page = random.choice(list(corpus.keys()))
            pagerank[current_page] += 1
        else:
            previous_page_distribution = transition_model(corpus, current_page, damping_factor)
            pages = []
            weights = []    
            for key, value in previous_page_distribution.items():
                pages.append(key)
                weights.append(value)
            current_page = random.choices(pages, weights, k=1)[0]
            pagerank[current_page] += 1

    for key, value in pagerank.items():
        pagerank[key] = value / n
    
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    current_page_rankings = {key: 1 / num_pages for key in corpus}
    is_converged = False
    
    while not is_converged:
        old_page_rankings = current_page_rankings.copy()

        for page in old_page_rankings:
            current_page_rankings[page] = PR(corpus, page, old_page_rankings, damping_factor, num_pages)

        greatest_difference = 0
        for page in current_page_rankings:
            difference = abs(current_page_rankings[page] - old_page_rankings[page])
            if difference > greatest_difference:
                greatest_difference = difference
        
        if greatest_difference <= .001:
            is_converged = True

    return current_page_rankings

# Function that calculates that page rank of a page in a corpus iteratively
def PR(corpus: dict, p, old_page_rankings, d, N):
    # Pages that link to p, or have no links at all in which they link to every page in the corpus
    pages_link_to_p = [key for key, values in corpus.items() if p in values or len(values) == 0]

    sum = 0
    for linked_page in pages_link_to_p:
        num_links_of_i = len(corpus[linked_page]) 
        if num_links_of_i == 0:
            num_links_of_i = N

        sum += (old_page_rankings[linked_page] / num_links_of_i)
    return (((1 - d) / N) + (d * sum))


if __name__ == "__main__":
    main()
