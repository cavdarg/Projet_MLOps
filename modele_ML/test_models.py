import mlflow.sklearn
import pandas as pd

# Liste des RUN_ID des modèles
RUN_IDS = [
    
    "4337d71ff5254040917c2542a4d97157"  # Modèle 4

]

# Exemple de données pour les prédictions
sample = [[6.1, 3.5, 2.4, 0.2]]  # Exemple d'entrée

# Initialiser une liste pour stocker les résultats
results = []

# Tester chaque modèle
for run_id in RUN_IDS:
    print(f"--- Test du modèle avec RUN_ID: {run_id} ---")
    try:
        # Charger le modèle depuis MLflow
        model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")

        # Faire une prédiction
        prediction = model.predict(sample)

        # Ajouter les résultats dans la liste
        results.append({"RUN_ID": run_id, "Prediction": prediction[0]})
        print(f"Prédiction : {prediction}\n")
    except Exception as e:
        # Enregistrer les erreurs dans les résultats
        results.append({"RUN_ID": run_id, "Prediction": f"Erreur: {e}"})
        print(f"Erreur lors du chargement ou de la prédiction pour le RUN_ID {run_id}: {e}\n")

# Convertir les résultats en DataFrame pour une visualisation claire
df_results = pd.DataFrame(results)

# Afficher les résultats
print("--- Résultats des prédictions ---")
print(df_results)

# Sauvegarder les résultats dans un fichier CSV (optionnel)
df_results.to_csv("model_predictions.csv", index=False)
print("Résultats sauvegardés dans 'model_predictions.csv'")
