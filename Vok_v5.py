import random
from googletrans import Translator
from fuzzywuzzy import fuzz
import pandas as pd

# Unit = input("Aus welcher Unit möchtest du Vokabeln lernen? ")

try:
    with open("vokabeln.csv", "r") as csvfile:
        vocabulary_df = pd.read_csv(csvfile, sep=";")
        vokabeln_g = [item for item in vocabulary_df["German"]]
        vokabeln_e = [item for item in vocabulary_df["English"]]


except FileNotFoundError:
    print("No vocabulary data found")
    vokabeln_g = []
    vokabeln_e = []


def add_vokabulary(ger_v, eng_v):
    vokabeln_g.append(ger_v)
    vokabeln_e.append(eng_v)
    with open("vokabeln.csv", "w", newline="") as csvfile:
        vocabulary = pd.DataFrame({"German": vokabeln_g, "English": vokabeln_e})
        vocabulary.to_csv(csvfile, sep=";", index=False)


HELP_MSG = """
Du kannst folgende Befehle verwenden:

"1" um dich alle Vokabeln abfragen zu lassen.
"2" um dir alle Vokabeln anzeigen zu lassen
"3" um Vokabeln hinzuzufügen

!trl <Text> <Zielsprachenkürzel> (de, fr, en, etc) um etwas in eine andere Sprache zu Übersetzen
"""


class Trainer:
    def __init__(self, username):
        self.reihenfolge = list(i for i in range(len(vokabeln_g)))
        random.shuffle(self.reihenfolge)
        try:
            with open("users.csv", "r") as csvfile:
                users_df = pd.read_csv(csvfile, sep=";")
            if username in users_df:
                print(users_df.to_string())
                print(f"Welcome back {username}!\n")
            else:
                users_df[username] = ""
                with open("users.csv", "w", newline="") as csvfile:
                    users_df.to_csv(csvfile, sep=";", index=False)
                    print(users_df)

        except FileNotFoundError:
            with open("users.csv", "w", newline="") as csvfile:
                users_df = pd.DataFrame({username: []})
                users_df.to_csv(csvfile, sep=";", index=False)
                print(f"New User '{username}' created")
        Trainer.userdataanalysis(self)

    def userdataanalysis(self):
        pass

    def train(self):
        while True:
            command = input("What do you want to do? ")

            if command == "exit" or command == "Exit" or command == "quit" or command == "beenden" or command == "Beenden":
                break
            elif command == "1" or command == "train" or command == "abfrage":
                if len(self.reihenfolge) == 0:
                    self.reihenfolge = list(i for i in range(len(vokabeln_e)))
                    random.shuffle(self.reihenfolge)

                while len(self.reihenfolge) != 0:
                    if random.randint(0, 1) == 0:

                        user_input = input(
                            f"\nWas ist die Englische Übersetzung von {vokabeln_g[self.reihenfolge[0]]} ")
                        print(fuzz.ratio(user_input, vokabeln_e[self.reihenfolge[0]]))
                        if user_input == "exit" or user_input == "Exit" or user_input == "quit" or user_input == "beenden" or user_input == "Beenden":
                            random.shuffle(self.reihenfolge)
                            skipped_vocabulary = self.reihenfolge[0]
                            while self.reihenfolge[0] == skipped_vocabulary:
                                random.shuffle(self.reihenfolge)
                            print("\n")
                            break

                        elif user_input == vokabeln_e[self.reihenfolge[0]]:
                            print("Richtig!!!")
                            self.reihenfolge.remove(self.reihenfolge[0])
                        elif user_input == "skip":
                            print(f"{vokabeln_g[self.reihenfolge[0]]} has been skipped")
                            skipped_vocabulary = self.reihenfolge[0]
                            while self.reihenfolge[0] == skipped_vocabulary:
                                random.shuffle(self.reihenfolge)
                        else:
                            print("Leider falsch.")
                            if fuzz.ratio(user_input, vokabeln_e[self.reihenfolge[0]]) > 60:
                                pass
                            else:
                                random.shuffle(self.reihenfolge)

                    else:
                        user_input = input(
                            f"\nWas ist die Deutsche Übersetzung von {vokabeln_e[self.reihenfolge[0]]} ")
                        if user_input == "exit" or user_input == "Exit" or user_input == "quit" or user_input == "beenden" or user_input == "Beenden":
                            random.shuffle(self.reihenfolge)
                            skipped_vocabulary = self.reihenfolge[0]
                            while self.reihenfolge[0] == skipped_vocabulary:
                                random.shuffle(self.reihenfolge)
                            print("\n")
                            break

                        elif user_input == vokabeln_g[self.reihenfolge[0]]:
                            print("Richtig!!!")
                            self.reihenfolge.remove(self.reihenfolge[0])
                        elif user_input == "skip":
                            print(f"{vokabeln_e[self.reihenfolge[0]]} has been skipped")
                            skipped_vocabulary = self.reihenfolge[0]
                            while self.reihenfolge[0] == skipped_vocabulary:
                                random.shuffle(self.reihenfolge)
                        else:
                            print("Leider falsch.")
                            random.shuffle(self.reihenfolge)

            elif command == "listv" or command == "vokabelliste" or command == "Vokabelliste" or command == "2":
                # print("\n" + "\n".join("{} - {}".format(vg, ve) for vg, ve in zip(vokabeln_g, vokabeln_e)) + "\n")
                print("\n".join(f"{vokabeln_g[i]} - {vokabeln_e[i]}" for i in range(len(vokabeln_e))))

            elif command == "add" or command == "addv" or command == "addvocabulary" or command == "3":
                vokg = input("Neue Deutsche Vokabel")
                voke = input("Neue Englische Vokabel")
                add_vokabulary(vokg, voke)
                self.reihenfolge = list(i for i in range(len(vokabeln_g)))
                random.shuffle(self.reihenfolge)

            elif command[:4] == "!trl":
                print(f"Übersetzung ihrer Eingabe:\n{Translator().translate(command[5:-3], command[-2:]).text}\n")

            elif command[:4] == "help":
                print(HELP_MSG)
            else:
                print("\nType 'help' for help\n")


username = input("Was ist dein Nutzername? ")

Trainer(username).train()
