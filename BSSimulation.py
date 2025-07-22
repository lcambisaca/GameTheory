
import random
import time

def print_intro():
    print()
    print("Welcome to the BS Game!")
    print("The player has 2 options")
    print("Bluff - Lie about the rank cards you put down")
    print("Truth - Put the cards u declare down")
    print("The other player has to guess if you are bluffing or telling the truth")
    print("If the other player guesses correctly, you have top pick up the pile of cards")
    print("If the other player guesses incorrectly, they have to pick up the pile of cards")
    print("The game ends when one player has no cards left")
    print("The player with no cards left wins the game")
    print()

def countcards(cards, rank):
    return cards.count(rank)


def get_player_choice():
    choice = input("Do you want to bluff or tell the truth? (b/t): ").lower()
    while choice not in ['b', 't']:
        print("Invalid choice. Please enter 'b' for bluff or 't' for truth.")
        choice = input("Do you want to bluff or tell the truth? (b/t): ").lower()
    return choice

    

def player_play_card(cards,rank,pile):
    choice = get_player_choice()
    valid = countcards(cards, rank)
    if (valid == 0 and choice == 't') or choice == 'b':
        choice = 'b'
        # The player is bluffing or has no cards of the rank they want to play
        print("You are bluffing or you have no cards of that rank!")
        num = int(input(f"Enter which rank you are bluffing about: "))
        while num not in cards:
            print("Invalid rank. Please enter a rank you have.")
            num = int(input(f"Enter which rank you are bluffing about: "))
        # Ask player how many cards they want to bluff about
        count = countcards(cards, num)
        toremove = int(input(f"Enter how many cards you want to bluff about 1-{count}: "))
        while toremove < 1 or toremove > count:
            print(f"Invalid number. Please enter a number between 1 and {count}.")
            toremove = int(input(f"Enter how many cards you want to bluff about 1-{count}: "))
            
        for i in range(toremove):
            cards.remove(num)
            pile.append(num)
        print(f"You put down {toremove} cards of rank {num}")
        
    else:
        toremove = int(input(f"Enter how many cards you want to put down 1-{valid}: "))
        while toremove < 1 or toremove > valid:
            print(f"Invalid number. Please enter a number between 1 and {valid}.")
            toremove = int(input(f"Enter how many cards you want to put down 1-{valid}: "))
            
        for i in range(toremove):
            cards.remove(rank)
            pile.append(rank)
        print(f"You put down {toremove} cards of rank {rank}")
    return choice


def player_guess(playercards,botcards,pile,botchoice):
    guess = input("Do you think the other player is bluffing? (y/n): ").lower()
    while guess not in ['y', 'n']:
        print("Invalid choice. Please enter 'y' for yes or 'n' for no.")
        guess = input("Do you think the other player is bluffing? (y/n): ").lower()
    if guess == 'y':
        if botchoice == 'b':
            print("You guessed correctly! The other player was bluffing.")
            botcards.extend(pile)
            pile.clear()
        else:
            print("You guessed incorrectly! The other player was telling the truth.")
            playercards.extend(pile)
            pile.clear()
    else:
        if botchoice == 'b':
            print("You guessed incorrectly! The other player was bluffing.")
         
        else:
            print("You guessed correctly! The other player was telling the truth.")
          
    
def bot_play_card(cards,rank,pile):
    odds = [1,2,2,2,2] # 1 in 5 chance of bluffing
    bluff = random.choices(odds)[0]
    valid = countcards(cards, rank)
    if bluff == 1 or valid ==0 :
        # The bot will bluff 20% of the time
        bluff_rank = random.choices(cards)[0]
        count = countcards(cards, bluff_rank)

        toremove = random.randint(1, count)
        for i in range(toremove):
            cards.remove(bluff_rank)
            pile.append(bluff_rank)
        print(f"Bot is bluffing with rank {bluff_rank} and removed {toremove} cards")

    else:
        # The bot will tell the truth 80% of the time
        count = countcards(cards, rank)
        toremove =random.randint(1, count)
        for i in range(toremove):
            cards.remove(rank)
            pile.append(rank)
        print(f"Bot is telling the truth with rank {rank} and removed {toremove} cards")
    if bluff == 1:
        bluff = 'b'
    else:
        bluff = 't'
    # Return the bot's choice for the player to guess
    print(pile)
    return bluff

def bot_guess(playercards,botcards,pile,playerchoice): 
    botchoice = random.choice(['y', 'n']) # Bot's guess we can switch up the logic here for how often the bot [plays bluff or truth]
    print(f"Bot guessed {botchoice}")

    if botchoice == 'y':
        if playerchoice == 'b':
            print("Bot guessed correctly! You were bluffing.")
            playercards.extend(pile)
            pile.clear()
        else:
            print("Bot guessed incorrectly! You were telling the truth.")
            botcards.extend(pile)
            pile.clear()
    else:
        if playerchoice == 'b':
            print("Bot guessed incorrectly! You were bluffing.")
        else:
            print("Bot guessed correctly! You were telling the truth.")
  

