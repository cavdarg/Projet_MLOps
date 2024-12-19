import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import mlflow
import mlflow.sklearn

# Charger le dataset depuis iris.csv
df = pd.read_csv('iris.csv')
X = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
y = df['target']

# Diviser les données en ensemble d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Ajouter un bruit aléatoire aux données d'entraînement
noise = np.random.normal(0, 0.1, X_train.shape)
X_train_noisy = X_train + noise


# Configurer MLflow pour suivre les expériences
EXPERIMENT_NAME = "Iris RandomForest Experiment"
mlflow.set_experiment(EXPERIMENT_NAME)

# Hyperparamètres (centralisés pour cohérence)
HYPERPARAMS = {
    "n_estimators": 50,      # Réduction du nombre d'arbres pour éviter la complexité excessive
    "max_depth": 5,          # Profondeur max des arbres
    "min_samples_split": 10, # Minimum d'échantillons pour splitter un noeud
    "min_samples_leaf": 5,   # Minimum d'échantillons pour une feuille
    "criterion": "gini",     # Utilisation du critère Gini (ou entropy)
    "random_state": 42
}

with mlflow.start_run():
    # Entraîner le modèle avec les hyperparamètres 
    model = RandomForestClassifier(**HYPERPARAMS)
    model.fit(X_train_noisy, y_train)

    # Validation croisée pour évaluer la généralisation
    scores = cross_val_score(model, X, y, cv=5)
    print(f"Validation croisée : {scores.mean() * 100:.2f}%")

    # Faire des prédictions
    y_pred = model.predict(X_test)

    # Calculer l'exactitude sur le test set
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy sur le test set : {accuracy * 100:.2f}%")

    # Loguer les hyperparamètres et les métriques dans MLflow
    for param, value in HYPERPARAMS.items():
        mlflow.log_param(param, value)
    mlflow.log_metric("accuracy", accuracy)

    # Enregistrer le modèle dans MLflow
    mlflow.sklearn.log_model(model, "model")
    print("Modèle sauvegardé dans MLflow.")