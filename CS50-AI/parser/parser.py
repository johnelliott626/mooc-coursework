import nltk
import sys

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
S -> NPV | NPV NP | NPV NP NP | NPV P NP Conj NP V | NPV NP Conj NPV P NP Adv
S -> NPV Conj NPV 
S -> NPV NP P NP Conj NPV P NP
NPV -> NP V | NP V Adv | V NP
NP -> N | Det N | P N | Det Adj N | N Adv | 


"""

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


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    tokens = nltk.word_tokenize(sentence)

    result = list()

    # Convert all characters to lowercase and remove non-alphabetic words
    for token in tokens:
        word = token.lower()
        for letter in word:
            if letter.isalpha():
                result.append(word)
                break
    
    return result


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    result = []
    subtrees = tree.subtrees()

    for subtree in subtrees:
        if subtree != tree and subtree.label() == "NP":
            has_np_child = False
            for child_subtree in subtree.subtrees():
                if child_subtree != subtree and child_subtree.label() == "NP":
                    has_np_child = True
                    break
            if not has_np_child:
                result.append(subtree)
    return result


if __name__ == "__main__":
    main()
