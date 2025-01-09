
from flask import Flask, render_template, request, redirect, url_for, send_file
import json
import os

app = Flask(__name__)
DATA_FILE = 'items.json'
ITEMS_FORNEC_FILE = 'itens_fornec.json'

if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))
    app.run(host='0.0.0.0', port=port)

# Funções auxiliares para manipular o JSON
def load_items():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

def save_items(items):
    with open(DATA_FILE, 'w') as file:
        json.dump(items, file, indent=4)

def load_items_fornec():
    if os.path.exists(ITEMS_FORNEC_FILE):
        with open(ITEMS_FORNEC_FILE, 'r') as file:
            return json.load(file)
    return []

def save_items_fornec(items):
    with open(ITEMS_FORNEC_FILE, 'w') as file:
        json.dump(items, file, indent=4)

# Rota para o Index
@app.route('/')
def index():
    return render_template('index.html')

# ================================================================== Baker ============================================================

# Rota para a lista de itens para o padeiro
@app.route('/list_to_the_baker', methods=['GET', 'POST'])
def list_to_the_baker():
    items = load_items()
    if request.method == 'POST':
        item_name = request.form['item']
        # quantity = request.form['quantity']
        observation = request.form.get('observation', '')
        
        item_id = len(items) + 1
        items.append({'id': item_id, 'item': item_name, """'quantity': quantity,""" 'observation': observation})
        save_items(items)
        return redirect(url_for('list_to_the_baker'))
    return render_template('list_to_the_baker.html', items=items)

# Adicionar item à lista do padeiro
@app.route('/add_item_baker', methods=['POST'])
def add_item_baker():
    item_name = request.form['item']
    # quantity = request.form['quantity']
    observation = request.form.get('observation', '')

    items = load_items()
    item_id = len(items) + 1
    items.append({'id': item_id, 'item': item_name, """'quantity': quantity,""" 'observation': observation})
    save_items(items)

    return redirect(url_for('list_to_the_baker'))

# Rota para remover um item do padeiro
@app.route('/remove_item_baker', methods=['POST'])
def remove_item():
    item_id = int(request.form['item_id'])
    items = load_items()
    items = [item for item in items if item['id'] != item_id]
    save_items(items)
    return redirect(url_for('list_to_the_baker'))

# Rota para editar um item do padeiro
@app.route('/edit_item_baker', methods=['POST'])
def edit_item():
    item_id = int(request.form['item_id'])
    new_item = request.form['item']
    # new_quantity = request.form['quantity']
    new_observation = request.form.get('observation', '')

    items = load_items()
    for item in items:
        if item['id'] == item_id:
            item['item'] = new_item
            # item['quantity'] = new_quantity
            item['observation'] = new_observation
            break

    save_items(items)
    return redirect(url_for('list_to_the_baker'))

# ================================================================== Fornec ============================================================

# Rota para a lista de itens do fornecedor
@app.route('/list_to_the_fornec', methods=['GET', 'POST'])
def list_to_the_fornec():
    items_fornec = load_items_fornec()  # Carrega os itens do fornecedor
    if request.method == 'POST':
        item_name = request.form['item']
        # quantity = request.form['quantity']
        observation = request.form.get('observation', '')
        
        item_id = len(items_fornec) + 1
        items_fornec.append({'id': item_id, 'item': item_name, """'quantity': quantity,""" 'observation': observation})
        save_items_fornec(items_fornec)  # Salva no arquivo itens_fornec.json
        return redirect(url_for('list_to_the_fornec'))
    return render_template('list_to_the_fornec.html', items=items_fornec)


@app.route('/add_item_fornec', methods=['POST'])
def add_item_fornec():
    item_name = request.form['item']
    # quantity = request.form['quantity']
    observation = request.form.get('observation', '')

    items_fornec = load_items_fornec()  # Carrega os itens do fornecedor
    item_id = len(items_fornec) + 1
    items_fornec.append({'id': item_id, 'item': item_name, """'quantity': quantity,""" 'observation': observation})
    save_items_fornec(items_fornec)  # Salva no arquivo itens_fornec.json

    return redirect(url_for('list_to_the_fornec'))


@app.route('/remove_item_fornec', methods=['POST'])
def remove_item_fornec():
    item_id = int(request.form['item_id'])
    items_fornec = load_items_fornec()
    items_fornec = [item for item in items_fornec if item['id'] != item_id]
    save_items_fornec(items_fornec)  # Salva a lista atualizada
    return redirect(url_for('list_to_the_fornec'))


@app.route('/edit_item_fornec', methods=['POST'])
def edit_item_fornec():
    item_id = int(request.form['item_id'])
    new_item = request.form['item']
    # new_quantity = request.form['quantity']
    new_observation = request.form.get('observation', '')

    items_fornec = load_items_fornec()
    for item in items_fornec:
        if item['id'] == item_id:
            item['item'] = new_item
            # item['quantity'] = new_quantity
            item['observation'] = new_observation
            break

    save_items_fornec(items_fornec)  # Salva a lista atualizada
    return redirect(url_for('list_to_the_fornec'))

if __name__ == '__main__':
    app.run(debug=True)
