"""
Train a machine learning model for network threat detection.
Uses Random Forest classifier to identify malicious traffic patterns.
"""

import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

class ThreatDetectionModel:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = None
        
    def load_data(self, data_path):
        """Load the dataset."""
        print(f"Loading data from {data_path}...")
        df = pd.read_csv(data_path)
        print(f"Loaded {len(df)} samples")
        return df
    
    def prepare_data(self, df):
        """Prepare features and labels."""
        X = df.drop('label', axis=1)
        y = df['label']
        self.feature_names = X.columns.tolist()
        return X, y
    
    def train(self, data_path):
        """Train the threat detection model."""
        # Load and prepare data
        df = self.load_data(data_path)
        X, y = self.prepare_data(df)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Random Forest model
        print("Training Random Forest model...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test_scaled)
        y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]
        
        print("\n=== MODEL EVALUATION ===")
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Normal', 'Malicious']))
        print(f"\nROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")
        
        # Feature importance
        print("\n=== TOP 5 IMPORTANT FEATURES ===")
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        print(feature_importance.head())
        
        return self.model
    
    def save_model(self, model_dir):
        """Save the trained model and scaler."""
        os.makedirs(model_dir, exist_ok=True)
        
        model_path = os.path.join(model_dir, 'threat_detector.joblib')
        scaler_path = os.path.join(model_dir, 'scaler.joblib')
        
        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler, scaler_path)
        
        print(f"\nModel saved to {model_path}")
        print(f"Scaler saved to {scaler_path}")
    
    def load_model(self, model_dir):
        """Load a previously trained model."""
        model_path = os.path.join(model_dir, 'threat_detector.joblib')
        scaler_path = os.path.join(model_dir, 'scaler.joblib')
        
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        print(f"Model loaded from {model_path}")
    
    def predict(self, features):
        """Make a prediction on new data."""
        features_scaled = self.scaler.transform([features])
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0][1]
        return prediction, probability

def main():
    # Paths
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(project_root, 'data', 'network_traffic.csv')
    model_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if data exists
    if not os.path.exists(data_path):
        print("Data not found. Please run data/generate_data.py first.")
        return
    
    # Create and train model
    detector = ThreatDetectionModel()
    detector.train(data_path)
    detector.save_model(model_dir)
    
    print("\n✓ Model training complete!")

if __name__ == '__main__':
    main()
