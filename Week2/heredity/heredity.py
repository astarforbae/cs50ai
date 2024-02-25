import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def genes_and_traits(people, one_gene, two_genes, have_trait):
    zero_gene = people - one_gene - two_genes
    no_trait = people - have_trait
    genes = {}
    genes.update({k: 0 for k in zero_gene})
    genes.update({k: 1 for k in one_gene})
    genes.update({k: 2 for k in two_genes})

    traits = {}
    traits.update({k: True for k in have_trait})
    traits.update({k: False for k in no_trait})
    return genes, traits


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # 初始化
    genes, traits = genes_and_traits(set(people.keys()), one_gene, two_genes, have_trait)
    prob_genes = {}  # key: name value: 有指定条基因的概率
    remains = set(people.keys())  # 存储还未计算的集合

    for p in remains:
        if people[p]["mother"] is None and people[p]["father"] is None:
            # 没有父母 可以直接算
            prob_genes[p] = PROBS["gene"][genes[p]]
        else:
            father = people[p]["father"]
            mother = people[p]["mother"]
            p_gene = genes[p]  # p有的基因条数
            prob_genes[p] = prob_of_child_genes(p_gene, genes[father], genes[mother])
    product = 1
    for prob in prob_genes.values():
        product *= prob
    for (p, t) in traits.items():
        product *= PROBS["trait"][genes[p]][t]
    return product


def prob_of_child_genes(child_gene, father_gene, mother_gene):
    if child_gene == 0:
        # father 0 mom 0
        return prob_of_passing_genes(0, father_gene) * prob_of_passing_genes(0, mother_gene)
    if child_gene == 1:
        # father 1 mom 0 or father 0 mom 1
        return prob_of_passing_genes(1, father_gene) * prob_of_passing_genes(0, mother_gene) \
            + prob_of_passing_genes(0, father_gene) * prob_of_passing_genes(1, mother_gene)

    if child_gene == 2:
        # father 1 mom 1
        return prob_of_passing_genes(1, father_gene) * prob_of_passing_genes(1, mother_gene)


def prob_of_passing_genes(passed, has):
    # passed: 需要提供多少条基因
    # has: 拥有多少条基因
    if passed == 0:
        # 有 0 条
        if has == 0:
            # good no mutate
            return 1 - PROBS["mutation"]
        if has == 1:
            # good no mutate
            # bad  do mutate
            return (1 - PROBS["mutation"] + PROBS["mutation"]) / 2
        if has == 2:
            # bad do mutate
            return PROBS["mutation"]
    if passed == 1:
        if has == 0:
            # good do mutate
            return PROBS["mutation"]
        if has == 1:
            # good do mutate
            # bad  no mutate
            return (1 - PROBS["mutation"] + PROBS["mutation"]) / 2
        if has == 2:
            # bad no mutate
            return 1 - PROBS["mutation"]
    raise Exception("can only pass 0 or 1")


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    genes, traits = genes_and_traits(set(probabilities.keys()), one_gene, two_genes, have_trait)
    for (people, g) in genes.items():
        probabilities[people]["gene"][g] += p
    for (people, t) in traits.items():
        probabilities[people]["trait"][t] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for p in probabilities:
        for category in probabilities[p]:
            weight_sum = 0
            for (k, v) in probabilities[p][category].items():
                weight_sum += v
            new_dict = {}
            for (k, v) in probabilities[p][category].items():
                new_dict[k] = v / weight_sum
            probabilities[p][category] = new_dict


if __name__ == "__main__":
    main()
