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
    Or(AKnave, AKnight),
    Or(Not(AKnave), Not(AKnight)),
    Or(And(AKnave, Not(And(AKnave, AKnight))), And(AKnight, And(AKnave, AKnight)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # 规则
    Or(AKnave, AKnight),
    Or(Not(AKnave), Not(AKnight)),
    Or(BKnave, BKnight),
    Or(Not(BKnave), Not(BKnight)),
    # A说的话
    Or(And(AKnave, Not(And(AKnave, BKnave))), And(AKnight, And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # 规则
    Or(AKnave, AKnight),
    Or(Not(AKnave), Not(AKnight)),
    Or(BKnave, BKnight),
    Or(Not(BKnave), Not(BKnight)),
    # A说的话
    Or(
        # A是 Knight，则A说的话真
        And(
            AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))
        ),
        # A是 Knave，则A说的话假
        And(
            AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))
        )
    ),
    # B说的话
    Or(
        # B是 Knight，则B说的话真
        And(
            BKnight, Or(And(AKnight, Not(BKnight)), And(AKnave, Not(BKnave)))
        ),
        # B是 Knave，则B说的话假
        And(
            BKnave, Not(Or(And(AKnight, Not(BKnight)), And(AKnave, Not(BKnave))))
        )
    )
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
    # 规则
    Or(AKnave, AKnight),
    Or(Not(AKnave), Not(AKnight)),
    Or(BKnave, BKnight),
    Or(Not(BKnave), Not(BKnight)),
    Or(CKnave, CKnight),
    Or(Not(CKnave), Not(CKnight)),
    # A说的话
    Or(
        # A Knight
        And(
            AKnight, Or(AKnight, AKnave)
        ),
        # A Knave
        And(

            AKnight, Not(Or(AKnight, AKnave))
        )
    ),
    # B说的话
    Or(
        # B Knight
        And(
            BKnight, AKnave,
        ),
        And(
            BKnave, Not(AKnave),
        )
    ),
    # C说的话
    Or(
        # C Knight
        And(
            CKnight, AKnight
        ),
        # C Knave
        And(
            CKnave, Not(AKnight)
        ),
    )
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
