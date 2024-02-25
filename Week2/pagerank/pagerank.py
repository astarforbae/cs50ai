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
    transition_dict = {}
    pages_linked_to = len(corpus[page])
    if pages_linked_to == 0:
        for key in corpus.keys():
            transition_dict[key] = 1 / len(corpus)
    else:
        for key in corpus.keys():
            transition_dict[key] = (1 - damping_factor) / len(corpus) \
                                   + ((damping_factor / pages_linked_to) if key in corpus[page] and key != page else 0)

    return transition_dict


def random_page(corpus):
    return random.choice(list(corpus.keys()))


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # 初始化计数器字典
    counter = {}
    for key in corpus.keys():
        counter[key] = 0
    # 随机选一个起始page
    page = random_page(corpus)
    counter[page] = 1
    # 随后执行 n-1 次 访问下一个网页的动作
    for i in range(n - 1):
        trans_model = transition_model(corpus, page, damping_factor)
        if len(trans_model) == 0:
            page = random_page(corpus)
        else:
            page = random.choices(list(trans_model.keys()), weights=list(trans_model.values()), k=1)[0]
        counter[page] += 1
    # 估计每个page的estimate importance 并返回
    prs = {}
    for (key, value) in counter.items():
        prs[key] = value / n
    return prs


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # 初始化 阈值 以及 每个page的estimated importance为 1/N
    threshold = 0.001
    prs = {}
    old_prs = {}
    for key in corpus.keys():
        old_prs[key] = 1 / len(corpus)

    # 根据公式迭代，直到误差小于threshold（所有的estimate importance差值都小于threshold）
    while True:
        check_continue = False
        for p in corpus.keys():
            # sum求和
            linking_sum = 0
            for linking_p in corpus.keys():
                if len(corpus[linking_p]) == 0:
                    linking_sum += old_prs[linking_p] / len(corpus)
                elif p in corpus[linking_p]:
                    linking_sum += old_prs[linking_p] / len(corpus[linking_p])
            prs[p] = (1 - damping_factor) / len(corpus) + damping_factor * linking_sum
        diff = max([abs(prs[x] - old_prs[x]) for x in old_prs.keys()])
        if diff < threshold:
            break
        else:
            old_prs = prs.copy()
    return old_prs


if __name__ == "__main__":
    main()