def get_cards(num_players):
    # Initialize a deck of cards
    # 1-13 represent the ranks of the cards (Ace to King)
    cards = [1,1,1,1, 2,2,2,2, 3,3,3,3, 4,4,4,4, 5,5,5,5, 6,6,6,6, 7,7,7,7, 8,8,8,8, 9,9,9,9, 10,10,10,10, 11,11,11,11, 12,12,12,12, 13,13,13,13]
    random.shuffle(cards)
    player1_cards = cards[:52//num_players]
    player2_cards = cards[52//num_players:2*(52//num_players)]
    player3_cards = cards[2*(52//num_players):3*(52//num_players)] if num_players > 2 else []
    player4_cards = cards[3*(52//num_players):] if num_players > 3 else []
    return [player1_cards, player2_cards, player3_cards, player4_cards]


def play_game():
    num_players = int(input("Enter the number of players: "))
    while(num_players < 2 or num_players > 4):
        print("Invalid number of players. Please choose between 2 and 4 players.")
        num_players = int(input("Enter the number of players: "))
    cards = get_cards(num_players)
    player1_cards = sorted(cards[0])
    player2_cards = sorted(cards[1])
    current_player = 1
    current_rank = 1
    pile = []
    # now we will let the players question each other and play the game
    while len(player1_cards) != 0 and len(player2_cards) != 0:
        print()
        print("--------------------------------------------------")
        print(f"Player {current_player}'s turn")
        print(f"Current rank: {current_rank}")
        print(f"Player 1 cards: {player1_cards} len: {len(player1_cards)}")
        print(f"Player 2 cards: {player2_cards} len: {len(player2_cards)}")
        print(f"Pile: {pile}")
        print("--------------------------------------------------")
        if current_player == 1:
            # Player 1's turn
            playerchoice = player_play_card(player1_cards, current_rank, pile) 
            bot_guess(player1_cards, player2_cards, pile, playerchoice)
            current_player = 2
        else:
            # Player 2's turn
            botchoice = bot_play_card(player2_cards, current_rank, pile)
            player_guess(player1_cards, player2_cards, pile, botchoice)
            current_player = 1

        current_rank += 1
        if current_rank > 13:
            current_rank = 1
        # Check if the current player has no cards left
    print()
    print("Game Over!")
    if len(player1_cards) == 0:
        print("Player 1 wins!")
    else:
        print("Player 2 wins!")

    print("Thanks for playing!")
    print("--------------------------------------------------")




#------------------------------------------------------------------#
# Define the strategy function for bluffing or not bluffing
def strategy_always_truth(cards, rank, pile):
    return 't'

def strategy_always_bluff(cards, rank, pile):
    return 'b'

def strategy_random(cards, rank, pile): # Probability of bluffing is 50%
    return random.choice(['b', 't'])

#------------------------------------------------------------------#


# Define the strategy function for calling or not calling
def strategy_always_call():
    return 'y'

def strategy_never_call():
    return 'n'

def strategy_random(): # Probability of bluffing is 50%
    return random.choice(['y', 'n'])

def Tweaker(history):
    # If a player called on you you want to call on them
    if history and history[-1] == 'b':
        return 'y'
    return 'n'

def countcards(cards, rank):
    return cards.count(rank)

#------------------------------------------------------------------#

# Simulate a single round of bot play using a strategy
def bot_guess_strategy(bot1cards,bot2cards,strategy_func, history, bot2choice,pile):
    botchoice = strategy_func() if strategy_func.__name__ != 'Tweaker' else strategy_func(history)
    if botchoice == 'y':
        if bot2choice == 'b':
            print("Bot guessed correctly!")
            bot2cards.extend(pile)
            pile.clear()
        else:
            print("Bot guessed incorrectly!")
            bot1cards.extend(pile)
            pile.clear()
         
    else:
        if bot2choice == 'b':
            print("Bot guessed incorrectly!")
        else:
            print("Bot guessed correctly!")
    return botchoice
    


def bot_bluff_or_truth_strategy(cards, rank, pile, strategy_func):
    choice = strategy_func(cards, rank, pile)
    valid = countcards(cards, rank)
    if choice == 'b' or valid == 0:
        bluff_rank = random.choice(cards)
        count = countcards(cards, bluff_rank)
        toremove = random.randint(1, count)
        for i in range(toremove):
            cards.remove(bluff_rank)
            pile.append(bluff_rank)
        return 'b'
    else:
        toremove = random.randint(1, valid)
        for i in range(toremove):
            cards.remove(rank)
            pile.append(rank)
        return 't'
    
    
def simulate_match(strategy1b,strategy1c, strategy2b,strategy2c,strategy3b,strategy3c, strategy4b,strategy4c, rounds=100):
    cards = get_cards(4)
    bot1_cards = cards[0]
    bot2_cards = cards[1]
    bot3_cards = cards[2]
    bot4_cards = cards[3]
    history1, history2,history3,history4 = [],[],[],[]
    pile = []
    current_rank = 1

    for i in range(rounds):

        if len(bot1_cards) == 0 or len(bot2_cards) == 0 or len(bot3_cards) == 0 or len(bot4_cards) == 0:
            print(f"Game Over!")
            break

        # Bot 1 plays bluff or truth
        choice1 = bot_bluff_or_truth_strategy(bot1_cards, current_rank, pile, strategy1b)

        # Bot 2 guesses
        temp1 = bot_guess_strategy(bot2_cards, bot1_cards, strategy2c, history1, choice1, pile)
        if temp1 != 'y':
            finish
        # Bot 3 guesses


        # Bot 4 guesses






     

        current_rank += 1

        if current_rank > 13:
            current_rank = 1
        history1.append(choice1)

        #------------------------------------------------------------------#
        # Bot 2 plays






        #------------------------------------------------------------------#
        # Bot 3 plays

        #------------------------------------------------------------------#
        # Bot 4 plays








    print(f"Broke in Round {i}")

    return len(bot1_cards), len(bot2_cards) , len(bot3_cards), len(bot4_cards)


def main():
    print_intro()
    play_game()

   


main()
        
     

