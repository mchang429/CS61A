"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################

'''Pig Out'''
def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 0.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN Question 1
    total, outcome_one = 0, 0
    while num_rolls > 0:
        value = dice()
        if value == 1:
            outcome_one += 1
        total = total + value
        num_rolls -= 1
    if outcome_one > 0:
        return 0
    return total

    # END Question 1

'''Free Bacon, Hogus Prie'''
def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN Question 2
    if num_rolls == 0:
        x, y = opponent_score//10, opponent_score%10
        score = max(x,y)+1
    else:
        score = roll_dice(num_rolls, dice)
    if is_prime(score):
        return next_prime(score)
    return score
    # END Question 2

def is_prime(n):
    k = 2
    if n <= 1:
        return False
    while k < n:
        if n % k == 0:
            return False
        else:
            k = k + 1
    return True

def next_prime(n):
    k = n + 1
    while not is_prime(k):
        k += 1
    return k

'''Hog Wild'''
def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    # BEGIN Question 3
    if (score+opponent_score) % 7 == 0:
        return four_sided
    else:
        return six_sided
    # END Question 3


def is_swap(score0, score1):
    """Returns whether the last two digits of SCORE0 and SCORE1 are reversed
    versions of each other, such as 19 and 91.
    """
    # BEGIN Question 4
    if score0 < 100 and score1 < 100:
        pass
    elif score0 > 100:
        score0 = score0-100
    else:
        score1 = score1-100
    player_ten, player_one = split_integer(score0)
    opponent_ten, opponent_one = split_integer(score1)
    return player_ten == opponent_one and player_one == opponent_ten
    # END Question 4

def split_integer (score):
    return score //  10, score % 10

def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN Question 5
    while score0 < goal and score1 < goal:
        if player == 0:
            num_rolls = strategy0(score0, score1)
            turn_score = take_turn(num_rolls, score1, select_dice(score0, score1))
            if turn_score == 0:
                score1 = score1 + num_rolls #Piggy Back
            score0 = score0 + turn_score
        elif player == 1:
            num_rolls = strategy1(score1, score0)
            turn_score = take_turn(num_rolls, score0, select_dice(score1, score0))
            if turn_score == 0:
                score0 = score0 + num_rolls #Piggy Back
            score1 = score1 + turn_score
        if is_swap(score0, score1):
            score0, score1 = score1, score0
        player = other(player)
    # END Question 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n

    return strategy


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    5.5

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 0.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 5.5.
    Note that the last example uses roll_dice so the hogtimus prime rule does
    not apply.
    """
    # BEGIN Question 6
    def average(*args):
        sum, k = 0, 1
        while k <= num_samples:
            sum, k = sum + fn(*args), k + 1
        return sum / num_samples
    return average
    # END Question 6


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN Question 7
    num_rolls, highest_score, best_roll = 10, 0, 0
    while num_rolls > 0:
        ave_turn_score = make_averaged(roll_dice)(num_rolls, dice)
        highest_score = max(ave_turn_score, highest_score)
        if ave_turn_score >= highest_score:
            best_roll = num_rolls
        num_rolls -= 1
    return best_roll
    # END Question 7


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 8
    free_bacon = max(opponent_score//10 + 1, opponent_score%10 + 1)
    if is_prime(free_bacon):
        free_bacon = next_prime(free_bacon)
    if free_bacon >= margin:
        num_rolls = 0
    return num_rolls  # Replace this statement
    # END Question 8


def swap_strategy(score, opponent_score, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial swap and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 9
    a, b = (opponent_score//10 + 1, opponent_score%10 + 1)
    free_bacon = max(a, b)
    if a == b:
        return num_rolls
    if True:
        if is_prime(free_bacon):
            free_bacon = next_prime(free_bacon)
            score = score + free_bacon
        else:
            score = score + free_bacon
    if is_swap(score, opponent_score):
        if score <= opponent_score:
            score, opponent_score = opponent_score, score
            return 0
        else:
            pass
    return num_rolls # Replace this statement
    # END Question 9

def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.
    The main strategy is to exploit Free Bacon as much as possible.
    Following that are different ranges between scores that return different
    strategies.
    """
    # BEGIN Question 10
    opponent_ten, opponent_one = opponent_score // 10, opponent_score % 10
    free_bacon = max(opponent_ten, opponent_one) + 1
    dice = select_dice(score, opponent_score)

    if (free_bacon + score + opponent_score) % 7 == 0:
        return 0
    elif free_bacon > 4:
        return 0
    elif (score + opponent_score) %  6== 0:
        return bacon_strategy(score, opponent_score, 4, 4)
    elif (opponent_score - score) > 10 :
        return swap_strategy(score, opponent_score, 6)
    elif (score - opponent_score) > 90:
        return bacon_strategy(score, opponent_score, 4, 4)
    elif (score - opponent_score) > 76:
        return 6
    elif (score - opponent_score) > 60:
        return bacon_strategy(score, opponent_score, 4, 4)
    elif (score - opponent_score) > 26:
        return 2
    elif (score - opponent_score) > 3:
        return bacon_strategy(score, opponent_score, 4, 4)
    elif (score - opponent_score) < 3:
        return  bacon_strategy(score, opponent_score, 6, 5)
    return 4

    # END Question 10



##########################
# Command Line Interface #
##########################


# Note: Functions in this section do not need to be changed. They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
