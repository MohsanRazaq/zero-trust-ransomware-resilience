import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

print("[ML] Automatically building dataset matrix...")
np.random.seed(42)
num_samples = 1000

# Introduce overlapping variables inside train_model.py to challenge the model:

# Normal user copies a few compressed ZIP/JPEG files (Velocity is low, but Entropy spikes!)
normal_v = np.random.randint(1, 6, num_samples)
normal_e = np.random.uniform(4.0, 7.0, num_samples)  # Increased entropy upper bound

# A slow, stealthy ransomware variant encrypts files deliberately slowly to bypass velocity triggers
attack_v = np.random.randint(4, 15, num_samples)    # Lowered velocity threshold
attack_e = np.random.uniform(6.5, 7.98, num_samples)
df_norm = pd.DataFrame({'velocity': normal_v, 'entropy': normal_e, 'is_malicious': normal_v})
df_att = pd.DataFrame({'velocity': attack_v, 'entropy': attack_e, 'is_malicious': attack_v})
df = pd.concat([df_norm, df_att], ignore_index=True).sample(frac=1).reset_index(drop=True)

df.to_csv('dataset.csv', index=False)
print("[ML] dataset.csv successfully updated with 2000 balanced records.")

X = df[['velocity', 'entropy']]
y = df['is_malicious']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(" ML] Training Random Forest Classifier engine...")
model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"\n[ QUALITY ASSURANCE EVALUATION]\nModel Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print(classification_report(y_test, y_pred))

joblib.dump(model, 'ransomware_model.pkl')
print("[🏁 SUCCESS] Core AI engine compiled and saved as: ransomware_model.pkl")