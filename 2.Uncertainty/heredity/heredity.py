import csv
import itertools
import sys

PROBS = {
    # Unconditional probabilities for having gene
    "gene": {2: 0.01, 1: 0.03, 0: 0.96},
    "trait": {
        # Probability of trait given two copies of gene
        2: {True: 0.65, False: 0.35},
        # Probability of trait given one copy of gene
        1: {True: 0.56, False: 0.44},
        # Probability of trait given no gene
        0: {True: 0.01, False: 0.99},
    },
    # Mutation probability
    "mutation": 0.01,
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {"gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0}}
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (
                people[person]["trait"] is not None
                and people[person]["trait"] != (person in have_trait)
            )
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
                "trait": (
                    True
                    if row["trait"] == "1"
                    else False if row["trait"] == "0" else None
                ),
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s)
        for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people: dict, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    global PROBS
    joint_prob = 1
    data = dict()
    for person in people:
        gene = 0
        if person in one_gene:
            gene = 1
        if person in two_genes:
            gene = 2
        trait = False
        if person in have_trait:
            trait = True
        data[person] = {"gene": gene, "trait": trait}

    for person in people:
        # how many genes this person has and their trait
        gene = data[person]["gene"]
        trait = data[person]["trait"]

        # if parents are unknown
        if people[person]["mother"] is None:
            # Unconditional probability for having this gene
            p_g = PROBS["gene"][gene]
            # Conditional probability of having this trait and this gene
            p_t_and_g = PROBS["trait"][gene][trait]
            person_prop = p_g * p_t_and_g

        # if parents are known
        else:
            mother = people[person]["mother"]
            father = people[person]["father"]
            mother_gene_num = data[mother]["gene"]
            father_gene_num = data[father]["gene"]
            p_gene_from_mother = get_parent_probability(mother_gene_num)
            p_gene_from_father = get_parent_probability(father_gene_num)
            match gene:
                case 0:
                    # probability that non of the parents gave their geans
                    p_g = (1 - p_gene_from_mother) * (1 - p_gene_from_father)
                case 1:
                    # two probability combined:
                    # ether got 1 gene from mother, and not from father
                    # or got 1 gene from father, and not from mother
                    p_g = (
                        p_gene_from_mother * (1 - p_gene_from_father)
                        + (1 - p_gene_from_mother) * p_gene_from_father
                    )
                case 2:
                    # probability that both of the parents gave their geans    
                    p_g = p_gene_from_mother * p_gene_from_father

        # Conditional probability of having this trait and this gene
        p_t_and_g = PROBS["trait"][gene][trait]
        person_prop = p_g * p_t_and_g

        # multiply probabilities from each person in studied population
        joint_prob *= person_prop
        
    print(f"{data} : {joint_prob:.8f}")
    return joint_prob


def get_parent_probability(parent_gene: int) -> float:
    """
    Return the probability that a parent with a given number of gene copies
    passes the gene to their child, accounting for mutation.
    - 0 genes: can only pass via mutation
    - 1 gene: 50% chance to pass the gene
    - 2 genes: almost always passes, except for mutation
    """
    if parent_gene == 0:
        return PROBS["mutation"]
    elif parent_gene == 1:
        return 0.5
    elif parent_gene == 2:
        return 1 - PROBS["mutation"]
    else:
        raise ValueError(f"Invalid parent_gene: {parent_gene}")


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities: dict):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # Sum up all values of keys in probabilities[person]["gene"]
        gene_prob_sum = sum(probabilities[person]["gene"].values())
        # Normalize each value by dividing it on the sum of probabilities
        if gene_prob_sum != 0:
            for gene in probabilities[person]["gene"]:
                probabilities[person]["gene"][gene] /= gene_prob_sum

        # Sum up all values of keys in probabilities[person]["trait"]
        trait_prob_sum = sum(probabilities[person]["trait"].values())
        # Normalize each value by dividing it on the sum of probabilities
        if trait_prob_sum != 0:
            for trait in probabilities[person]["trait"]:
                probabilities[person]["trait"][trait] /= trait_prob_sum


if __name__ == "__main__":
    main()
