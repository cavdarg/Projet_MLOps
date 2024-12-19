from sklearn.datasets import load_iris
import pandas as pd

# Charger le dataset Iris
data = load_iris()

# Créer un DataFrame avec les caractéristiques
df = pd.DataFrame(data.data, columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'])

# Ajouter les cibles (types de fleurs)
df['target'] = data.target

# Sauvegarder au format CSV
df.to_csv('iris.csv', index=False)
print("Le fichier 'iris.csv' a été généré.")
