import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn
import random

# Configurer MLflow Tracking URI
mlflow.set_tracking_uri("file:./mlruns")
EXPERIMENT_NAME = "Iris RandomForest Experiment"
mlflow.set_experiment(EXPERIMENT_NAME)

# Charger les données
df = pd.read_csv('iris.csv')
X = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
y = df['target']

# Diviser les données
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Définir les plages de recherche des hyperparamètres
HYPERPARAMS_SPACE = {
    "n_estimators": [10, 50, 100],
    "max_depth": [None, 5, 10],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 3, 5],
    "criterion": ["gini", "entropy"]
}

# Effectuer une recherche aléatoire sur les hyperparamètres
best_accuracy = 0
best_hyperparams = None

for i in range(10):  # Par exemple, tester 10 combinaisons aléatoires
    # Générer une combinaison aléatoire d'hyperparamètres
    hyperparams = {
        "n_estimators": random.choice(HYPERPARAMS_SPACE["n_estimators"]),
        "max_depth": random.choice(HYPERPARAMS_SPACE["max_depth"]),
        "min_samples_split": random.choice(HYPERPARAMS_SPACE["min_samples_split"]),
        "min_samples_leaf": random.choice(HYPERPARAMS_SPACE["min_samples_leaf"]),
        "criterion": random.choice(HYPERPARAMS_SPACE["criterion"]),
        "random_state": 42
    }
    
    # Entraîner le modèle
    model = RandomForestClassifier(**hyperparams)
    model.fit(X_train, y_train)
    
    # Évaluer le modèle
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test {i + 1}: Accuracy: {accuracy * 100:.2f}% - Hyperparams: {hyperparams}")
    
    # Enregistrer les résultats dans MLflow
    with mlflow.start_run():
        for param, value in hyperparams.items():
            mlflow.log_param(param, value)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(model, "model")
        
        run_id = mlflow.active_run().info.run_id
        print(f"Modèle enregistré avec RUN_ID: {run_id}")
        
        # Mettre à jour le meilleur modèle si nécessaire
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_hyperparams = hyperparams

print("\n--- Résultats ---")
print(f"Meilleur modèle : Accuracy: {best_accuracy * 100:.2f}% - Hyperparams: {best_hyperparams}")
