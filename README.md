# **Projet : Pipeline d'Entraînement et de déploiement d'un Modèle ML avec Docker et MLflow**

Ce projet utilise le dataset **Iris** pour créer un modèle de classification basé sur **RandomForestClassifier**. Il inclut une **pipeline d'entraînement automatisée**, un **suivi des expériences avec MLflow**, la **conteneurisation de l'API Flask et de la pipeline**, et des instructions pour un déploiement automatisé.

---

## **Structure du Projet**
```
Projet_MLOps/
├── modele_ML/
│   ├── mlruns/                # Dossier contenant les artefacts des expériences MLflow
│   ├── docker_images/         # Contient les images Docker exportées
│   │   ├── app-api.tar        # Image Docker pour app.py
│   │   └── pipeline-job.tar   # Image Docker pour pipeline.py
│   ├── export_iris.py         # Script pour exporter le dataset Iris en CSV
│   ├── iris.csv               # Dataset généré à partir de scikit-learn
│   ├── model_predictions.csv  # Fichier contenant les prédictions des modèles
│   ├── pipeline.py            # Pipeline automatisée d'entraînement et de sélection de modèle
│   ├── app.py                 # API Flask pour servir le modèle
│   ├── train.py               # Script pour entraîner le modèle avec des hyperparamètres
│   ├── test_models.py         # Script pour charger et tester les modèles
│   ├── deploy.py              # Script pour déployer l'API après entraînement
│   ├── Dockerfile_app         # Dockerfile pour app.py
│   ├── Dockerfile_pipeline    # Dockerfile pour pipeline.py
│   ├── requirements.txt       # Liste des dépendances Python
├── terraform/                 # Répertoire pour le provisionnement de l'infrastructure AWS
│   ├── main.tf                # Configuration principale de Terraform
│   ├── variables.tf           # Variables Terraform
│   ├── outputs.tf             # Outputs Terraform
│   └── myKey.pem              # Clé SSH pour l'accès à l'instance EC2
├── ansible/                   # Répertoire pour la configuration des serveurs
│   ├── playbook.yml           # Playbook principal Ansible
│   ├── inventory.ini          # Inventaire des serveurs
│   └── roles/                 # Rôles Ansible
│       ├── docker_install/    # Installation de Docker
│       │   └── tasks/main.yml
│       ├── transfer_image/    # Transfert des images Docker
│       │   └── tasks/main.yml
│       └── deploy_app/        # Déploiement de l'application
│           └── tasks/main.yml
│
│── README.md                    # Documentation du projet
```

---

## **Dépendances**
Voici les bibliothèques requises pour ce projet (ajoutées dans `requirements.txt`) :
```
mlflow==2.19.0
cloudpickle==3.1.0
numpy==2.1.3
pandas==2.2.3
scikit-learn==1.6.0
scipy==1.14.1
flask==2.3.2
```

---

## **Étape 1 : Installation et Configuration**

1. **Cloner le projet** :
   ```bash
   git clone <lien-du-repo>
   cd modele_ML
   ```

2. **Créer un environnement virtuel** :
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # Sous Windows : myenv\Scripts\activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

---

## **Étape 2 : Générer le Dataset Iris**
1. Exécutez le script `export_iris.py` pour générer le fichier `iris.csv` :
   ```bash
   python export_iris.py
   ```
2. Le fichier `iris.csv` sera créé dans le répertoire courant.

---

## **Étape 3 : Entraîner le Modèle**
1. Lancez le script `train.py` pour entraîner un modèle RandomForest avec des hyperparamètres optimisés :
   ```bash
   python train.py
   ```
