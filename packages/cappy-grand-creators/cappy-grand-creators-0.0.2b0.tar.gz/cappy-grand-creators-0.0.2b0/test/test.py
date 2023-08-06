# This adds Cappy to the PATH so that it can be imported without building it.
try:
    import sys
    sys.path.append("src/")
    print("(test.py) Appended src/ to sys.path.")
except Exception:
    print("(test.py) Failed to append src/ to sys.path.")

# Import cards and cappy
from cards import cards
import cappy


# Make the board!
board = cappy.Board(
    cappy.Deck(
        [cards[0].gen() for _ in range(20)]
    )
)

board.engine = {
    0: cards[1].gen(),
    1: cards[2].gen(),
    2: cards[3].gen(),
    3: cards[4].gen(),
    4: cards[5].gen(),
}


print([card.name for card in board.hand])
assert [card.name for card in board.hand] == []
board.turn_start()
# print([card.name for card in board.hand])
board.next_phase()
board.next_phase()
board.next_phase()
board.next_phase()
