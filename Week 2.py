import random
import logging

# List of words for the game
word_list = ['python', 'hangman', 'programming', 'developer', 'computer', 'algorithm', 'data']

# Configure logging to save game results
logging.basicConfig(filename='hangman_game.log', level=logging.INFO)

def select_word():
    """Randomly select a word from the word list."""
    return random.choice(word_list)

def display_word(word, guessed_letters):
    """Display the current state of the word with guessed letters revealed."""
    return ''.join([letter if letter in guessed_letters else '_' for letter in word])

def log_game_result(result, word):
    """Log the result of the game to a log file."""
    logging.info(f"Game Result: {result} - Word: {word}")

def hangman_game():
    """Main function to run the Hangman game."""
    print("Welcome to Hangman!")
    
    # Select a random word
    word = select_word()
    guessed_letters = set()
    attempts_left = 6
    incorrect_guesses = set()
    
    while attempts_left > 0:
        # Display the current game state
        print("\nWord: ", display_word(word, guessed_letters))
        print("Guessed Letters: ", ' '.join(guessed_letters))
        print(f"Remaining Attempts: {attempts_left}")
        print(f"Incorrect Guesses: {', '.join(incorrect_guesses)}")
        
        # Get user input
        guess = input("Enter a letter: ").lower()
        
        # Validate input: check if the guess is a single letter and alphabetic
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a valid single letter.")
            continue
        
        # Check if the letter has already been guessed
        if guess in guessed_letters or guess in incorrect_guesses:
            print("You've already guessed that letter!")
            continue
        
        # Check if the guess is correct
        if guess in word:
            guessed_letters.add(guess)
            print(f"Good guess! '{guess}' is in the word.")
        else:
            incorrect_guesses.add(guess)
            attempts_left -= 1
            print(f"Oops! '{guess}' is not in the word.")
        
        # Check if the word is fully guessed
        if all(letter in guessed_letters for letter in word):
            print(f"Congratulations! You've guessed the word: {word}")
            log_game_result("Win", word)  # Log the win result
            break
    else:
        # Game over (out of attempts)
        print(f"You've run out of attempts! The word was: {word}")
        log_game_result("Loss", word)  # Log the loss result

if __name__ == "__main__":
    hangman_game()
