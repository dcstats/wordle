"""
A bot that naively plays the game Wordle.

Author: Daniel Cowan
"""

import numpy as np
from wordfreq import zipf_frequency as zf


class WordLengthError(Exception):
    pass


class InvalidWordError(Exception):
    pass


class VersionError(Exception):
    pass


class Wordle:
    """
    This class represents a bot that plays the game Wordle in a
    fairly naive manner. Words on each round of guessing are chosen probabilistically
    based on 1) the results of previous guesses and 2) the frequency of the word in the
    English language.

    Parameters - answer (string) - default 'random', in which case the bot is given a
        random word as the answer. User can also define their own 5-letter word as the
        answer, so long as the word is in the list of possible words.

                version (string) - default 'new', in which case the NYT word list is used;
                if version is 'old', the word list from the original Wordle site is used.
    """

    def __init__(self, answer="random", version="new"):
        # check which version of words to use
        if version == "new":
            fn = "wordle.txt"
            fna = "wordle_answers.txt"
        elif version == "old":
            fn = "wordle_old.txt"
            fna = "wordle_answers_old.txt"
        else:
            raise VersionError(
                f'{version} is not a valid verson. Please use only "new" or "old".'
            )

        # set answer
        if answer == "random":
            with open(fna, "r") as f:
                string = f.read()

            ans = string.split(", ")
            ans = sorted(ans)
            self.answer = np.random.choice(ans)
        else:
            self.answer = str.lower(answer)

        # check word length
        if len(self.answer) != 5:
            raise WordLengthError(f"{self.answer} is not a 5-letter word.")

        # initialize list of possible words
        with open(fn, "r") as f:
            string = f.read()
        words = string.split(", ")
        words = sorted(words)
        self.words = words

        # check if answer is in the word list
        if self.answer not in self.words:
            raise InvalidWordError(
                f"{self.answer} is not in the list of possible words."
            )

        # use zipf scores to rank frequency of words
        freq = {}
        for word in words:
            score = zf(word, "en")
            freq[word] = score
        self.freq = dict(
            sorted(freq.items(), key=lambda x: x[1], reverse=True))

        self.played = False
        self.solved = False
        self.filtered = self.freq
        self.not_in = []
        self.contains = {}
        self.equals = {}
        self.guesses = []
        self.board = []
        self.green_square = "\U0001F7E9"
        self.yellow_square = "\U0001F7E8"
        self.gray_square = "\U00002B1C"

    def play(self):
        """
        This function plays one round of Wordle and prints the output.

        Parameters - N/A

        Returns - self.solved (boolean): whether the puzzle has been solved
        """
        if self.played:
            self.reset_game()

        for i in range(6):
            guess = self.make_guess()

            self.check_word(guess)

            self.filter_possible()

            if self.is_solved(guess):
                self.solved = True
                break

        self.print_state()
        self.played = True

        return self.solved

    def reset_game(self):
        self.played = False
        self.solved = False
        self.filtered = self.freq
        self.not_in = []
        self.contains = {}
        self.equals = {}
        self.guesses = []
        self.board = []
        return

    def return_total_moves(self):
        """
        This function returns the total number of moves that have been made in the game.

        Parameters - N/A

        Returns - the number of guesses made so far, or 7 if the bot failed to solve the puzzle
        """
        if not self.solved and len(self.guesses) == 6:
            return 7
        else:
            return len(self.guesses)

    def make_guess(self):
        """
        This function makes a guess from the list of possible remaining words.
        The words are chosen using a weighted random choice, the weights being determined
        by the word's zipf frequency.

        Parameters - N/A

        Returns - guess (string): the next word to guess
        """
        tot = sum(self.filtered.values())
        probs = {word: (self.filtered[word] / tot) for word in self.filtered}
        guess = np.random.choice(list(probs.keys()), p=list(probs.values()))
        self.guesses.append(guess)
        return guess

    def check_word(self, guess):
        """
        This function checks the current guess against the answer.

        Parameters - guess (string): the current guess

        Returns - N/A
        """
        if self.solved:
            return

        bd = []

        for j in range(len(self.answer)):
            t_let = self.answer[j]
            g_let = guess[j]

            if g_let == t_let:
                bd.append(self.green_square)
                self.equals[j] = g_let

            elif g_let in self.answer:
                bd.append(self.yellow_square)

                if j not in self.contains:
                    self.contains[j] = [g_let]
                else:
                    self.contains[j].append(g_let)

            else:
                bd.append(self.gray_square)
                self.not_in.append(g_let)

        self.board.append(bd)

        return

    def is_solved(self, guess):
        """
        This function checks whether the puzzle has been solved.

        Parameters - guess (string): the current guess

        Returns - (boolean): whether the puzzle has been solved
        """
        return guess == self.answer

    def filter_possible(self):
        """
        This function filters down the word list based on the guesses that
        have been made so far.

        Parameters - N/A

        Returns - N/A
        """
        for k in self.equals:
            self.filtered = {
                word: self.filtered[word]
                for word in self.filtered
                if word[k] == self.equals[k]
            }

        for k in self.contains:
            for let in self.contains[k]:
                self.filtered = {
                    word: self.filtered[word]
                    for word in self.filtered
                    if let in word and not word[k] == let
                }

        for k in self.not_in:
            self.filtered = {
                word: self.filtered[word] for word in self.filtered if k not in word
            }

        return

    def print_state(self):
        """
        This function prints the state of the game.

        Parameters - N/A

        Returns - N/A
        """
        for i in range(len(self.board)):
            print(f'{"".join(self.board[i])} | {self.guesses[i]}')

        return
