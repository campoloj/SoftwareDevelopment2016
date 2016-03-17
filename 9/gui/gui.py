from Tkinter import *

species_template = "        [%d, %d, %d, %s, %s]"
card_template = "[%d, %s]"
player_template = """Player %d:
    Species ([Food, Body, Population, Traits, Fat-food]):
%s
    Bag: %d
    Hand: %s"""
dealer_template = """Dealer Configuration:
    Watering Hole: %d
    Deck: %s
    Players:
%s"""


def display(text):
    """
    Displays the given string of text in a GUI display window
    :param text: String of text to be displayed
    """
    root = Tk()

    xscroll = Scrollbar(root, orient=HORIZONTAL)
    xscroll.pack(side=BOTTOM, fill=X)
    yscroll = Scrollbar(root)
    yscroll.pack(side=RIGHT, fill=Y)

    text_window = Text(root, wrap=NONE,
                       xscrollcommand=xscroll.set,
                       yscrollcommand=yscroll.set)
    text_window.pack(expand=True)

    xscroll.config(command=text_window.xview)
    yscroll.config(command=text_window.yview)

    text_window.insert(END, text)
    mainloop()


def render_dealer(dealer):
    """
    Return a string representing the given dealer
    :param dealer: a Dealer
    :return: String representing the dealer
    """
    return dealer_template % (dealer.watering_hole, render_traitcards(dealer.deck),
                              render_players(dealer.list_of_players))


def render_players(list_of_players):
    """
    Render a list of players into the string format for the gui
    :param list_of_players: a List of PlayerState
    :return: String representing the list_of_players
    """
    player_text = ""
    for player in list_of_players:
        player_display_list = ["        " + line for line in render_player(player).split('\n')]
        player_text += "\n".join(player_display_list)
        if player is not list_of_players[-1]:
            player_text += "\n"

    return player_text


def render_player(player_state):
    """
    Return a string representing the given player state
    :param player_state: a PlayerState
    :return: String representing the player
    """
    return player_template % (player_state.name, render_species(player_state.species),
                              player_state.food_bag, render_traitcards(player_state.hand))


def render_species(species_boards):
    """
    Render a list of species boards into the string format for the gui
    :param species_boards: a List of Species
    :return: String representing the species_boards "[food, body, pop, traits, fat-storage]"
    """
    if not species_boards:
        return '        None'
    species_strings = [species_template % (species.food, species.body, species.population,
                                           "[%s]" % ", ".join(species.trait_names()), str(species.fat_storage))
                       for species in species_boards]
    return '\n'.join(species_strings)


def render_traitcards(trait_cards):
    """
    Render a list of trait cards into the string format for the gui
    :param trait_cards: a List of TraitCards
    :return: String representing the trait_cards "[[trait, int],...]"
    """
    trait_card_strings = [card_template % (card.food_points, card.trait) for card in trait_cards]
    return "[%s]" % ", ".join(trait_card_strings)