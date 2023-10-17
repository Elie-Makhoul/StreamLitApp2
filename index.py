import pandas as pd

df = pd.read_csv("csv/LC_Loan_Modified.csv")


# Removing the '%' symbol and converting 'revol_util' to float


print("Data type of the column:", df["home_ownership"].dtype)


print(">>>", df["loan_status"][0])
