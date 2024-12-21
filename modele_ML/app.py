from flask import Flask, request, jsonify, Response
import mlflow
import mlflow.sklearn
import os
from prometheus_client import start_http_server, Summary, Counter, Gauge, generate_latest

app = Flask(__name__)

# Définir les métriques
REQUEST_COUNT = Counter('request_count', 'Nombre de requêtes reçues', ['method', 'endpoint'])
IN_PROGRESS = Gauge('in_progress', 'Requêtes en cours')
REQUEST_LATENCY = Summary('request_latency_seconds', 'Temps d\'exécution des requêtes')

# Exemple de middleware pour mesurer les métriques
@app.before_request
def before_request():
    IN_PROGRESS.inc()
    REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()

@app.after_request
def after_request(response):
    IN_PROGRESS.dec()
    return response

# Définir l'expérience MLflow et configurer l'URI
EXPERIMENT_NAME = "Iris RandomForest Experiment"
if os.environ.get("DOCKER_ENV", False):
    mlflow.set_tracking_uri("file:/app/mlruns")
else:
    mlflow.set_tracking_uri("file:./mlruns")
print(f"MLflow Tracking URI configuré : {mlflow.get_tracking_uri()}")

# Charger le meilleur modèle à partir des métadonnées MLflow
try:
    runs = mlflow.search_runs(experiment_names=[EXPERIMENT_NAME], order_by=["metrics.accuracy DESC"])
    if len(runs) > 0:
        best_run = runs.iloc[0]
        RUN_ID = best_run['run_id']
        print(f"Tentative de chargement du meilleur modèle pour RUN_ID : {RUN_ID}...")
        model = mlflow.sklearn.load_model(f"runs:/{RUN_ID}/model")
        print("Modèle chargé avec succès.")
    else:
        raise Exception("Aucun modèle disponible dans l'expérience MLflow.")
except Exception as e:
    print(f"Erreur lors du chargement du modèle : {e}")
    model = None

# Vérifier si le modèle est disponible
if model is None:
    print("Erreur critique : Aucun modèle n'est disponible. L'application ne pourra pas servir de prédictions.")
    exit(1)  # Quitter proprement si aucun modèle n'est disponible

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({"error": "Aucun modèle disponible pour faire des prédictions."}), 500
    try:
        data = request.get_json()
        features = data.get("features", [])
        if not features:
            return jsonify({"error": "No features provided"}), 400
        predictions = model.predict(features)
        return jsonify({"predictions": predictions.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "running"}), 200

# Endpoint /metrics
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

