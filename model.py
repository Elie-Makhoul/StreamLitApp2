
# %%
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report


df = pd.read_csv("csv/LC_Loan_Modified.csv")


def one_hot_encode_all(df):
    # Select non-numerical columns for one-hot encoding
    non_numeric_columns = df.select_dtypes(exclude=['number']).columns

    # Perform one-hot encoding for each non-numerical column
    for col in non_numeric_columns:
        df = pd.concat([df, pd.get_dummies(df[col], prefix=col)], axis=1)
        df.drop(col, axis=1, inplace=True)

    return df


df['loan_status'] = df['loan_status'].map({'Charged Off': 1, 'Fully Paid': 0})
# %%

# Features (X) and target variable (y)
non_numeric_columns = df.select_dtypes(exclude=['number']).columns
df = df.drop(columns=non_numeric_columns)
x = df.drop('loan_status', axis=1)  # Features
# one_hot_encode_all(x)
y = df['loan_status']  # Target
# print(">>>", y)


# Train-test split
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=12)
# %%
# Model selection and training (using XGBoost)
model = XGBClassifier()  # You can specify hyperparameters here
model.fit(x_train, y_train)
# %%
# Model evaluation
y_pred = model.predict(x_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# %%


# Create a confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Plot the confusion matrix
plt.figure(figsize=(6, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
            annot_kws={'size': 16}, linewidths=0.5)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

# %%
