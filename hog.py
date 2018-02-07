"""CS 61A Presents The Game of Hog."""

from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    sum, one_times, pigout = 0, 0, False
    while one_times < num_rolls:
        current_roll = dice()
        if current_roll == 1:
            pigout = True
        else:
            sum += current_roll
        one_times += 1
    return (pigout and 1) or sum
    # END PROBLEM 1


def free_bacon(score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    assert score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    i = 0
    while score:
        score, remainder = score // 10, score % 10
        if i < remainder:
            i = remainder
    return i + 1
    # END PROBLEM 2


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 3
    if num_rolls == 0:
        return max(opponent_score // 10, opponent_score % 10) + 1
    else:
        sum = roll_dice(num_rolls, dice)
    return sum
    # END PROBLEM 3


def is_swap(score0, score1):
    """Return whether one of the scores is an integer multiple of the other."""
    # BEGIN PROBLEM 4
    if (score0 == 0 or score0 == 1) or (score1 == 0 or score1 == 1):
        return False
    elif (score0 % score1 == 0) or (score1 % score0 == 0):
        return True
    else:
        return False
    # END PROBLEM 4


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    return silence


def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    while score0 < goal and score1 < goal:
        if player == 0:
            score0 += take_turn(strategy0(score0, score1), score1, dice)
            if is_swap(score0, score1):
                score0, score1 = score1, score0
        else:
            score1 += take_turn(strategy1(score1, score0), score0, dice)
            if is_swap(score1, score0):
                score0, score1 = score1, score0
        player = other(player)
        say = say(score0, score1)
    # END PROBLEM 5
    return score0, score1

## A strategy is a function that, given a player's score and their opponent's score,
#returns how many dice the player wants to roll. A strategy function (such as strategy0 and strategy1)
#takes two arguments: scores for the current player and opposing player, which both must be non-negative integers.
#A strategy function returns the number of dice that the current player wants to roll in the turn.
#Each strategy function should be called only once per turn. Don't worry about the details of
#implementing strategies yet. You will develop them in Phase 3. ###


#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores


def announce_lead_changes(previous_leader=None):
    """Return a commentary function that announces lead changes.

    >>> f0 = announce_lead_changes()
    >>> f1 = f0(5, 0)
    Player 0 takes the lead by 5
    >>> f2 = f1(5, 12)
    Player 1 takes the lead by 7
    >>> f3 = f2(8, 12)
    >>> f4 = f3(8, 13)
    >>> f5 = f4(15, 13)
    Player 0 takes the lead by 2
    """
    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != previous_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)
    return say


def both(f, g):
    """Return a commentary function that says what f says, then what g says.

    >>> h0 = both(say_scores, announce_lead_changes())
    >>> h1 = h0(10, 0)
    Player 0 now has 10 and Player 1 now has 0
    Player 0 takes the lead by 10
    >>> h2 = h1(10, 6)
    Player 0 now has 10 and Player 1 now has 6
    >>> h3 = h2(6, 18) # Player 0 gets 8 points, then Swine Swap applies
    Player 0 now has 6 and Player 1 now has 18
    Player 1 takes the lead by 12
    """
    # BEGIN PROBLEM 6
    def say_both(s0, s1):
        return both(f(s0,s1), g(s0,s1))
    return say_both
    # END PROBLEM 6


def announce_highest(who, previous_high=0, previous_score=0):
    """Return a commentary function that announces when WHO's score
    increases by more than ever before in the game.

    >>> f0 = announce_highest(1) # Only announce Player 1 score gains
    >>> f1 = f0(11, 0)
    >>> f2 = f1(11, 1)
    1 point! That's the biggest gain yet for Player 1
    >>> f3 = f2(20, 1)
    >>> f4 = f3(5, 20) # Player 1 gets 4 points, then Swine Swap applies
    19 points! That's the biggest gain yet for Player 1
    >>> f5 = f4(20, 40) # Player 0 gets 35 points, then Swine Swap applies
    20 points! That's the biggest gain yet for Player 1
    >>> f6 = f5(20, 55) # Player 1 gets 15 points; not enough for a new high
    """
    assert who == 0 or who == 1, 'The who argument should indicate a player.'
    # BEGIN PROBLEM 7
    def announce(score0, score1):
        nonlocal previous_score, previous_high
        if who == 0: #when the player is player 0
            if score0 - previous_score > previous_high:
                if (score0 - previous_score) == 1:
                    print("1 point! That's the biggest gain yet for Player 0")
                else:
                    print((score0 - previous_score), "points! That's the biggest gain yet for Player 0")
                previous_high = score0 - previous_score
            previous_score = score0
        else: #will go to player 1
            if score1 - previous_score > previous_high:
                if score1 - previous_score == 1:
                    print("1 point! That's the biggest gain yet for Player 1")
                else:
                    print((score1 - previous_score), "points! That's the biggest gain yet for Player 1")
                previous_high = score1 - previous_score
            previous_score = score1
        return announce
    return announce
####
# """first attempt"""
#    def announce(score0, score1):
#        current_high0 = max(score0 - previous_score, previous_high)
#        current_high1 = max(score1 - previous_score, previous_high)
#        current_high = current_high0 and current_high1
#        new_score = score0 and score1
#        if who == 0 and current_high0 > previous_high:
#            if current_high0 == 1:
#                newscore0 = score0 - previous_score
#                print(newscore0, "point! That's the biggest gain yet for Player 0")
#            if current_high0 >= 2:
#                newscore0 = score0 - previous_score
#                print(newscore0, "points! That's the biggest gain yet for Player 0")
#        elif who == 1 and current_high1 > previous_high:
#            if current_high1 == 1:
#                newscore1 = score1 - previous_score
#                print(newscore1, "point! That's the biggest gain yet for Player 1")
#            if current_high1 >= 2:
#                newscore1 = score1 - previous_score
#                print(newscore1, "points! That's the biggest gain yet for Player 1")
#        return announce_highest(who, current_high, new_score)
#    return announce

####
# """ 2nd attempt"""
#        if who == 0 and (score0 - previous_score > previous_high):
#            if score0 - previous_score == 1:
#                newscore0 = max(score0 - previous_score, previous_high)
#                print(newscore0, "point! That's the biggest gain yet for Player 0")
#            if score0 - previous_score >= 2:
#                newscore0 = max(score0 - previous_score, previous_high)
#                print(newscore0, "points! That's the biggest gain yet for Player 1")
#        elif who == 1 and (score1 - previous_score > previous_high):
#            if score1 - previous_score == 1:
#                newscore1 = max(score1 - previous_score, previous_high)
#                print(newscore1, "point! That's the biggest gain yet for Player 1")
#            if score1 - previous_score >= 2:
#                newscore1 = max(score1 - previous_score, previous_high)
#                print(newscore1, "points! That's the biggest gain yet for Player 1")
#        else:
#            if who == 0 and (score0 - previous_score < previous_high):
#                highestgain0 = max(score0 - previous_score, previous_high)
#                return announce_highest(who, highestgain0, score0)
#            if who == 1 and (score1 - previous_score < previous_high):
#                highestgain1 = max(score1 - previous_score, previous_high)
#                return announce_highest(who, highestgain1, score1)
#        if who == 0:
#            return announce_highest(who, newscore0, score0)
#        if who == 1:
#            return announce_highest(who, newscore1, score1)
#    return announce
####
    # END PROBLEM 7


#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_roll_dice = make_averaged(roll_dice, 1000)
    >>>averaged_roll_dice(2, dice)
    6.0
    """
    # BEGIN PROBLEM 8
    def average(*args):
        sum, i = 0, 0
        while i < num_samples:
            sum, i = sum + fn(*args), i + 1
        return sum / num_samples
    return average
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    num_dice, fixed_average = 1, 0 ##num_dice = minimum of 1 dice rolled, don't think free-bacon would count for this function
    average = make_averaged(roll_dice, num_samples) ## using the make_averged function defined previously
    while num_dice <= 10: #max number of dice can roll is 10, so set limit to 10
        if average(num_dice, dice) > fixed_average:
            fixed_average = average(num_dice, dice)
            max_num_dice = num_dice
        num_dice += 1
#        max_roll = max(max_roll, average) ##ignore this block of code, attempt number 1 ###
#        if average >= max_roll:
#            re_turn = num_dice
#        num_dice -= 1 ## <--- issue, would throw inside infinite loop, fix!!! += or -=
    return max_num_dice
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
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

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if False:  # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"


def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points, and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    bacon = max(opponent_score // 10, opponent_score % 10) + 1 #refer back to free_bacon & take_turn
    if bacon >= margin:
        return 0  # Replace this statement
    else:
        return num_rolls
    # END PROBLEM 10


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.

    >>> swap_strategy(13, 60, 8, 6)
    0
    >>> swap_strategy(30, 54, 8, 6)
    6
    """
    # BEGIN PROBLEM 11
#    bacon = max(opponent_score // 10, opponent_score % 10) + 1
#    if ((score + bacon) != opponent_score) and score < opponent_score:
#        return 0
#    elif score + bacon > 2 * opponent_score:
#        return num_rolls
#    else:
#        return num_rolls
#        return bacon_strategy(score, opponent_score, margin, num_rolls) # Replace this statement
    # END PROBLEM 11
    bacon = max(opponent_score // 10, opponent_score % 10) + 1
#    if 2 * (score + bacon) == opponent_score:
    if bacon >= margin or (((bacon + score) * 2) + 2) <= opponent_score:
        return 0
    elif score + bacon > 2 * opponent_score:
        return num_rolls
    else:
        return num_rolls
#    elif score + bacon == 2 * opponent_score:
#        return num_rolls
#    elif bacon >= margin:
#        return 0
#    free_score=1+int(max(str(opponent_score)))
#    if 2*(score+free_score) == opponent_score:
#        return 0
#    elif score+free_score == 2*opponent_score:
#        return BASELINE_NUM_ROLLS
#    elif free_score >= BACON_MARGIN:
#        return 0
#    else:
#        return BASELINE_NUM_ROLLS

#    if free_bacon_score >= margin or (free_bacon_score + score)*2 == opponent_score:
#        return 0
#    return num_rolls

def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    "*** REPLACE THIS LINE ***"
    return 4  # Replace this statement
    # END PROBLEM 12


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


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
