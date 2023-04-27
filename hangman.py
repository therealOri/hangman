import os
import secrets
import beaupy
import requests
import sys
import re
import hashlib



update_wordlist = False
min_word_length = 5
max_word_length = 9




def clear():
    os.system("clear||cls")



def update_words():
    github_url = "https://github.com/therealOri/hangman/raw/main/words_alpha.txt"
    hash_url = "https://github.com/therealOri/hangman/raw/main/words_alpha_sha256sum.txt"

    local_file = "words_alpha.txt"

    response = requests.get(hash_url)
    remote_hash = response.content.decode().strip()

    with open(local_file, "rb") as f:
        local_hash = hashlib.sha256(f.read()).hexdigest()

    if remote_hash == local_hash:
        clear()
        print("Local file is up-to-date.")
        return
    else:
        clear()
        print("Hashes don't match! Updating words_alpha.txt...")
        response = requests.get(github_url)
        if response.status_code == 200:
            with open(local_file, "wb") as f:
                f.write(response.content)
            print("words_alpha.txt has been successfully updated!")
            return
        else:
            exit("Error: could not get words_alpha.txt contents from GitHub. Please contact therealOri:https://github.com/therealOri/ on github if this continues...")




def main():
    with open('words_alpha.txt', 'r') as file:
        words = file.readlines()

    chosen_word = secrets.choice(words).strip()
    while len(chosen_word) < min_word_length or len(chosen_word) > max_word_length:
        chosen_word = secrets.choice(words).strip()

    word_length = len(chosen_word)
    display = []
    for _ in range(word_length):
        display.append("_")

    used_letters = []
    hangman = ["    _______",
                "   | /     |",
                "   |/      |",
                "   |      (_)",
                "   |      /|\\",
                "   |       |",
                "   |      / \\",
                "   |   ",
                "   |   ",
                "___|___",
                "       ",]

    MAX_INCORRECT_GUESSES = 10
    incorrect_guesses = 0

    # Main game loop
    while "_" in display and incorrect_guesses < MAX_INCORRECT_GUESSES:
        sys.stdout.write("\033[H\033[J")

        # Update the hangman figure.
        sys.stdout.write("\n".join(hangman[:incorrect_guesses]))
        sys.stdout.write("\n\n")

        # Update display/the word to be guessed.
        sys.stdout.write(" ".join(display))
        sys.stdout.write("\n\n")

        # Show used letters
        sys.stdout.write("Used letters: ")
        for letter in used_letters:
            sys.stdout.write(letter)
            sys.stdout.write(" ")
        sys.stdout.write("\n\n")

        guess = beaupy.prompt("Guess a letter: ").lower()

        if not guess or guess == ' ':
            input('No letter was provided, please provide a letter. Press "enter" to continue...')
            continue

        if len(guess) > 1:
            input('One letter at a time please. Press "enter" to continue...')
            continue

        if not re.match("^[a-zA-Z]*$", guess):
            input('Please choose valid letter from the english alphabet. Press "enter" to continue...')
            continue

        if guess in used_letters:
            input('You have already guessed that letter. Press "enter" to continue...')
            continue

        used_letters.append(guess)

        if guess in chosen_word:
            for i in range(word_length):
                if chosen_word[i] == guess:
                    display[i] = guess
        else:
            incorrect_guesses += 1

    # Game over
    sys.stdout.write("\033[H\033[J")
    if "_" not in display:
        sys.stdout.write(f'Congratulations! You got the word.\nThe word was "{chosen_word}".\n\nDefinition: https://www.definitions.net/definition/{chosen_word}\nNo definition? let me know (https://github.com/therealOri/hangman/issues)\n\n')
    else:
        sys.stdout.write(f'Sorry, Game Over...\nThe word was "{chosen_word}".\n\nDefinition: https://www.definitions.net/definition/{chosen_word}\nNo definition? let me know (https://github.com/therealOri/hangman/issues)\n\n')
        sys.stdout.write("\n".join(hangman))







if __name__ == '__main__':
    if update_wordlist == True:
        clear()
        update_words()
        input('\n\nPress "enter" to start a game of hangman!')
        clear()
        main()
    else:
        clear()
        main()
