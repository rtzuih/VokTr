import random
from httpcore import _exceptions
from googletrans import Translator
from fuzzywuzzy import fuzz
import pandas as pd
from termcolor import colored

# Unit = input("Aus welcher Unit möchtest du Vokabeln lernen? ")

try:
    with open("vokabeln.csv", "r") as csvfile:
        voc_df = pd.read_csv(csvfile, sep=";")


except FileNotFoundError:
    print("No vocabulary data found")
    with open("vokabeln.csv", "w") as csvfile:
        voc_df = pd.DataFrame()
        voc_df.to_csv(csvfile, sep=";", index=False)


def add_vokabulary(ger_v, eng_v):
    with open("vokabeln.csv", "w", newline="") as f:
        voc_df.append([ger_v, eng_v], ignore_index=True)
        if input(voc_df):
            voc_df.to_csv(f, sep=";", index=False)
        else:
            print("nope")


HELP_MSG = """
Du kannst folgende Befehle verwenden:

"1" um dich alle Vokabeln abfragen zu lassen.
"2" um dir alle Vokabeln anzeigen zu lassen
"3" um Vokabeln hinzuzufügen

!trl <Text> <Zielsprachenkürzel> (de, fr, en, etc) um etwas in eine andere Sprache zu Übersetzen
"""


class Trainer:
    def __init__(self, username):
        try:
            with open("users.csv", "r") as csvfile:
                self.users_df = pd.read_csv(csvfile, sep=";")
            if username in self.users_df:
                print(f"Welcome back {username}!\n")

            else:
                self.users_df[username] = [0 for i in range(len(voc_df))]
                print(f"Welcome {username}\n")
                with open("users.csv", "w", newline="") as csvfile:
                    self.users_df.to_csv(csvfile, sep=";", index=False)

        except FileNotFoundError:
            with open("users.csv", "w", newline="") as csvfile:
                self.users_df = pd.DataFrame(data={username: [0 for i in range(len(voc_df))]})
                self.users_df.to_csv(csvfile, sep=";", index=False)
                print(f"New User '{username}' created")
        except pd.errors.EmptyDataError:
            with open("users.csv", "w", newline="") as csvfile:
                self.users_df = pd.DataFrame(data={username: [0 for i in range(len(voc_df))]})
                self.users_df.to_csv(csvfile, sep=";", index=False)
                print(f"New User '{username}' created")
        Trainer.userdataanalysis(self)

    def userdataanalysis(self):
        self.hard_to_learn = pd.DataFrame(data={"Ger": [], "Eng": []})
        for i in range(len(self.users_df)):
            if self.users_df.loc[i, username] > 0:
                self.hard_to_learn = self.hard_to_learn.append(voc_df.loc[i], ignore_index=True)
                # learn_the_problematic = input(f"Willst du '{voc_df.loc[i, 'Ger']}' insbesondere üben? Du hast diese Vokabel letzes mal {self.users_df.loc[i, username]} falsch gemacht.")
        #print("\n".join(f"{self.hard_to_learn['Ger'][i]} - {self.hard_to_learn['Eng'][i]}" for i in range(len(self.hard_to_learn))))
        if len(self.hard_to_learn) > 0:
            if input(
                    f"Letztes mal hattest du mit einigen Vokabeln besondere Schwierigkeiten. Möchtest du diese insbesondere Üben? (y/n)") == "y":
                print("Ok, los gehts!")
                with open("users.csv", "w", newline="") as csvfile:
                    self.users_df[username] = pd.DataFrame(data={username: [0 for i in range(len(voc_df))]})
                    self.users_df.to_csv(csvfile, sep=";", index=False)
                Trainer.train(self, self.hard_to_learn)
                Trainer.menu(self)

            else:
                Trainer.menu(self)
        else:
            Trainer.menu(self)

    def menu(self):

        while True:
            command = input("What do you want to do? ")

            if command == "exit":
                break
            elif command == "1":
                Trainer.train(self, voc_df)

            elif command == "2":
                # print("\n" + "\n".join("{} - {}".format(vg, ve) for vg, ve in zip(vokabeln_g, vokabeln_e)) + "\n")
                print("\n".join(f"{voc_df['Ger'][i]} - {voc_df['Eng'][i]}" for i in range(len(voc_df['Ger']))))

            elif command == "3":
                vokg = input("Neue Deutsche Vokabel")
                voke = input("Neue Englische Vokabel")
                add_vokabulary(vokg, voke)

            elif command[:4] == "!trl":
                try:
                    print(f"Übersetzung ihrer Eingabe:\n{Translator().translate(command[5:-3], command[-2:]).text}\n")
                except _exceptions.ConnectError:
                    print("Dein Text konnte nicht übersetzt werden.\nHast du vielleicht keine Internetverbindung?")

            elif command[:4] == "help":
                print(HELP_MSG)
            else:
                print("\nType 'help' for help\n")

    def train(self, voc):
        order = list(i for i in range(len(voc["Ger"])))
        random.shuffle(order)

        mode = random.randint(0, 1)
        while len(order) != 0:

            user_input = input(
                f"\nWas ist die {'Englische' if mode == 0 else 'Deutsche'} Übersetzung von " + colored(f"{voc['Ger' if mode == 0 else 'Eng'][order[0]]} ", "blue"))

            if user_input.lower() == "exit":
                break

            elif user_input == voc['Eng' if mode == 0 else 'Ger'][order[0]]:
                print(colored("Richtig!!!", "green"))
                mode = random.randint(0, 1)
                order.remove(order[0])
            elif user_input == "skip":
                print(f"{voc['Ger' if mode == 0 else 'Eng'][order[0]]} has been skipped")
                skipped_vocabulary = order[0]
                while order[0] == skipped_vocabulary:
                    random.shuffle(order)
            else:
                if fuzz.ratio(user_input.lower(), voc['Eng' if mode == 0 else 'Ger'][order[0]].lower()) > 75:
                    print(colored("Hast du dich vielleicht nur vertippt?\n", "yellow"))
                else:
                    print(colored("Leider falsch.", "red"))
                    self.users_df.loc[order[0], username] = self.users_df.loc[order[0], username] + 1
                    random.shuffle(order)

        with open("users.csv", "w", newline="") as csvfile:
            self.users_df.to_csv(csvfile, sep=";", index=False)

        if self.users_df[username].any():
            if input("Willst du die Vokabeln wissen, mit denen du Schwierigkeiten hast? (y/n) ") == "y":
                hard = []
                for i in range(len(voc_df)):
                    if self.users_df.loc[i, username] > 0:
                        hard.append(i)
                print("\n".join(f"{voc_df['Ger'][i]} - {voc_df['Eng'][i]}" for i in hard))

username = input("Was ist dein Nutzername? ")

Trainer(username)