2. Les hyperparamètres par défaut sont :
   - `n_estimators = 50` (nombre d'arbres)
   - `max_depth = 5` (profondeur maximale)
   - `min_samples_split = 10` (nombre minimum d'échantillons pour un split)
   - `min_samples_leaf = 5` (nombre minimum d'échantillons par feuille)
   - `criterion = 'gini'` (critère de division)

   Vous pouvez modifier ces valeurs dans le fichier `train.py` pour tester d'autres configurations.

3. **Validation croisée** :
   Le script inclut une validation croisée pour évaluer la robustesse du modèle sur plusieurs sous-ensembles.

4. **Suivi des résultats avec MLflow** :
   Les métriques (ex. : `accuracy`) et les hyperparamètres sont logués dans MLflow.

   Pour visualiser les résultats, démarrez le serveur MLflow :
   ```bash
   mlflow ui
   ```
   Accédez à l'interface ici : [http://localhost:5000](http://localhost:5000).

---

## **Étape 4 : Charger un Modèle et Faire une Prédiction**
1. Trouvez l'identifiant du run (`RUN_ID`) dans l'interface MLflow :
   - Ouvrez une exécution dans l'interface.
   - Copiez le **Run ID**.

2. Ajoutez ce `RUN_ID` dans le script `test_models.py` pour tester les prédictions du modèle :

   Exemple de prédiction dans `test_models.py` :
   ```python
   sample = [[6.1, 3.5, 2.4, 0.2]]  # Longueur/Largeur du sépale et pétale
   ```

   *Les prédictions permettent de savoir à quelle espèce correspond la fleur avec ces dimensions de pétales/sépales : 
   - Si la valeur retrounée est 0 -> Setosa
   - Si la valeur retrounée est 1 -> Versicolor
   - Si la valeur retrounée est 2 -> Virginica


3. Exécutez le script :
   ```bash
   python test_models.py
   ```
4. Les prédictions et erreurs (s'il y en a) seront affichées dans le terminal et sauvegardées dans `model_predictions.csv`.

---

## **Étape 5 : Enrichir le Dataset**
Pour enrichir le dataset et réduire les risques de sur-apprentissage :

   **Ajoutez du bruit dans les données d'entraînment** :
   Une petite variation est ajoutée aux données pour les rendre plus robustes.

---

## **Étape 6 : Pipeline d'Entraînement Automatique**

### **Script pipeline.py**
1. **Description** :
   - Entraîne automatiquement le modèle.
   - Compare les performances avec les anciens modèles dans **MLflow**.
   - Sélectionne le meilleur modèle pour le déploiement.

2. **Exécution** :
   ```bash
   python pipeline.py
   ```

   Les modèles sont sauvegardés et versionnés dans **MLflow**.

---

## **Étape 7 : API Flask pour Servir le Modèle**

### **Script app.py**
1. **Description** :
   - Sert le meilleur modèle pour répondre aux requêtes de prédictions.
   - Le modèle est chargé depuis **MLflow**.

2. **Exécution** :
   ```bash
   python app.py
   ```
3. **Test** :

   ```bash
   curl -X POST -H "Content-Type: application/json" \
   -d '{"features": [[5.1, 3.5, 1.4, 0.2]]}' \
   http://localhost:5000/predict
   ```
   **Réponse attendue** :
   ```json
   {"predictions": [0]}
   ```
   L'API peut être testée avec une entrée en JSON dans POSTMAN par exemple.


---

## **Étape 8 : Conteneurisation avec Docker**

### **Dockerfile_pipeline** (pour pipeline.py)
```Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "pipeline.py"]
```

### **Dockerfile_app** (pour app.py)
```Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
```

### **Construire et Exporter les Images Docker**

1. **Naviguer dans `modele_ML`** :
   ```bash
   cd modele_ML
   ```

2. **Construire et sauvegarder l'image pour pipeline.py** :
   ```bash
   docker build -t pipeline-job -f Dockerfile_pipeline .
   docker save -o docker_images/pipeline-job.tar pipeline-job
   ```

3. **Construire et sauvegarder l'image pour app.py** :
   ```bash
   docker build -t app-api -f Dockerfile_app .
   docker save -o docker_images/app-api.tar app-api
   ```

---

## **Étape 9 : Construire les Images Docker**

1. **Construire l'image pour pipeline.py** :
   ```bash
   docker build -t pipeline-job -f Dockerfile_pipeline .
   ```

2. **Construire l'image pour app.py** :
   ```bash
   docker build -t app-api -f Dockerfile_app .
   ```

---

## **Étape 10 : Exécuter la Pipeline et Déployer l'API**

### **1. Exécution du pipeline pour entraîner le modèle**
```bash
docker run --rm -v $(pwd)/mlruns:/app/mlruns pipeline-job
```
   - **Option `-v`** : Monte le répertoire `mlruns` local dans le conteneur pour partager les artefacts MLflow.

### **2. Déployer l'API Flask avec le meilleur modèle**
```bash
docker run -d -p 5000:5000 --name app-api-container -v $(pwd)/mlruns:/app/mlruns app-api
```
   - **Option `-p 5000:5000`** : Expose le port 5000 pour accéder à l'API.
   - **Option `-v`** : Partage les artefacts MLflow entre la pipeline et l'API.

---

## **Étape 11 : Automatisation avec deploy.py**

Le script `deploy.py` automatise l'exécution de la pipeline et le redéploiement de l'API Flask avec le meilleur modèle.

**Exécution** :
```bash
python deploy.py
```

---

## **Étape 12 : Tester l'API**

1. **Tester la prédiction** :
   ```bash
   curl -X POST -H "Content-Type: application/json" \
   -d '{"features": [[5.1, 3.5, 1.4, 0.2]]}' \
   http://localhost:5000/predict
   ```
   **Réponse attendue** :
   ```json
   {"predictions": [0]}
   ```

2. **Vérifier la santé de l'API** :
   ```bash
   curl http://localhost:5000/health
   ```
   **Réponse attendue** :
   ```json
   {"status": "running"}
   ```

---

# **Étape 13 : Déploiement sur AWS avec Terraform et Ansible**

Le déploiement sur AWS EC2 est réalisé grâce à Terraform pour provisionner l'infrastructure et Ansible pour configurer l'instance et déployer les conteneurs Docker.

## 1 : Pré-requis**

### **Outils nécessaires**

- **Terraform** pour provisionner l'infrastructure.
- **Ansible** pour configurer les serveurs.
- **Docker** pour conteneuriser l'application.

### **Clé SSH**

- Placez votre clé privée `myKey.pem` dans le répertoire `terraform/`.

### **AWS Credentials**

- Assurez-vous que vos clés AWS (`credentials`) sont configurées dans :
  - Sous Linux : `~/.aws/credentials`
  - Sous Windows : `C:\Users\<VotreNom>\.aws\credentials`

---

## 2 : Installer les Dépendances**

### **Terraform**

1. Téléchargez Terraform depuis [Terraform Downloads](https://www.terraform.io/downloads).
2. Placez le binaire Terraform dans votre `PATH`.
3. Vérifiez l'installation :
   ```bash
   terraform --version
   ```

### **Ansible**

1. Installez Ansible :
   ```bash
   sudo apt update
   sudo apt install ansible -y
   ```
2. Vérifiez l'installation :
   ```bash
   ansible --version
   ```

### **Docker**

1. Installez Docker sur votre machine locale :
   ```bash
   sudo apt update
   sudo apt install docker.io -y
   ```
2. Vérifiez l'installation :
   ```bash
   docker --version
   ```

---

### **Terraform**

1. **Naviguer dans le répertoire Terraform** :
   ```bash
   cd ../terraform
   ```

2. **Initialiser Terraform** :
   ```bash
   terraform init
   ```

3. **Visualiser le plan** :
   ```bash
   terraform plan
   ```

4. **Appliquer les modifications** :
   ```bash
   terraform apply
   ```

5. **Récupérer l'IP publique de l'instance EC2** :
   ```bash
   terraform output instance_ip
   ```

### **Ansible**
1. **Mettre à jour l'inventaire Ansible** :
   Dans `ansible/inventory.ini`, remplacez `<EC2_PUBLIC_IP>` par l'IP publique de l'instance EC2 :
   ```ini
   [ml_api]
   <EC2_PUBLIC_IP> ansible_user=ubuntu ansible_ssh_private_key_file=../terraform/myKey.pem
   ```

2. **Exécuter le Playbook Ansible** :
   ```bash
   cd ../ansible
   ansible-playbook -i inventory.ini playbook.yml
   ```

---

## **Étape 14 : Tester l'API**

### **Tester localement sur l'instance EC2** :
1. Connectez-vous à l'instance EC2 :
   ```bash
   ssh -i ../terraform/myKey.pem ubuntu@<EC2_PUBLIC_IP>
   ```
2. Testez l'API avec `curl` :
   ```bash
   curl -X POST -H "Content-Type: application/json" \
   -d '{"features": [[5.1, 3.5, 1.4, 0.2]]}' \
   http://127.0.0.1:5000/predict
   ```

### **Tester depuis votre machine locale** :
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"features": [[5.1, 3.5, 1.4, 0.2]]}' \
http://<EC2_PUBLIC_IP>:5000/predict
```

---

## **Nettoyage des Ressources**
Pour éviter les coûts inutiles, supprimez les ressources AWS après usage :
```bash
terraform destroy
```

---
