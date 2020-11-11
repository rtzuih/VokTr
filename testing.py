import pandas as pd

df = pd.DataFrame({"Timo": [0, 1, 2, 3, 4], "Henrik": [5, 5, 5, 5, 5]})
df["John"] = ""
print(df)
