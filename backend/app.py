from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory database for tenders
tenders = []
tender_id_counter = 1

# Endpoint to list all tenders
@app.route('/tenders', methods=['GET'])
def get_tenders():
    return jsonify(tenders), 200

# Endpoint to get a specific tender by ID
@app.route('/tenders/<int:tender_id>', methods=['GET'])
def get_tender(tender_id):
    tender = next((tender for tender in tenders if tender['id'] == tender_id), None)
    if tender is None:
        abort(404, description="Tender not found")
    return jsonify(tender), 200

# Endpoint to create a new tender
@app.route('/tenders', methods=['POST'])
def create_tender():
    global tender_id_counter
    if not request.json or 'name' not in request.json or 'description' not in request.json:
        abort(400, description="Name and description are required")
    
    new_tender = {
        'id': tender_id_counter,
        'name': request.json['name'],
        'description': request.json['description'],
        'status': 'open'
    }
    tenders.append(new_tender)
    tender_id_counter += 1
    return jsonify(new_tender), 201

# Endpoint to update a tender's status (close/open)
@app.route('/tenders/<int:tender_id>', methods=['PUT'])
def update_tender(tender_id):
    tender = next((tender for tender in tenders if tender['id'] == tender_id), None)
    if tender is None:
        abort(404, description="Tender not found")
    
    if 'status' in request.json:
        tender['status'] = request.json['status']
    
    return jsonify(tender), 200

# Endpoint to delete a tender
@app.route('/tenders/<int:tender_id>', methods=['DELETE'])
def delete_tender(tender_id):
    tender = next((tender for tender in tenders if tender['id'] == tender_id), None)
    if tender is None:
        abort(404, description="Tender not found")
    
    tenders.remove(tender)
    return jsonify({"message": "Tender deleted"}), 200

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error)}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)