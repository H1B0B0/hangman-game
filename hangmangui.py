import customtkinter
from hangman import hangman
from tkinter import messagebox



class gui(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.hangman = hangman() 
        self.title("Hangman-game")
        self.listletterbutton=[]
        customtkinter.set_appearance_mode("System")
        self.titleframe = customtkinter.CTkFrame(self)
        self.titlegame = customtkinter.CTkLabel(self.titleframe, text="Hangman-game", font=("arial", 20))
        self.titleletter = customtkinter.CTkLabel(self.titleframe, text="", font=("arial", 20))
        self.startgamebutton =  customtkinter.CTkButton(self.titleframe, text="Start a game", command=self.start_game)
        self.hangmanframe = customtkinter.CTkFrame(self)
        self.buttonframe = customtkinter.CTkFrame(self)
        self.entryframe = customtkinter.CTkFrame(self)
        self.entry = customtkinter.CTkEntry(self.entryframe)
        self.hangman_canvas = customtkinter.CTkCanvas(self.hangmanframe)
        self.buttonsubmit = customtkinter.CTkButton(self.entryframe, text="submit", command=self.submit_clicked)
        self.restart_button = customtkinter.CTkButton(self.titleframe, text="Restart", command=self.restart_game)
        self.resizable(False, False)
        for i in range(26):
            letter = chr(65+i)
            self.button = customtkinter.CTkButton(
                self.buttonframe, width=30, height=30, text=chr(65+i), command=lambda l=letter: self.send_letter(l)
            )
            self.listletterbutton.append(self.button)
            self.button.grid(column=i % 4, row=i // 4, padx=2, pady=2)
        self.titleframe.grid(column=0, columnspan=2, row=0, sticky="nsew")
        self.titlegame.pack(padx=5, pady=5)
        self.startgamebutton.pack(padx=5, pady=5)
        self.hangmanframe.grid(column=0, row=3, sticky="w", padx=5, pady=2)
        self.buttonframe.grid(column=1, row=3, sticky="e", padx=5, pady=2)
        self.entryframe.grid(column=0,columnspan=2, row=4, sticky="nswe", padx=5, pady=2)
        self.entry.grid(column=0, columnspan=1, row=0, padx=2, pady=2, sticky="w")
        self.buttonsubmit.grid(column=1, columnspan=1, row=0, padx=2, pady=2, sticky="e")
        self.hangman_canvas.pack(padx=5, pady=2)
        self.current_hangman_stage = 0
        self.hangman_drawings = [

                        """
                        ============
                        """,
                        """ 
                            |
                            |
                        ============
                        """,
                        """
                            |
                            |
                            |
                        ============
                        """,
                        """
                            |
                            |
                            |
                            |
                            |
                        ============
                        """,
                        """
                        +---+
                            |
                            |
                            |
                            |
                            |
                        ============
                        """,
                        """
                        +---+
                        |   |
                            |
                            |
                            |
                            |
                        ============
                        """,
                        """
                        +---+
                        |   |
                        O   |
                            |
                            |
                            |
                        ============
                        """,
                        """
                        +---+
                        |   |
                        O   |
                        |   |
                            |
                            |
                        ============
                        """,
                        """
                        +---+
                        |   |
                        O   |
                       /|   |
                            |
                            |
                        ============
                        """,
                        """
                        +---+
                        |   |
                        O   |
                       /|\\  |
                            |
                            |
                        ============
                        """,
                        """
                        +---+
                        |   |
                        O   |
                       /|\\  |
                       /    |
                            |
                        ============
                        """,
                        """
                        +---+
                        |   |
                        O   |
                       /|\\  |
                       / \\  |
                            |
                        ============
                        """
                    ]

    def send_letter(self, letter):
        result = self.hangman.ingamegui(letter)
        
        # Update the GUI based on the information returned from ingame
        if result["message"]:
            self.titleletter.configure(text=result["message"])  # You can replace this with updating a label or messagebox
        if result["update_word"]:
            self.titlegame.configure(text=' '.join(self.word[2]))
            # Disable the letter button
            self.disable_letter_button(letter)
        if result["game_over"]:
            self.restart_button.pack(padx=5, pady=5)
            
        # Update hangman drawing if a letter is not found
        if not result["update_word"]:
            self.current_hangman_stage += 1
            self.update_hangman()
            
            # Disable the letter button
            self.disable_letter_button(letter)


    def restart_game(self):
        # Reset the hangman object
        self.hangman = hangman()

        # Enable all letter buttons
        for button in self.listletterbutton:
            button.configure(state="normal")

        # Clear the hangman drawing
        self.hangman_canvas.delete("all")

        # Clear the word and message labels
        self.titlegame.configure(text="")
        self.titleletter.configure(text="")

        # Show the "Start a game" button again and hide the "Restart" button
        self.startgamebutton.pack()
        self.titlegame(text="Hangman-game")
        self.restart_button.pack_forget()

    def submit_clicked(self):
        letter = self.entry.get()
        self.send_letter(letter)

    def disable_letter_button(self, letter):
        # Disable the button corresponding to the letter
        for button in self.listletterbutton:
            if button.cget("text") == letter:
                button.configure(state="disabled")
                break  # No need to continue searching for the button

    # Add this method to update the hangman drawing
    def update_hangman(self):
        if self.current_hangman_stage < len(self.hangman_drawings):
            hangman_drawing = self.hangman_drawings[self.current_hangman_stage]
            self.hangman_canvas.delete("all")
            self.hangman_canvas.create_text(100, 100, text=hangman_drawing, anchor="center", font=("courier", 12))
        else:
            # Handle game over when hangman is fully drawn
            pass

    def start_game(self):
        self.hangman = hangman()
        result = messagebox.askyesno("Langage option", "Do you want to setup langage?")
        if result:
            self.inputlangage = customtkinter.CTkInputDialog(title="Setup langage", text="Enter the langage")
            self.word = self.hangman.select_random_word_with_langage(self.inputlangage.get_input())
            self.titlegame.configure(text=' '.join(self.word[2]))
            self.startgamebutton.pack_forget()
            self.titleletter.pack(pady=10, padx=5)
        else:
            self.word = self.hangman.select_random_word()
            self.titlegame.configure(text=' '.join(self.word[2]))
            self.startgamebutton.pack_forget()
            self.titleletter.pack(pady=10, padx=5)

if __name__=="__main__":
    hangmangui = gui()
    hangmangui.mainloop()