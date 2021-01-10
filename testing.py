import pandas as pd

df = pd.read_csv("vokabeln.csv", sep=";")
userdf = pd.read_csv("users.csv", sep=";")

print(userdf["Tim"].any())
