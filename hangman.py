from random_word import RandomWords
import os

# Funciton that clears the console. Source: https://bit.ly/2MDZBCC
def clear():
    '''Clears the console window.'''
    os.system('cls' if os.name == 'nt' else 'clear')

class Game:
    '''Game rules integral to the program running.'''
    def __init__(self):
        '''Initialize values for tracking victory and running condition.'''
        self.victory = False
        self.difficulty = 0
    
    def check_victory(self, guess, keyword):
        '''Checks if the player has correctly guessed the keyword.'''
        if guess == keyword:
            self.victory = True
        else:
            self.victory = False

    def set_difficulty(self):
        print('Choose your difficulty:')
        print('Easy: 4\t\tMedium: 6\tHard: 8')
        while self.difficulty not in range(4, 8):
            self.difficulty = int(input('>>> '))
    
    def check_guess(self, progress, keyword):
        '''After each round, check if the player has guessed the keyword'''
        str = ''
        for letter in progress:
            str += letter

        if str == keyword:
            return True
        else:
            return False
    
class Keyword:
    '''A hidden word the player attempts to guess.'''
    def __init__(self, difficulty):
        '''Initializes a variable that holds the hidden word.'''
        # Create variables used for generating keyword.
        k = RandomWords()
        min = difficulty
        max = difficulty + 2
        self.keyword = k.get_random_word(minLength = min, maxLength = max)
        del k, min, max       
        
        self.progress = []
        for char in range(len(self.keyword)):
            if self.keyword[char] == '-':
                self.progress.append('-')
            else:
                self.progress.append('_')
        
        self.guessed_letters = []
    
    def record_guess(self, guess):
        '''Record the player's guess'''
        self.guessed_letters.append(guess)
        self.guessed_letters.sort()
    
    def get_guessed_letters(self):
        return str(*self.guessed_letters, end='\n')
    
    def update_progress(self, guess):
        # Implement relevant correted guess outcome.
        for letter in range(len(self.keyword)):
            if guess == list(self.keyword)[letter]:
                self.progress[letter] = guess
    
    def compare(self, guess):
        if guess in self.keyword:
            return True
        else:
            return False

class GameBoard:
    '''Game UI displayed in the console window.'''
    def __init__(self, lives):
        self.body = {
            "head": 'O' if lives <= 5 else ' ',
            "torso": '|' if lives <= 4 else ' ',
            "left_arm": '/' if lives <= 3 else ' ',
            "right_arm": '\\' if lives <= 2 else ' ',
            "left_leg": '/' if lives <= 1 else ' ',
            "right_leg": '\\' if lives == 0 else ' '
        }
        self.gallows = {
            "row0": '\t\t\t ____________',
            "row1": '\t\t\t |\t    |',
            "row2": 'Limbs Remaining: {}\t {self.body["head"]}\t    |',
            "row3": '\t\t\t{self.body["left_arm"]}{self.body["torso"]}{self.body["right_arm"]}\t    |',
            "row4": '\t\t\t{self.body["left_leg"]} {self.body["right_leg"]}\t    |',
            "row5": '\t\t\t     _______|____',
            "row6": '\t\t\t    |           |'
        }

    def set_body(self, lives, progress):
        self.body = {
            "head": 'O' if lives <= 5 else ' ',
            "torso": '|' if lives <= 4 else ' ',
            "left_arm": '/' if lives <= 3 else ' ',
            "right_arm": '\\' if lives <= 2 else ' ',
            "left_leg": '/' if lives <= 1 else ' ',
            "right_leg": '\\' if lives == 0 else ' '
        }
        clear()

    def get_gallows(self, lives):
        for i in range(7):
            pass

        print('\t\t\t ____________')
        print('\t\t\t |\t    |')
        print(f'Limbs Remaining: {lives}\t {self.body["head"]}\t    |')
        print(f'\t\t\t{self.body["left_arm"]}{self.body["torso"]}{self.body["right_arm"]}\t    |')
        print(f'\t\t\t{self.body["left_leg"]} {self.body["right_leg"]}\t    |')
        print('\t\t\t     _______|____')
        print('\t\t\t    |           |')

        # print(*progress, end=' ')
        # print()
    def get_progress(self, progress):
        print(*progress, end='\n')

class Player:
    def __init__(self):
        self.lives = 6
        self.guess = 'default'

    def set_guess(self):
        self.guess = str(list(input('Does it have the letter... '))[0])
    
    def check_guess(self, keyword):
        if self.guess == keyword:
            return True
        else:
            return False

##############################################################################
clear()
# Main Program starts here.
# Condition that keeps the script running.
# This lets the player play as many games as they wish.
keep_playing = True
player = Player()
games_played = []   # List containing data of each played game.

# Main loop starts here.
while keep_playing:
    
    game = Game()
    game.set_difficulty()
    key = Keyword(game.difficulty)
    board = GameBoard(player.lives)

    while player.lives > 0:
        # Play the game here.
        # Part I: Print the board and UI.
        clear()
        board.get_gallows(player.lives)
        print(*key.progress, end='\n')
        print('Letters guessed: ', end='')
        print(*key.guessed_letters, end='\n')

        # Part II: Player guesses a letter.
        player.set_guess()
        key.guessed_letters.append(player.guess.upper())
        # Sort the guessed letters for readability upon board refresh
        key.guessed_letters.sort()
        

        # Part III: Check the validity of the player's guess.
        if game.check_guess(key.progress, key.keyword):
            # End the current game loop to endgame events.
            break
        # If the player hasn't won the game, see if their guess was valid.
        elif key.compare(player.guess):
            # Record the letter guessed for future reference.
            key.record_guess(player.guess)
            key.update_progress(player.guess)
        else:
            # The player guessed incorrect and loses one life.
            player.lives -= 1        

    if game.check_guess(key.progress, key.keyword):
        print('CONGRATULATIONS! YOU WIN!')
    else:
        # Perhaps this clause is a duplicate code of a method written above.
        # Must check later...
        for letter in range(len(key.keyword)):
            key.progress[letter] = key.keyword[letter]
        print(*key.progress, end='\n')
        print('GAME OVER')

    # Prompt the player to play another game or to terminate the script.
    again = input("Press 'Y' to play another game.")
    if again == 'Y':
        pass
    else:
        keep_playing = False
