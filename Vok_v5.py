import random
from httpcore import _exceptions
from googletrans import Translator
from fuzzywuzzy import fuzz
import pandas as pd

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

    def menu(self):
        while True:
            command = input("What do you want to do? ")

            if command == "exit":
                break
            elif command == "1":
                Trainer.train(self)

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

    def train(self):
        order = list(i for i in range(len(voc_df["Ger"])))
        random.shuffle(order)

        mode = random.randint(0, 1)
        while len(order) != 0:

            user_input = input(
                f"\nWas ist die {'Englische' if mode == 0 else 'Deutsche'} Übersetzung von {voc_df['Ger' if mode == 0 else 'Eng'][order[0]]} ")

            if user_input.lower() == "exit":
                break

            elif user_input == voc_df['Eng' if mode == 0 else 'Ger'][order[0]]:
                print("Richtig!!!")
                mode = random.randint(0, 1)
                order.remove(order[0])
            elif user_input == "skip":
                print(f"{voc_df['Ger' if mode == 0 else 'Eng'][order[0]]} has been skipped")
                skipped_vocabulary = order[0]
                while order[0] == skipped_vocabulary:
                    random.shuffle(order)
            else:
                if fuzz.ratio(user_input.lower(), voc_df['Eng' if mode == 0 else 'Ger'][order[0]].lower()) > 75:
                    print("Hast du dich vielleicht nur vertippt?\n")
                else:
                    print("Leider falsch.")
                    

                    random.shuffle(order)


username = input("Was ist dein Nutzername? ")

Trainer(username).menu()
