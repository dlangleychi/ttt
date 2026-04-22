import random
import os

def clear_screen():
    os.system('clear')

class Square:
    INITIAL_MARKER = " "
    HUMAN_MARKER = "X"
    COMPUTER_MARKER = "O"

    def __init__(self, marker=INITIAL_MARKER):
        self.marker = marker

    def __str__(self):
        return self.marker

    @property
    def marker(self):
        return self._marker

    @marker.setter
    def marker(self, marker):
        self._marker = marker

    def is_unused(self):
        return self.marker == Square.INITIAL_MARKER

class Board:
    def __init__(self):
        self.squares = {key: Square() for key in range(1, 10)}

    def clear(self):
        for square in self.squares.values():
            square.marker = Square.INITIAL_MARKER

    def display(self):
        print()
        print("     |     |")
        print(f"  {self.squares[1]}  |"
              f"  {self.squares[2]}  |"
              f"  {self.squares[3]}")
        print("     |     |")
        print("-----+-----+-----")
        print("     |     |")
        print(f"  {self.squares[4]}  |"
              f"  {self.squares[5]}  |"
              f"  {self.squares[6]}")
        print("     |     |")
        print("-----+-----+-----")
        print("     |     |")
        print(f"  {self.squares[7]}  |"
              f"  {self.squares[8]}  |"
              f"  {self.squares[9]}")
        print("     |     |")
        print()

    def mark_square_at(self, key, marker):
        self.squares[key].marker = marker

    def unused_squares(self):
        return [key
                for key, square in self.squares.items()
                if square.is_unused()]

    def is_full(self):
        return len(self.unused_squares()) == 0

    def count_markers_for(self, player, keys):
        markers = [self.squares[key].marker for key in keys]
        return markers.count(player.marker)

    def display_with_clear(self):
        clear_screen()
        print("\n")
        self.display()

class Player:
    def __init__(self, marker):
        self.marker = marker
        self.score = 0

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    def increment_score(self):
        self.score += 1

class Human(Player):
    def __init__(self):
        super().__init__(Square.HUMAN_MARKER)

class Computer(Player):
    def __init__(self):
        super().__init__(Square.COMPUTER_MARKER)

class TTTGame:

    POSSIBLE_WINNING_ROWS = (
        (1, 2, 3),  # top row of board
        (4, 5, 6),  # center row of board
        (7, 8, 9),  # bottom row of board
        (1, 4, 7),  # left column of board
        (2, 5, 8),  # middle column of board
        (3, 6, 9),  # right column of board
        (1, 5, 9),  # diagonal: top-left to bottom-right
        (3, 5, 7),  # diagonal: top-right to bottom-left
    )

    CENTER_SQUARE = 5
    MATCH_WINNING_SCORE = 3

    @staticmethod
    def _join_or(ls, delimiter=', ', before_last='or'):
        if len(ls) == 0:
            return ''
        if len(ls) == 1:
            return str(ls[0])
        if len(ls) == 2:
            return f'{ls[0]} {before_last} {ls[1]}'
        return delimiter.join(map(str, ls[:-1])) \
            + f'{delimiter}{before_last} {ls[-1]}'

    def __init__(self):
        self.board = Board()
        self.human = Human()
        self.computer = Computer()

    def play_match(self):
        self.display_welcome_message()

        first_player = self.human
        second_player = self.computer

        while True:
            self.board.clear()
            self.board.display()

            self.play_single_game(first_player)

            self.record_score()

            self.display_score()

            if self.is_match_over():
                self.display_match_results()
                break

            if not self.play_again():
                break

            first_player, second_player = second_player, first_player
        self.display_goodbye_message()

    def play_single_game(self, first_player):
        while True:

            if first_player is self.human:
                self.human_moves()
            else:
                self.computer_moves()
                self.board.display_with_clear()
            if self.is_game_over():
                break

            if first_player is self.human:
                self.computer_moves()
                self.board.display_with_clear()
            else:
                self.human_moves()
            if self.is_game_over():
                break

        self.board.display_with_clear()
        self.display_results()

    def record_score(self):
        if self.is_winner(self.human):
            self.human.increment_score()
        if self.is_winner(self.computer):
            self.computer.increment_score()

    def is_match_over(self):
        return self.is_match_winner(self.human) \
            or self.is_match_winner(self.computer)

    def is_match_winner(self, player):
        return player.score >= TTTGame.MATCH_WINNING_SCORE

    def display_score(self):
        print(f'Human: {self.human.score} Computer: {self.computer.score}')

    def display_welcome_message(self):
        clear_screen()
        print("Welcome to Tic Tac Toe!")
        print()

    def display_goodbye_message(self):
        print("Thanks for playing Tic Tac Toe! Goodbye!")

    def display_results(self):
        if self.is_winner(self.human):
            print("You won! Congratulations!")
        elif self.is_winner(self.computer):
            print("I won! I won! Take that, human!")
        else:
            print("A tie game. How boring.")

    def display_match_results(self):
        if self.is_match_winner(self.human):
            print("Human Wins Match!!!!!!")
        elif self.is_match_winner(self.computer):
            print("Computer Wins MATCH :(")

    def human_moves(self):
        choice = None
        valid_choices = self.board.unused_squares()
        while True:
            choices_list = [str(choice) for choice in valid_choices]
            printable_choices = TTTGame._join_or(choices_list)
            prompt = f"Choose a square ({printable_choices}): "
            choice = input(prompt)

            try:
                choice = int(choice)
                if choice in valid_choices:
                    break
            except ValueError:
                pass

            print("Sorry, that's not a valid choice.")
            print()

        self.board.mark_square_at(choice, self.human.marker)

    def computer_moves(self):

        choice = self.critical_square(self.computer)
        if choice is None:
            choice = self.critical_square(self.human)
        if choice is None:
            choice = self.pick_center_square()
        if choice is None:
            choice = self.pick_random_square()

        self.board.mark_square_at(choice, self.computer.marker)

    def critical_square(self, player):
        for row in TTTGame.POSSIBLE_WINNING_ROWS:
            if self.board.count_markers_for(player, row) == 2:
                for square in row:
                    if square in self.board.unused_squares():
                        return square
        return None

    def pick_center_square(self):
        if TTTGame.CENTER_SQUARE in self.board.unused_squares():
            return TTTGame.CENTER_SQUARE
        return None

    def pick_random_square(self):
        return random.choice(self.board.unused_squares())

    def is_game_over(self):
        return self.board.is_full() or self.someone_won()

    def three_in_a_row(self, player, row):
        return self.board.count_markers_for(player, row) == 3

    def someone_won(self):
        return (self.is_winner(self.human) or
                self.is_winner(self.computer))

    def is_winner(self, player):
        for row in TTTGame.POSSIBLE_WINNING_ROWS:
            if self.three_in_a_row(player, row):
                return True

        return False

    def play_again(self):
        while True:
            answer = input('play again? ')

            try:
                answer = answer.lower()
                if answer == 'y':
                    return True
                if answer == 'n':
                    return False
            except Exception:
                pass

            print('Invalid answer.  Please enter y or n.')

game = TTTGame()
game.play_match()