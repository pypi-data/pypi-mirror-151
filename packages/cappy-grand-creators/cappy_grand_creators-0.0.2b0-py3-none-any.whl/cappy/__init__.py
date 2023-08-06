# NOTE: Module variables
__doc__ = "Cappy - Card and board management API for The Grand Creators"
__version__ = "0.0.1-beta"
__all__ = ("CardAttribute", "CardRarity", "CardType", "Card", "Deck", "Board")


# NOTE: Imports
from typing import Callable
import copy
import random


# NOTE: Utility functions
def default(value: any, default: any):
    return default if value is None else value


# NOTE: "enums"
class CardAttribute:
    """Enum containing all card attributes.

    .ETERNAL - This card cannot be destroyed in any means.
    .LIFE_STEAL - When this card deals damage, the card's owner gains the damage dealt.
    """
    ETERNAL = 0
    LIFE_STEAL = 1


class CardRarity:
    """Enum containing all card rarities.

    .CM - Common (Cm)
    .RA - Rare (Ra)
    .SURA - Super Rare (SuRa)
    .SERA - Secret Rare (SeRa)
    """
    CM = 0
    RA = 1
    SURA = 2
    SERA = 3


class CardType:
    """Enum containing all card types.

    .FRONTROW - This card is a front-row unit.
    .SUPPORT - This card is a support unit.
    .ENGINE_S0 - This card is a stage 0 card for the engine.
    .ENGINE_S1 - This card is a stage 1 card for the engine.
    .ENGINE_S2 - This card is a stage 2 card for the engine.
    .ENGINE_S3 - This card is a stage 3 card for the engine.
    .ENGINE_S4 - This card is a stage 4 card for the engine.
    """
    FRONTROW = 0
    SUPPORT = 1
    ENGINE_S0 = 2
    ENGINE_S1 = 3
    ENGINE_S2 = 4
    ENGINE_S3 = 5
    ENGINE_S4 = 6


# NOTE: Classes
# NOTE[Classes]: Card
class Card:
    def __init__(
        self,
        name: str,
        typ: CardType,
        authorid: str,
        desc: str = None,
        effect: Callable = None,
        attributes: list[CardAttribute] = None,
        rarity: CardRarity = None,
        attack: int = None,
    ):
        """An object with all values requried for a card.

        Arguments:
            name (str): The card's name.
            typ (CardType): The card's type. See cappy.CardType.
            authorid (str): The card author's name.
            desc (str, Optional): The card's description. Defaults to "".
            effect (Callable, Optional): The card's effect function. Defaults to lambda _: None.
            attributes (list[CardAttribute], Optional): A list of card attributes. Defaults to [].
            rarity (CardRarity, Optional): The card's rarity. See cappy.CardRarity. Defaults to CardRarity.CM.
            attack (int, Optional): The card's attack. Only required for a CardType.LIVE card. Defaults to 0.
        """
        self.name = name
        self.typ = typ
        self.authorid = authorid
        self.desc = default(desc, "")
        self.effect = default(effect, lambda _: None)
        self.attributes = default(attributes, [])
        self.rarity = default(rarity, CardRarity.CM)
        self.attack = default(attack, 0)

    def gen(self):
        """Generates and returns a deepcopy of the card.

        Returns:
            Card: The copy.
        """
        return copy.deepcopy(self)


# NOTE[Classes]: Deck
class Deck:
    def __init__(self, decklist: list[Card]):
        """A deck, contains a decklist and a copy of the decklist.

        Arguments:
            decklist (list[Card]): A list of `Card`s to use as the decklist.
        """
        self.decklist = decklist
        self.instance = copy.copy(self.decklist)

    def draw(self, cards: int = None):
        """Draws a certain number of cards and returns them in a list.

        Arguments:
            cards (int, Optional): The amount of cards to draw. Defaults to 1.

        Returns:
            list[Card]: The cards drawn.
        """
        cards = 1 if cards is None else cards
        return [self.decklist.pop() for _ in range(cards)]

    def shuffle(self):
        """Shuffles the deck's instance.
        """
        random.shuffle(self.instance)

    def reset(self):
        """Resets the deck's instance.
        """
        self.instance = copy.copy(self.decklist)


# NOTE[Classes]: Board
class Board:
    def __init__(self, deck: Deck):
        """Generates a board for a single player.

        Arguments:
            deck (Deck): The deck to use.
        """
        self.frontrow = [None, None]
        self.supports = [None, None, None]
        self.engine = {
            0: None,
            1: None,
            2: None,
            3: None,
            4: None,
        }

        self.player = {
            "hp": 1000,
        }

        self.deck = deck
        self.hand = []

        self.phase = 0
        self.is_turn = False

    def game_start(self):
        """Called when the game starts.
        """
        self.draw(5)

    def turn_start(self):
        """Starts the board player's turn. Sets `phase` to 0 and calls `engine[0].effect`.
        """
        self.is_turn = True

        self.phase = 0
        self.engine[self.phase].effect(self)

        self.next_phase()

    def next_phase(self):
        """Proceeds to the next phase and activates the next engine effect.
        """
        self.phase += 1
        self.engine[self.phase].effect(self)

    def end_turn(self):
        """Sets the phase to 0 and sets `is_turn` to `False`.
        """
        self.phase = 0
        self.is_turn = False

    def draw(self, cards: int = None):
        """Draw a card(s) and appends them to the hand.

        Arguments:
            cards (int, Optional): The amount of cards to draw. Defaults to 1.
        """
        cards = 1 if cards is None else cards
        [self.hand.append(card) for card in self.deck.draw(cards)]
