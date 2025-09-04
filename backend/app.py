import json
import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS

# --- SETUP INICIAL ---
app = Flask(__name__)
CORS(app)

# --- FUNÇÕES AUXILIARES ---
def load_data():
    """Abre e lê o ficheiro database.json de forma segura."""
    try:
        with open('database.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'categories' not in data or not isinstance(data['categories'], list):
                data = {'categories': []}
            return data
    except (FileNotFoundError, json.JSONDecodeError):
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
        if not isinstance(category, dict): continue
        total_sets = 0
        total_cards = 0
        for subtopic in category.get('subtopics', []):
            if not isinstance(subtopic, dict): continue
            total_sets += len(subtopic.get('sets', []))
            for study_set in subtopic.get('sets', []):
                if not isinstance(study_set, dict): continue
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
    if not new_category_data or not new_category_data.get('name'):
        return jsonify({'error': 'O nome da categoria é obrigatório'}), 400
    
    category_name = new_category_data['name']
    new_category = { "id": f"cat-{uuid.uuid4()}", "name": category_name, "subtopics": [] }
    data.setdefault('categories', []).append(new_category)
    save_data(data)
    return jsonify(new_category), 201

@app.route('/api/categories/<category_id>/subtopics', methods=['GET'])
def get_subtopics(category_id):
    """Endpoint para LER os sub-tópicos de uma categoria."""
    data = load_data()
    category = next((cat for cat in data.get('categories', []) if isinstance(cat, dict) and cat.get('id') == category_id), None)
    if not category: return jsonify({'error': 'Categoria não encontrada'}), 404
    
    summaries = []
    for subtopic in category.get('subtopics', []):
        if not isinstance(subtopic, dict): continue
        total_sets = len(subtopic.get('sets', []))
        total_cards = sum(len(s.get('flashcards', [])) for s in subtopic.get('sets', []) if isinstance(s, dict))
        summaries.append({
            'id': subtopic.get('id'),
            'name': subtopic.get('name'),
            'totalSets': total_sets,
            'totalCards': total_cards
        })
    return jsonify(summaries)

@app.route('/api/categories/<category_id>/subtopics', methods=['POST'])
def add_subtopic(category_id):
    """Endpoint para ADICIONAR um novo sub-tópico a uma categoria."""
    data = load_data()
    category = next((cat for cat in data.get('categories', []) if isinstance(cat, dict) and cat.get('id') == category_id), None)
    if not category: return jsonify({'error': 'Categoria não encontrada'}), 404

    new_subtopic_data = request.json
    if not new_subtopic_data or not new_subtopic_data.get('name'):
        return jsonify({'error': 'O nome do sub-tópico é obrigatório'}), 400

    subtopic_name = new_subtopic_data['name']
    new_subtopic = { "id": f"sub-{uuid.uuid4()}", "name": subtopic_name, "sets": [] }
    category.setdefault('subtopics', []).append(new_subtopic)
    save_data(data)
    return jsonify(new_subtopic), 201

# --- NOVOS ENDPOINTS PARA CONJUNTOS (SETS) ---

@app.route('/api/categories/<category_id>/subtopics/<subtopic_id>/sets', methods=['GET'])
def get_sets(category_id, subtopic_id):
    """Endpoint para LER os conjuntos de um sub-tópico."""
    data = load_data()
    category = next((cat for cat in data.get('categories', []) if isinstance(cat, dict) and cat.get('id') == category_id), None)
    if not category: return jsonify({'error': 'Categoria não encontrada'}), 404
    
    subtopic = next((sub for sub in category.get('subtopics', []) if isinstance(sub, dict) and sub.get('id') == subtopic_id), None)
    if not subtopic: return jsonify({'error': 'Sub-tópico não encontrado'}), 404

    return jsonify(subtopic.get('sets', []))

@app.route('/api/categories/<category_id>/subtopics/<subtopic_id>/sets', methods=['POST'])
def add_set(category_id, subtopic_id):
    """Endpoint para ADICIONAR um novo conjunto a um sub-tópico."""
    data = load_data()
    category = next((cat for cat in data.get('categories', []) if isinstance(cat, dict) and cat.get('id') == category_id), None)
    if not category: return jsonify({'error': 'Categoria não encontrada'}), 404

    subtopic = next((sub for sub in category.get('subtopics', []) if isinstance(sub, dict) and sub.get('id') == subtopic_id), None)
    if not subtopic: return jsonify({'error': 'Sub-tópico não encontrado'}), 404

    new_set_data = request.json
    if not new_set_data or not new_set_data.get('name'):
        return jsonify({'error': 'O nome do conjunto é obrigatório'}), 400

    set_name = new_set_data['name']
    new_set = { "id": f"set-{uuid.uuid4()}", "name": set_name, "flashcards": [] }
    subtopic.setdefault('sets', []).append(new_set)
    save_data(data)
    return jsonify(new_set), 201

# --- EXECUÇÃO DO SERVIDOR ---
if __name__ == '__main__':
    app.run(debug=True)