import random
import pandas as pd
import sys
from fuzzywuzzy import fuzz
from termcolor import colored
from time import sleep
from colorama import init


init() #initialises ANSI-colorcodes for windows, no effect on Linux

# Unit = input("Aus welcher Unit möchtest du Vokabeln lernen? ")


HELP_MSG = """
Du kannst folgende Befehle verwenden:

"1" um dich alle Vokabeln abfragen zu lassen.
"2" um dir alle Vokabeln anzeigen zu lassen
"3" um Vokabeln hinzuzufügen
"exit" um das Programm zu beenden

"""


class Trainer:
    def __init__(self):
        try:
            with open("vokabeln.csv", "r") as csvfile:
                self.voc_df = pd.read_csv(csvfile, sep=";")

        except:
            print(colored("\nNo vocabulary data found or file corrupted\n",
                          "red") + "\nCreate a new vocabulary data file?(y/n) ", end='')
            if input() != "y":
                print("Terminating process due to missing vocabulary data")
                sleep(2)
                sys.exit(sys.argv)
            print("creating new data file\nyou can add vocabulary by typing '3'")
            with open("vokabeln.csv", "w", newline="") as csvfile:
                self.voc_df = pd.DataFrame(data={"Ger": ["Hallo"], "Eng": ["hello"]})
                self.voc_df.to_csv(csvfile, sep=";", index=False)

        self.username = input("Was ist dein Nutzername? ")
        try:
            with open("users.csv", "r") as csvfile:
                self.users_df = pd.read_csv(csvfile, sep=";")
            if self.username in self.users_df:
                print(f"Welcome back {self.username}!\n")

            else:
                self.users_df[self.username] = [0 for i in range(len(self.voc_df))]
                print(f"Welcome {self.username}\n")
                with open("users.csv", "w", newline="") as csvfile:
                    self.users_df.to_csv(csvfile, sep=";", index=False)

        except:
            with open("users.csv", "w", newline="") as csvfile:
                self.users_df = pd.DataFrame(data={self.username: [0 for i in range(len(self.voc_df))]})
                self.users_df.to_csv(csvfile, sep=";", index=False)
                print(f"New User '{self.username}' created")
        if len(self.users_df[self.username]) == len(self.voc_df):
            self.userdataanalysis()
        else:
            with open("users.csv", "w", newline="") as csvfile:
                self.users_df[self.username] = pd.DataFrame(data={self.username: [0 for i in range(len(self.voc_df))]})
                self.users_df.to_csv(csvfile, sep=";", index=False)
                self.menu()

    def userdataanalysis(self):
        self.hard_to_learn = pd.DataFrame(data={"Ger": [], "Eng": []})
        for i in range(len(self.users_df)):
            if self.users_df.loc[i, self.username] > 0:
                self.hard_to_learn = self.hard_to_learn.append(self.voc_df.loc[i], ignore_index=True)
                # learn_the_problematic = input(f"Willst du '{self.voc_df.loc[i, 'Ger']}' insbesondere üben? Du hast diese Vokabel letzes mal {self.users_df.loc[i, self.username]} falsch gemacht.")
        #print("\n".join(f"{self.hard_to_learn['Ger'][i]} - {self.hard_to_learn['Eng'][i]}" for i in range(len(self.hard_to_learn))))
        if len(self.hard_to_learn) > 0:
            if input(
                    f"Letztes mal hattest du mit einigen Vokabeln besondere Schwierigkeiten. Möchtest du diese insbesondere Üben? (y/n)") == "y":
                print("Ok, los gehts!")
                with open("users.csv", "w", newline="") as csvfile:
                    self.users_df[self.username] = pd.DataFrame(data={self.username: [0 for i in range(len(self.voc_df))]})
                    self.users_df.to_csv(csvfile, sep=";", index=False)
                self.train(self.hard_to_learn)
                self.menu()

            else:
                self.menu()
        else:
            self.menu()
        print("Du kannst folgende Befehele verwenden:\n\n1 - Training\n2 - Vokabeln anzeigen\n3 - Vokabeln hinzufügen\nhelp - Hilfe anzeigen\nexit - programm beenden\n")

    def menu(self):

        while True:
            command = input("What do you want to do? ")

            if command == "exit":
                break
            elif command == "1":
                self.train(self.voc_df)

            elif command == "2":
                # print("\n" + "\n".join("{} - {}".format(vg, ve) for vg, ve in zip(vokabeln_g, vokabeln_e)) + "\n")
                print("\n".join(colored(f"{self.voc_df['Ger'][i]}", "blue") +" - " + colored(f"{self.voc_df['Eng'][i]}", "magenta") for i in range(len(self.voc_df['Ger']))))

            elif command == "3":
                vokg = input("Neue Deutsche Vokabel ")
                voke = input("Neue Englische Vokabel ")
                self.add_vokabulary(vokg, voke)

            elif command[:4] == "help":
                print(HELP_MSG)
            else:
                print("\nType 'help' for help\n")

    def train(self, voc):
        order = list(i for i in range(len(voc["Ger"])))
        random.shuffle(order)

        mode = random.randint(0, 1)
        print("\nDu kannst folgende Befehle verwenden:\n\nskip - Vokabel überspringen\n? - Lösung anzeigen \nexit um ins Menü zurückzukommen")
        while len(order) != 0:

            print(
                f"\nWas ist die {'Englische' if mode == 0 else 'Deutsche'} Übersetzung von " + colored(f"{voc['Ger' if mode == 0 else 'Eng'][order[0]]} ", "cyan"), end='')
            user_input = input()

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
            elif user_input == "?":
                print(colored(f"{voc['Ger' if mode == 0 else 'Eng'][order[0]]}", "blue") + " - " + colored(f"{voc['Eng' if mode == 0 else 'Ger'][order[0]]}", "magenta"))
                skipped_vocabulary = order[0]
                while order[0] == skipped_vocabulary:
                    random.shuffle(order)
            else:
                if fuzz.ratio(user_input.lower(), voc['Eng' if mode == 0 else 'Ger'][order[0]].lower()) > 75:
                    print(colored("Hast du dich vielleicht nur vertippt?\n", "yellow"))
                else:
                    print(colored("Leider falsch.", "red"))
                    self.users_df.loc[order[0], self.username] = self.users_df.loc[order[0], self.username] + 1
                    random.shuffle(order)

        with open("users.csv", "w", newline="") as csvfile:
            self.users_df.to_csv(csvfile, sep=";", index=False)

        if self.users_df[self.username].any():
            if input("Willst du die Vokabeln wissen, mit denen du Schwierigkeiten hast? (y/n) ") == "y":
                hard = []
                for i in range(len(self.voc_df)):
                    if self.users_df.loc[i, self.username] > 0:
                        hard.append(i)
                print("\n".join(colored(f"{self.voc_df['Ger'][i]}", "blue") + " - " + colored(f"{self.voc_df['Eng'][i]}", "magenta") for i in hard))
        else:
            print(colored("Super, du bist fertig und hast keine Fehler gemacht!!!", "green"))
        print("Du kannst folgende Befehele verwenden:\n\n1 - Training\n2 - Vokabeln anzeigen\n3 - Vokabeln hinzufügen\nhelp - Hilfe anzeigen\nexit - programm beenden\n")
    def add_vokabulary(self, ger_v, eng_v):


        if input(f"\nType exit if there is something incorrect\n{ger_v} - {eng_v}\n") != "exit":
            self.voc_df = self.voc_df.append({"Ger": ger_v, "Eng": eng_v}, ignore_index=True)
            self.users_df = self.users_df.append({self.username: 0}, ignore_index=True)
            with open("vokabeln.csv", "w", newline="") as f:
                self.voc_df.to_csv(f, sep=";", index=False)
            with open("users.csv", "w", newline="") as csvfile:
                self.users_df.to_csv(csvfile, sep=";", index=False)
        else:
            with open("vokabeln.csv", "r") as f:
                self.voc_df = pd.read_csv(f, sep=";", index=False)
            print("nope")

Trainer()