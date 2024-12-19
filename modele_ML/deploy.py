import os
import subprocess

# Configuration des images et volumes
PIPELINE_IMAGE = "pipeline-job"
API_IMAGE = "app-api"
API_CONTAINER_NAME = "app-api-container"
MLRUNS_VOLUME = os.path.abspath("mlruns")

def run_pipeline():
    """Exécuter le pipeline pour entraîner et enregistrer le modèle."""
    print("Exécution du pipeline...")
    subprocess.run([
        "docker", "run", "--rm", 
        "-v", f"{MLRUNS_VOLUME}:/app/mlruns", 
        PIPELINE_IMAGE
    ], check=True)
    print("Pipeline exécuté avec succès.")

def restart_api():
    """Redémarrer le conteneur de l'API avec le modèle mis à jour."""
    print("Arrêt et redémarrage de l'API Flask...")
    subprocess.run(["docker", "stop", API_CONTAINER_NAME], check=False)
    subprocess.run(["docker", "rm", API_CONTAINER_NAME], check=False)
    subprocess.run([
        "docker", "run", "-d", "--name", API_CONTAINER_NAME,
        "-p", "5000:5000", 
        "-v", f"{MLRUNS_VOLUME}:/app/mlruns", 
        API_IMAGE
    ], check=True)
    print("API Flask redémarrée avec succès.")

if __name__ == "__main__":
    run_pipeline()
    restart_api()
