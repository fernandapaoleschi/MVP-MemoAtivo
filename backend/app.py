import json
from flask import Flask, jsonify
from flask_cors import CORS

# --- SETUP INICIAL ---
# Cria a aplicação Flask
app = Flask(__name__)
# Habilita o CORS para permitir que o front-end acesse a API
CORS(app)

# --- FUNÇÃO AUXILIAR ---
# Uma função para carregar os dados do nosso "banco de dados"
def load_data():
    """Abre e lê o ficheiro database.json."""
    try:
        with open('database.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Se o ficheiro não existir, retorna uma estrutura vazia
        return {"categories": []}

# --- ENDPOINTS DA API ---

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """
    Este endpoint lê todas as categorias do banco de dados, calcula um resumo
    para cada uma e retorna para o front-end.
    """
    data = load_data()
    summaries = []

    for category in data.get('categories', []):
        total_sets = 0
        total_cards = 0
        
        for subtopic in category.get('subtopics', []):
            total_sets += len(subtopic.get('sets', []))
            
            # CORREÇÃO: A variável 'for-set' foi alterada para 'study_set'
            for study_set in subtopic.get('sets', []):
                total_cards += len(study_set.get('flashcards', []))

        summaries.append({
            'id': category.get('id'),
            'name': category.get('name'),
            'totalSets': total_sets,
            'totalCards': total_cards,
            'cardsToReview': 0  # Lógica de revisão a ser implementada
        })
    
    return jsonify(summaries)

# --- EXECUÇÃO DO SERVIDOR ---
if __name__ == '__main__':
    app.run(debug=True)
