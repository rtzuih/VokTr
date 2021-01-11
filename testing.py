import pandas as pd

df = pd.read_csv("vokabeln.csv", sep=";")
udf = pd.read_csv("users.csv", sep=";")

print(len(df))
print((len(udf)))
udf = pd.DataFrame({"Timo": [0 for i in range(len(df))]})
udf.to_csv("users.csv", sep=";", index=False)
print(len(udf))
print(udf)