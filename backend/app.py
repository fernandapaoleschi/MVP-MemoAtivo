from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # permite que o frontend acesse a API

# Função para carregar o banco de dados JSON
def load_db():
    with open("database.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------------------
# Backend Matheus (API básica)
# ---------------------------

# Endpoint: GET /api/categories
# Retorna um resumo das categorias
@app.route("/api/categories", methods=["GET"])
def get_categories():
    db = load_db()
    resumo = []
    for cat in db["categories"]:
        total_sets = len(cat["sets"])
        total_flashcards = sum(len(s["flashcards"]) for s in cat["sets"])
        resumo.append({
            "id": cat["id"],
            "nome": cat["nome"],
            "total_sets": total_sets,
            "total_flashcards": total_flashcards
        })
    return jsonify(resumo)


# ---------------------------
# Backend Felipe (Lógica extra)
# ---------------------------

# Endpoint: GET /api/categories/<id>/sets
# Retorna apenas os conjuntos de uma categoria
@app.route("/api/categories/<int:category_id>/sets", methods=["GET"])
def get_sets(category_id):
    db = load_db()
    for cat in db["categories"]:
        if cat["id"] == category_id:
            return jsonify(cat["sets"])
    return jsonify({"erro": "Categoria não encontrada"}), 404


# (planejamento para o Dia 2: criar novos endpoints POST/PUT/DELETE)

# Rodar servidor
if __name__ == "__main__":
    app.run(debug=True)
