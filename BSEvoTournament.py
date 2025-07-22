import random
import matplotlib.pyplot as plt
from collections import defaultdict

evolution_history = []

class Bot:
    def __init__(self, bluff_strategy, call_strategy):
        self.bluff_strategy = bluff_strategy
        self.call_strategy = call_strategy
        self.score = 0 # Utility score for the bot
        self.wins = 0 # Number of wins

    def get_strategies(self):
        # You can implement mutation logic later
        return (self.bluff_strategy, self.call_strategy)

        
    def __str__(self):
        return f" Bluff = {self.bluff_strategy.__name__}, Call = {self.call_strategy.__name__}, Score = {self.score}, Wins = {self.wins}"

# Define the bluffing strategies
def strategy_always_truth():
    return 't'

def strategy_always_bluff():
    return 'b'

def strategy_random_bluff():
    return random.choice(['b', 't'])

def strategy_react(opponent_history):
    for opponent, calls in opponent_history.items():
        if not calls or calls[-1] == 'n':
            return 'b'  # Bluff if any opponent didn't call
    return 't'  # Everyone called last time

        
#-----------------------------------------------------#

# Define the calling strategies
def strategy_always_call():
    return 'y'

def strategy_never_call():
    return 'n'

def strategy_random_call():
    return random.choice(['y', 'n'])

def strategy_tit_for_tat(history): # If the user bluffed in the prev round call them out
    if len(history) == 0:
        return 'n'
    if history[-1] == 'b':
        return 'y'
    return 'n'

def strategy_Grim_Trigger(history): # if the user ever bluffed before always call them out
    if len(history) == 0:
        return 'n'
    if history.count('b') > 0:
        return 'y'
    return 'n'

#-----------------------------------------------------#

def countcards(cards, rank):
    return cards.count(rank)

# Deal cards to players
def get_cards(num_players):
    deck = [i for i in range(1, 14) for _ in range(4)]
    random.shuffle(deck)
    return [deck[i::num_players] for i in range(num_players)]

#-----------------------------------------------------#

# Strategy-based bluff/truth play
def bot_bluff_or_truth_strategy(cards, rank, pile, strategy_func,history): 
    # This function is called by the player to decide whether to bluff or tell the truth a
    if strategy_func.__name__ == 'strategy_react':
        choice = strategy_func(history)
    else:
        choice = strategy_func() 

    valid = countcards(cards, rank)
    if choice == 'b' or valid == 0:
        bluff_rank = random.choice(cards)
        count = countcards(cards, bluff_rank)
        toremove = random.randint(1, count)
        for _ in range(toremove):
            cards.remove(bluff_rank)
            pile.append(bluff_rank)
        return 'b'
    else:
        toremove = random.randint(1, valid)
        for _ in range(toremove):
            cards.remove(rank)
            pile.append(rank)
        return 't'

# Strategy-based call decision
def bot_guess_strategy(bot_cards, opponent_cards, strategy_func, history, opponent_choice, pile):
    if strategy_func.__name__ == 'strategy_tit_for_tat' or strategy_func.__name__ == 'strategy_Grim_Trigger':
        guess = strategy_func(history)
    else:
        guess = strategy_func() 

    if guess == 'y':
        if opponent_choice == 'b':
            opponent_cards.extend(pile)
            pile.clear()
        else:
            bot_cards.extend(pile)
            pile.clear()
    return guess

def add_opponent_history(self, opponent_id, choice): # if oppononet calles or not add here
    if opponent_id in self.opponent_history:
        self.opponent_history[opponent_id].append(choice)
    else:
        raise ValueError(f"Opponent ID {opponent_id} not found in history.")
#-----------------------------------------------------#

# Full 4-player simulation loop
def simulate_match(strategy1b, strategy1c, strategy2b, strategy2c,
                   strategy3b, strategy3c, strategy4b, strategy4c,
                   rounds):
    cards = get_cards(4)
    bot_cards = cards
    histories = [[] for _ in range(4)]
    opponent_call_history = {0: {1: [], 2: [], 3: []},
                        1: {0: [], 2: [], 3: []},
                        2: {1: [], 0: [], 3: []},
                        3: {1: [], 2: [], 0: []}
                        } # Maybe Implement this 

    pile = []
    current_rank = 1
 #   print("Initial cards:")
