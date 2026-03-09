import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier

# Load the Kaggle data
try:
    df = pd.read_csv('dataset.csv')
    print("Dataset loaded successfully!")
except FileNotFoundError:
    print("Error: 'dataset.csv' not found!")
    exit()

# Clean symptom strings: remove underscores and lowercase
for col in df.columns:
    if col != 'Disease':
        df[col] = df[col].str.replace('_', ' ').str.strip().str.lower()

# Get symptoms, but REMOVE the 'nan' (float) values before sorting
symptom_cols = [c for c in df.columns if c != 'Disease']
all_features = df[symptom_cols].values.flatten()
# This line removes the empty/NaN values that caused your error
all_features = sorted(list(set([s for s in all_features if isinstance(s, str)])))

# Create a 1/0 matrix for training
X = pd.DataFrame(0, index=np.arange(len(df)), columns=all_features)
for i in range(len(df)):
    row_symptoms = df.iloc[i][symptom_cols].dropna().values
    X.loc[i, row_symptoms] = 1

y = df['Disease']

print(f"Training on {len(all_features)} symptoms... please wait.")
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# Save the model and the feature list
joblib.dump(model, 'model.pkl')
joblib.dump(all_features, 'features.pkl')

print("Successfully trained! 'model.pkl' and 'features.pkl' are ready.")