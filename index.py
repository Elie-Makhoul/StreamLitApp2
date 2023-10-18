# this is a playground  file

import pandas as pd

df = pd.read_csv("csv/LC_Loan_Modified.csv")


# Removing the '%' symbol and converting 'revol_util' to float


print("Data type of the column:", df["loan_amnt"].dtype)


print(">>>", df["loan_status"][0])
