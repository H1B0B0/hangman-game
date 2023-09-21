import os
import click
import openai
import configparser

# Define the Hangman class
class hangman:
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
        for key in self.cfg["hangman"]:
            self.saved_data.append({key:self.cfg.get("hangman", key)})

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
        self.word = self.get_completion(prompt="Give me just one random word.")
        self.save_words = list(self.word.lower())
        if not self.cfg.has_section("hangman"):
            self.cfg.add_section("hangman")
        self.cfg["hangman"] = {self.word.lower() : 0}
        for i in range(len(self.word)):
            self.hidden_word.append("_")
        
    # Method to select a random word with a specified language
    def select_random_word_with_langage(self, langage):
        self.word = self.get_completion(prompt=f"Give me just one random word in {langage} language. Don't translate the word. Don't return punctuation.")
        self.save_words = list(self.word.lower())
        if not self.cfg.has_section("hangman"):
            self.cfg.add_section("hangman")
        self.cfg["hangman"] = {self.word.lower() : 0}
        for i in range(len(self.word)):
            self.hidden_word.append("_")
        
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
                        if int(self.cfg["hangman"][self.word.lower()]) > self.point:
                            click.echo(click.style(f"Best ever!!! You've guessed {self.word.upper()} in {self.point} attempts.", fg="green"))
                        else:
                            lastpoint = self.cfg["hangman"][self.word.lower()]
                            click.echo(click.style(f"You've guessed {self.word.upper()} in {self.point} attempts. The record is {lastpoint} attempts.", fg="green"))
                    except:
                        click.echo(click.style(f"{self.word.upper()}: correct guess\nCongratulations!", fg="green"))
                    for key in self.cfg['hangman']:  
                        if key != self.word.lower():
                            self.cfg["hangman"][self.word.lower()] = str(self.point)
                        else:
                            self.cfg.set("hangman", self.word.lower(), str(self.point))
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
                            if int(self.cfg["hangman"][self.word.lower()]) > self.point:
                                click.echo(click.style(f"Best ever!!! You've guessed {self.word.upper()} in {self.point} attempts.", fg="green"))
                            else:
                                lastpoint = self.cfg["hangman"][self.word.lower()]
                                click.echo(click.style(f"You've guessed {self.word.upper()} in {self.point} attempts. The record is {lastpoint} attempts.", fg="green"))
                        except:
                            click.echo(click.style(f"{self.word.upper()}: correct guess\nCongratulations!", fg="green"))
                        for key in self.cfg['hangman']:  
                            if key != self.word.lower():
                                self.cfg["hangman"][self.word.lower()] = str(self.point)
                            else:
                                self.cfg.set("hangman", self.word.lower(), str(self.point))
                        with open('config.cfg', 'w') as configfile:
                            self.cfg.write(configfile)
                        exit()
        else: 
            click.echo(click.style(f"GAME OVER\nThe word was: {self.word}", fg="red"))
            for key in self.cfg['hangman']:  
                if key != self.word.lower():
                    self.cfg["hangman"][self.word.lower()] = str(self.point)
                else:
                    self.cfg.set("hangman", self.word.lower(), str(self.point))
            with open('config.cfg', 'w') as configfile:
                self.cfg.write(configfile)
            exit()

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
