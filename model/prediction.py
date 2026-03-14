import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib

# ===============================
# 1.LOAD CHURN TRAINING DATA
# ===============================

file_path = r"E:\churn project\prediction.xlsx"
sheet_name = 'vw_ChurnData'

# Using openpyxl engine to avoid format errors
data = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
print("✅ Data loaded successfully:")
print(data.head())

# ===============================
# 2. DATA PREPROCESSING
# ===============================

# Drop unnecessary columns
data = data.drop(['Customer_ID', 'Churn_Category', 'Churn_Reason'], axis=1)

# Columns to label encode
columns_to_encode = [
    'Gender', 'Married', 'State', 'Value_Deal', 'Phone_Service', 'Multiple_Lines',
    'Internet_Service', 'Internet_Type', 'Online_Security', 'Online_Backup',
    'Device_Protection_Plan', 'Premium_Support', 'Streaming_TV', 'Streaming_Movies',
    'Streaming_Music', 'Unlimited_Data', 'Contract', 'Paperless_Billing',
    'Payment_Method'
]

# Encode categorical variables
label_encoders = {}
for column in columns_to_encode:
    label_encoders[column] = LabelEncoder()
    data[column] = label_encoders[column].fit_transform(data[column])

# Encode target variable
data['Customer_Status'] = data['Customer_Status'].map({'Stayed': 0, 'Churned': 1})

# Split features and target
X = data.drop('Customer_Status', axis=1)
y = data['Customer_Status']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ===============================
# 3️. TRAIN RANDOM FOREST MODEL
# ===============================
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# ===============================
# 4️. EVALUATE MODEL
# ===============================
y_pred = rf_model.predict(X_test)

print("\n✅ Model Evaluation:")
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Feature importance plot
importances = rf_model.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(15, 6))
sns.barplot(x=importances[indices], y=X.columns[indices])
plt.title('Feature Importances')
plt.xlabel('Relative Importance')
plt.ylabel('Feature Names')
plt.show()

# ===============================
# 5️. PREDICT ON NEW DATA
# ===============================
sheet_name = 'vw_JoinData'
new_data = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')

print("\n✅ New data loaded successfully:")
print(new_data.head())

# Keep a copy of original data
original_data = new_data.copy()
customer_ids = new_data['Customer_ID']

# Drop unused columns
new_data = new_data.drop(['Customer_ID', 'Customer_Status', 'Churn_Category', 'Churn_Reason'], axis=1)

# Encode categorical columns
for column in new_data.select_dtypes(include=['object']).columns:
    if column in label_encoders:
        new_data[column] = label_encoders[column].transform(new_data[column])
    else:
        print(f"⚠️ Warning: Column '{column}' not found in encoders — check column names.")

# Make predictions
new_predictions = rf_model.predict(new_data)

# Add predictions to original DataFrame
original_data['Customer_Status_Predicted'] = new_predictions

# Filter churned customers
churned_customers = original_data[original_data['Customer_Status_Predicted'] == 1]

# ===============================
# 6️6 SAVE RESULTS
# ===============================
output_path = r"E:\churn project\Predictions.xlsx"
churned_customers.to_excel(output_path, index=False, engine='openpyxl')

print(f"\n🎯 Predictions saved successfully at: {output_path}")
