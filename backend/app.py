import json
import uuid  # Usado para gerar IDs únicos
from flask import Flask, jsonify, request
from flask_cors import CORS

# --- SETUP INICIAL ---
app = Flask(__name__)
CORS(app)

# --- FUNÇÕES AUXILIARES ---
def load_data():
    """Abre e lê o ficheiro database.json."""
    try:
        with open('database.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"categories": []}

def save_data(data):
    """Guarda os dados atualizados no ficheiro database.json."""
    with open('database.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# --- ENDPOINTS DA API ---

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Endpoint para LER e retornar um resumo de todas as categorias."""
    data = load_data()
    summaries = []

    for category in data.get('categories', []):
        total_sets = 0
        total_cards = 0
        
        for subtopic in category.get('subtopics', []):
            total_sets += len(subtopic.get('sets', []))
            for study_set in subtopic.get('sets', []):
                total_cards += len(study_set.get('flashcards', []))

        summaries.append({
            'id': category.get('id'),
            'name': category.get('name'),
            'totalSets': total_sets,
            'totalCards': total_cards,
            'cardsToReview': 0
        })
    
    return jsonify(summaries)

@app.route('/api/categories', methods=['POST'])
def add_category():
    """Endpoint para ADICIONAR uma nova categoria."""
    data = load_data()
    new_category_data = request.json

    # Validação simples para garantir que o nome foi enviado
    if not new_category_data or 'name' not in new_category_data:
        return jsonify({'error': 'O nome da categoria é obrigatório'}), 400

    category_name = new_category_data['name']

    # Estrutura da nova categoria
    new_category = {
        "id": f"cat-{uuid.uuid4()}", # Gera um ID único
        "name": category_name,
        "subtopics": []
    }

    data['categories'].append(new_category)
    save_data(data)

    # Retorna a categoria recém-criada com o status 201 (Created)
    return jsonify(new_category), 201

# --- EXECUÇÃO DO SERVIDOR ---
if __name__ == '__main__':
    app.run(debug=True)

