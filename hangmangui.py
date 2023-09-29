import customtkinter
from hangman import hangman
from tkinter import messagebox
from PIL import Image



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
        self.buttonsubmit = customtkinter.CTkButton(self.entryframe, text="submit", command=self.submit_clicked)
        self.restart_button = customtkinter.CTkButton(self.titleframe, text="Restart", command=self.restart_game)
        self.hangmanlabel = customtkinter.CTkLabel(self.hangmanframe, text="")
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
        self.hangmanlabel.pack(padx=5, pady=2)
        self.current_hangman_stage = 0
        self.image_list = []
        for i in range(11):
            my_image = customtkinter.CTkImage(light_image=Image.open(f"img/img{i}.png"),
                                        dark_image=Image.open(f"img/img{i}.png"),
                                        size=(200, 200))
            self.image_list.append(my_image)

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
        self.hangmanlabel.configure(image=None, text="")
        self.titleletter.configure(text="")
        self.current_hangman_stage = 0

        # Show the "Start a game" button again and hide the "Restart" button
        self.startgamebutton.pack()
        self.titlegame.configure(text="Hangman-game")
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
        if self.current_hangman_stage < len(self.image_list):
            self.hangmanlabel.configure(image=self.image_list[self.current_hangman_stage-1], text="")
        else:
            self.hangmanlabel.configure(image=self.image_list[self.current_hangman_stage-1], text="")
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
            self.check_point_status()
        else:
            self.word = self.hangman.select_random_word()
            self.titlegame.configure(text=' '.join(self.word[2]))
            self.startgamebutton.pack_forget()
            self.titleletter.pack(pady=10, padx=5)
            self.check_point_status()

    def check_point_status(self):
        if self.hangman.point >= 11:
            result = self.hangman.ingamegui("*")
            if result["message"]:
                self.titleletter.configure(text=result["message"])  # You can replace this with updating a label or messagebox
            if result["update_word"]:
                self.titlegame.configure(text=' '.join(self.word[2]))
            if result["game_over"]:
                self.restart_button.pack(padx=5, pady=5)
        else:
            self.after(50, self.check_point_status)
                
            


if __name__=="__main__":
    hangmangui = gui()
    hangmangui.mainloop()