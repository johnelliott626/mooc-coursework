from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    And(Or(AKnight, AKnave), Implication(AKnight, Not(AKnave)), Implication(AKnave, Not(AKnight))),
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    And(Or(AKnight, AKnave), Implication(AKnight, Not(AKnave)), Implication(AKnave, Not(AKnight))),
    And(Or(BKnight, BKnave), Implication(BKnight, Not(BKnave)), Implication(BKnave, Not(BKnight))),
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    And(Or(AKnight, AKnave), Implication(AKnight, Not(AKnave)), Implication(AKnave, Not(AKnight))),
    And(Or(BKnight, BKnave), Implication(BKnight, Not(BKnave)), Implication(BKnave, Not(BKnight))),
    # A says "We are the same kind."
    Implication(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),
    Implication(AKnave, Not(Or(And(AKnave, BKnave), And(AKnight, BKnight)))),
    # B says "We are of different kinds."
    Implication(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave))),
    Implication(BKnave, Not(Or(And(AKnave, BKnight), And(AKnight, BKnave)))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    And(Or(AKnight, AKnave), Implication(AKnight, Not(AKnave)), Implication(AKnave, Not(AKnight))),
    And(Or(BKnight, BKnave), Implication(BKnight, Not(BKnave)), Implication(BKnave, Not(BKnight))),
    And(Or(CKnight, CKnave), Implication(CKnight, Not(CKnave)), Implication(CKnave, Not(CKnight))),
    # A says either "I am a knight." or "I am a knave.", but you don't know which.
    Implication(Or(And(AKnight, Not(AKnave)), And(AKnave, Not(AKnight))), AKnight),
    Implication(Not(Or(And(AKnight, Not(AKnave)), And(AKnave, Not(AKnight)))), AKnave),
    # B says "A said 'I am a knave'."
    Implication(And(AKnight, BKnight), BKnave),
    Implication(And(AKnave, BKnight), Not(BKnave)),
    # B says "C is a knave."
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),
    # C says "A is a knight."
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
