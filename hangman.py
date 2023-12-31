import os
import click
import openai
import configparser

class hangman:
    """
    The `hangman` class is a Python class that represents a Hangman game. It allows the user to start the game, set the language of the word, select a random word, and play the game by guessing letters of the word. The class keeps track of the player's score, the word to guess, and the hidden word with guessed letters.

    Example Usage:
    hangman_game = hangman()
    hangman_game.start_game()  # Asks the user if they want to start the game
    hangman_game.set_language()  # Asks the user if they want to set the language of the word
    hangman_game.select_random_word()  # Selects a random word
    hangman_game.ingame()  # Plays the Hangman game

    Methods:
    - __init__: Initializes the instance variables of the `hangman` class.
    - start_game: Asks the user if they want to start the game.
    - set_language: Asks the user if they want to set the language of the word.
    - select_random_word: Selects a random word and initializes the hidden word with underscores.
    - ingame: Allows the user to play the Hangman game by guessing letters of the word.
    - get_completion: Uses OpenAI to get a word completion based on a prompt.
    - number_to_words: Converts a number to words.

    Fields:
    - point: Player's score.
    - word: The word to guess.
    - hidden_word: The word with guessed letters hidden.
    - openai_key: OpenAI API key.
    - cfg: ConfigParser object to read and write configuration data.
    - saved_data: List to store saved data from the configuration file.
    """
    def __init__(self) -> None:
        # Initialize instance variables
        self.point = 0                  # Player's score
        self.word = ""                  # The word to guess
        self.hidden_word = []           # The word with guessed letters hidden
        openai_key = os.environ.get("OPENAI")   # Get OpenAI API key from environment variables
        openai.api_key = openai_key
        self.cfg = configparser.ConfigParser()
        self.saved_data = []
        try:
            self.cfg.read("config.cfg")
        except:
            pass
        try:
            for key in self.cfg["hangman"]:
                self.saved_data.append({key:self.cfg.get("hangman", key)})
        except:
            self.cfg.add_section("hangman")

    # Method to start the game
    def start_game(self):
        result = input("Do you want to start the game? (enter yes or no)\n")
        if result == "yes":
            return True
        else:
            self.start_game()

    # Method to set the language of the word
    def set_langage(self):
        result = input("Do you want to set the language of the word? (enter yes or no)\n")
        if result == "yes":
            return True, input("Enter the language\n")
        elif result == "no":
            return False, ""
        else:
            self.set_langage()

    # Method to select a random word
    def select_random_word(self):
        self.word = self.get_completion(prompt="Give me just one random word. Don't return punctuation.")
        self.save_words = list(self.word.lower())
        if not self.cfg.has_section("hangman"):
            self.cfg.add_section("hangman")
        self.cfg["hangman"] = {self.word.lower() : 0}
        for i in range(len(self.word)):
            self.hidden_word.append("_")
        return self.word, self.save_words, self.hidden_word
        
    # Method to select a random word with a specified language
    def select_random_word_with_langage(self, langage):
        self.word = self.get_completion(prompt=f"Give me just one random word in {langage} language. Don't translate the word. Don't return punctuation.")
        self.save_words = list(self.word.lower())
        if not self.cfg.has_section("hangman"):
            self.cfg.add_section("hangman")
        self.cfg["hangman"] = {self.word.lower() : 0}
        for i in range(len(self.word)):
            self.hidden_word.append("_")
        return self.word, self.save_words, self.hidden_word
        
    # Method to get a word completion using OpenAI
    def get_completion(self, prompt, model="gpt-3.5-turbo"):
        try:
            messages = [{"role": "user", "content": prompt}]
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0.7)
            return response.choices[0].message["content"]
        except Exception as e:
            click.echo(click.style(f"An error has occurred: {e}", fg="red"))
            exit()
    
    # Method to convert a number to words
    def number_to_words(self, num):
        number_words = {
            0: 'zero',
            1: 'one',
            2: 'two',
            3: 'three',
            4: 'four',
        }

        return number_words.get(num, str(num))
    # Method to play the Hangman game
    def ingame(self):
        for element in self.saved_data:
            for key in element:
                self.cfg.set("hangman", key, element[key])
        if self.point < 11:
            counter = 0
            click.echo(click.style(f"{' '.join(self.hidden_word)} / {self.point} point{'s' if self.point > 1 else ''}", fg='blue'))
            entry_result = input()
            if len(entry_result) > 1:
                if entry_result.lower() == self.word.lower():
                    try:
                        record = self.cfg["hangman"].get(self.word.lower())
                        if record is None or int(record) > self.point:
                            click.echo(click.style(f"Best ever!!!\n You've guessed {self.word.upper()}\n in {self.point} attempts.", fg="green"))
                            self.cfg["hangman"][self.word.lower()] = str(self.point)  # Update the record only if the current score is better
                        elif int(record) < self.point:
                            lastpoint = self.cfg["hangman"][self.word.lower()]
                            click.echo(click.style(f"You've guessed {self.word.upper()}\n in {self.point} attempts.\n The record is {lastpoint} attempts.", fg="green"))
                        else: 
                            click.echo(click.style(f"{self.word.upper()}: correct guess\nCongratulations!", fg="green"))
                            self.cfg["hangman"][self.word.lower()] = str(self.point)
                    except:
                        click.echo(click.style(f"{self.word.upper()}: correct guess\nCongratulations!", fg="green"))
                        self.cfg["hangman"][self.word.lower()] = str(self.point)
                    with open('config.cfg', 'w') as configfile:
                        self.cfg.write(configfile)
                    exit()
                else: 
                    click.echo(click.style("Bad word retry", fg="red"))
                    self.point += 1
                    self.ingame()
            else:
                entry_result_lower = entry_result.lower()
                for index, letter in enumerate(self.save_words):
                    if entry_result_lower == letter:
                        if letter in self.save_words:
                            counter += 1
                            self.hidden_word[index] = self.word[index].upper()  # Uppercase the correct letter
                            self.save_words[index] = "*"  # Mark the letter as found
                if counter == 0:
                    self.point += 1
                    click.echo(click.style(f"No '{entry_result.upper()}' found", fg="red"))
                    self.ingame()
                else:
                    if "_" in self.hidden_word:
                        click.echo(click.style(f"Found {self.number_to_words(counter)} '{entry_result.upper()}'", fg="green"))
                        self.ingame()
                    else:
                        try:
                            record = self.cfg["hangman"].get(self.word.lower())
                            if record is None or int(record) > self.point:
                                click.echo(click.style(f"Best ever!!! You've guessed {self.word.upper()} in {self.point} attempts.", fg="green"))
                                self.cfg["hangman"][self.word.lower()] = str(self.point)  # Update the record only if the current score is better
                            elif int(record) < self.point:
                                lastpoint = self.cfg["hangman"][self.word.lower()]
                                click.echo(click.style(f"You've guessed {self.word.upper()} in {self.point} attempts. The record is {lastpoint} attempts.", fg="green"))
                            else: 
                                click.echo(click.style(f"{self.word.upper()}: correct guess\nCongratulations!", fg="green"))
                                self.cfg["hangman"][self.word.lower()] = str(self.point)
                        except:
                            click.echo(click.style(f"{self.word.upper()}: correct guess\nCongratulations!", fg="green"))
                            self.cfg["hangman"][self.word.lower()] = str(self.point)

                        with open('config.cfg', 'w') as configfile:
                            self.cfg.write(configfile)
                        exit()
        else: 
            click.echo(click.style(f"GAME OVER\nThe word was: {self.word}", fg="red"))
            record = self.cfg["hangman"].get(self.word.lower())
            if record is None or int(record) < self.point:
                self.cfg["hangman"][self.word.lower()] = str(self.point)  # Update the record only if it's better than the previous score
            with open('config.cfg', 'w') as configfile:
                self.cfg.write(configfile)
            exit()

    def ingamegui(self, letter):
        for element in self.saved_data:
            for key in element:
                self.cfg.set("hangman", key, element[key])
        result = {"message": "", "update_word": True, "disable_letter": False, "game_over": False}

        if self.point < 11:
            counter = 0
            entry_result_lower = letter.lower()
            if len(entry_result_lower) > 1:
                if entry_result_lower == self.word.lower():
                    try:
                        record = self.cfg["hangman"].get(self.word.lower())
                        if record is None or int(record) > self.point:
                            result["message"] = f"Best ever!!!\n You've guessed {self.word.upper()}\n in {self.point} attempts."
                            self.cfg["hangman"][self.word.lower()] = str(self.point)
                            record = self.cfg["hangman"].get(self.word.lower())
                            if record is None or int(record) < self.point:
                                self.cfg["hangman"][self.word.lower()] = str(self.point)
                            with open('config.cfg', 'w') as configfile:
                                self.cfg.write(configfile)
                            result["game_over"] = True
                            return result
                        elif int(record) < self.point:
                            lastpoint = self.cfg["hangman"][self.word.lower()]
                            result["message"] = f"You've guessed {self.word.upper()}\n in {self.point} attempts.\n The record is {lastpoint} attempts."
                            record = self.cfg["hangman"].get(self.word.lower())
                            if record is None or int(record) < self.point:
                                self.cfg["hangman"][self.word.lower()] = str(self.point)
                            with open('config.cfg', 'w') as configfile:
                                self.cfg.write(configfile)
                            result["game_over"] = True
                            return result
                        else:
                            result["message"] = f"{self.word.upper()}: correct guess\nCongratulations!"
                            self.cfg["hangman"][self.word.lower()] = str(self.point)
                            record = self.cfg["hangman"].get(self.word.lower())
                            if record is None or int(record) < self.point:
                                self.cfg["hangman"][self.word.lower()] = str(self.point)
                            with open('config.cfg', 'w') as configfile:
                                self.cfg.write(configfile)
                            result["game_over"] = True
                            return result
                    except:
                        result["message"] = f"{self.word.upper()}: correct guess\nCongratulations!"
                        self.cfg["hangman"][self.word.lower()] = str(self.point)
                        record = self.cfg["hangman"].get(self.word.lower())
                        if record is None or int(record) < self.point:
                            self.cfg["hangman"][self.word.lower()] = str(self.point)
                        with open('config.cfg', 'w') as configfile:
                            self.cfg.write(configfile)
                        result["game_over"] = True
                        return result
            for index, word_letter in enumerate(self.save_words):
                if entry_result_lower == word_letter.lower():
                    counter += 1
                    self.hidden_word[index] = self.word[index].upper()
                    self.save_words[index] = "*"  # Mark the letter as found
                    result["update_word"] = True

            if counter == 0:
                self.point += 1
                result["message"] = f"No '{letter.upper()}' found"
                result["update_word"] = False
            else:
                if "_" not in self.hidden_word:
                    try:
                        record = self.cfg["hangman"].get(self.word.lower())
                        if record is None or int(record) > self.point:
                            result["message"] = f"Best ever!!!\n You've guessed {self.word.upper()}\n in {self.point} attempts."
                            self.cfg["hangman"][self.word.lower()] = str(self.point)
                        elif int(record) < self.point:
                            lastpoint = self.cfg["hangman"][self.word.lower()]
                            result["message"] = f"You've guessed {self.word.upper()}\n in {self.point} attempts.\n The record is {lastpoint} attempts."
                        else:
                            result["message"] = f"{self.word.upper()}: correct guess\nCongratulations!"
                            self.cfg["hangman"][self.word.lower()] = str(self.point)
                    except:
                        result["message"] = f"{self.word.upper()}: correct guess\nCongratulations!"
                        self.cfg["hangman"][self.word.lower()] = str(self.point)

                    with open('config.cfg', 'w') as configfile:
                        self.cfg.write(configfile)
                    result["game_over"] = True
        else:
            result["message"] = f"GAME OVER\nThe word was: {self.word}"
            record = self.cfg["hangman"].get(self.word.lower())
            if record is None or int(record) < self.point:
                self.cfg["hangman"][self.word.lower()] = str(self.point)
            with open('config.cfg', 'w') as configfile:
                self.cfg.write(configfile)
            result["game_over"] = True

        return result



# Entry point for the script
if __name__ == "__main__":
    game = hangman()
    langage = game.set_langage()
    game.start_game()
    if langage[0]:
        game.select_random_word_with_langage(langage[1])
    else: 
        game.select_random_word()
    game.ingame()