#    print(bot_cards)

    for i in range(rounds):
        for current_player in range(4):
     #       print("Player", current_player + 1, "is playing")
      #      print("Current rank:", current_rank)

            if any(len(bot_cards[j]) == 0 for j in range(4)):
                
                return tuple(len(bot_cards[j]) for j in range(4))

            strategies_b = [strategy1b, strategy2b, strategy3b, strategy4b]
            strategies_c = [strategy1c, strategy2c, strategy3c, strategy4c]

            choice = bot_bluff_or_truth_strategy(bot_cards[current_player], current_rank, pile, strategies_b[current_player],opponent_call_history[current_player])
       #     print(choice, "by player", current_player + 1)
        #    print(strategies_b[current_player].__name__)


            # All other players guess
            for opponent in range(4):
                if opponent == current_player:
                    continue

                bot_guess = bot_guess_strategy(bot_cards[opponent], bot_cards[current_player],
                                   strategies_c[opponent], histories[current_player],
                                   choice, pile)
                opponent_call_history[current_player][opponent].append(bot_guess) # Add to the history of the opponent
                
              #  print("Player", opponent + 1, "guessed", bot_guess, "for player", current_player + 1)
               # print(strategies_c[opponent].__name__)
               # print(histories[current_player])

                if bot_guess == 'y':
                    break
            histories[current_player].append(choice)
        #    print(histories)
         #   print(bot_cards)



            current_rank = current_rank + 1 if current_rank < 13 else 1
         #   print()
    return tuple(len(bot_cards[j]) for j in range(4))

"""
def evolve(bots):
    bots.sort(key=lambda x: x.score)  # Best at top
    best_bot = bots[0]
    worst_bot = bots[-1]

    # (Optional) Add mutation logic here later
    new_bot = Bot(best_bot.bluff_strategy, best_bot.call_strategy)

    bots[-1] = new_bot 
"""


def evolve(bots):
    total_fitness = sum(1.0 / (bot.score + 1e-6) for bot in bots)  
    probs = [(1.0 / (bot.score + 1e-6)) / total_fitness for bot in bots]
    
    new_bots = []
    for _ in range(len(bots)):
        selected_bot = random.choices(bots, weights=probs, k=1)[0]
        new_bots.append(Bot(selected_bot.bluff_strategy, selected_bot.call_strategy))  

    bots[:] = new_bots


def tournament(bots, num_matches=50, rounds_per_match=2000):
    for i in range(num_matches):
        # Choose 4 random bots for this match
        match_bots = random.sample(bots, 4)

        final_counts = simulate_match(
            match_bots[0].get_strategies()[0], match_bots[0].get_strategies()[1],
            match_bots[1].get_strategies()[0], match_bots[1].get_strategies()[1],
            match_bots[2].get_strategies()[0], match_bots[2].get_strategies()[1],
            match_bots[3].get_strategies()[0], match_bots[3].get_strategies()[1],
            rounds=rounds_per_match
        )

        # Update scores and wins for just these 4
        for bot, cards_left in zip(match_bots, final_counts):
            bot.score += cards_left
            if cards_left == 0:
                bot.wins += 1

        # Evolution step — on the **whole** population
        evolve(bots)
        composition = defaultdict(int)
        for bot in bots:
            key = (bot.bluff_strategy.__name__, bot.call_strategy.__name__)
            composition[key] += 1
        evolution_history.append(composition)

    # Normalize scores
    for bot in bots:
        bot.score /= num_matches


def plot_evolution_over_time(evolution_history, total_bots):
    # Get all strategy pairs seen
    all_strategies = set()
    for snapshot in evolution_history:
        all_strategies.update(snapshot.keys())
    all_strategies = sorted(all_strategies)

    # Prepare time series data
    time_series = {strategy: [] for strategy in all_strategies}

    for snapshot in evolution_history:
        for strategy in all_strategies:
            count = snapshot.get(strategy, 0)
            time_series[strategy].append(count / total_bots)  # proportion

    # Plot
    plt.figure(figsize=(12, 6))

    colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray','cyan','magenta','black','yellow','olive','teal','navy','lime','coral','salmon','gold','plum','khaki']
    color_index = 0
    for strategy, values in time_series.items():
        label = f"{strategy[0]} + {strategy[1]}"
        plt.plot(values, label=label, color=colors[color_index])
        color_index += 1

    plt.xlabel("Generation (Tournament Round)")
    plt.ylabel("Population Proportion")
    plt.title("Evolution of Strategy Pairs Over Time")
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.show()


def main():
   
    bluff_strategies = [strategy_always_truth, strategy_always_bluff, strategy_random_bluff,strategy_react]
    call_strategies = [strategy_always_call, strategy_never_call, strategy_random_call, strategy_tit_for_tat, strategy_Grim_Trigger]

    bots = [Bot(b, c) for b in bluff_strategies for c in call_strategies]

    tournament(bots)
    plot_evolution_over_time(evolution_history, total_bots=len(bots))


 




 

main()

