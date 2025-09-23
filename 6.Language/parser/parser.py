import nltk
import sys
from nltk import Tree

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP

NP -> N 
NP -> Det N
NP -> PP NP
NP -> AP NP
NP -> N PP


VP -> V 
VP -> V NP
VP -> NP VP
VP -> V NP PP

AP -> Adj | Adj AP

PP -> P
PP -> P NP

"""
# AP -> A | A AP
# NP -> N | D NP | AP NP | N PP | D N
# PP -> P NP
# VP -> V | V NP | V NP PP


grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():
    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()
    
    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")
    
    # Convert input into list of words
    s = preprocess(s)
    
    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return
    
    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()
    
        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence: str) -> list[str]:
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Convert sentence to lowercase
    sentence = sentence.lower()
    
    # Tokenize the sentence into words
    words = nltk.word_tokenize(sentence)
    
    # Filter words to keep only those containing alphabetic characters
    filtered_words = []
    for word in words:
        if any(char.isalpha() for char in word):
            filtered_words.append(word)
    
    return filtered_words


def np_chunk(tree: Tree) -> list:
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunks = []
    for subtree in tree.subtrees():
        if subtree.label() == 'NP':
            # Check if this NP contains any other NPs as subtrees
            has_nested_np = False
            for nested in subtree.subtrees():
                if nested != subtree and nested.label() == 'NP':
                    has_nested_np = True
                    break
            
            # If this NP doesn't contain other NPs, it's a chunk
            if not has_nested_np:
                np_chunks.append(subtree)
    
    return np_chunks


if __name__ == "__main__":
    main()
