from flask import request, jsonify
from .config import db, app
from api.utils.debuggernaut import heimdahl, laufeyspawn, jotunbane

@app.route('/ping', methods = ['GET'])
def pong():
    return jsonify({'message': 'pong'}), 200

@app.route('/', methods = ['GET'])
def root():
    '''
    Basic health check route.
    '''
    return jsonify({
        'message': 'Paperclip Adjacent API is running',
        'status': 'OK'
    }), 200

@laufeyspawn(summoned = False)
@app.route('/memcells', methods = ['GET'])
def get_all_memcells():
    '''
    Return all memcells in the database.

    Returns:
    -------
    JSON response containing all memcells.
    '''
    heimdahl('GET /memcells called', unveil = True, threat = 1)
    return jsonify([dict(cell) for cell in db.all])

@laufeyspawn(summoned = False)
@app.route('/memcells', methods = ['POST'])
def create_memcell():
    '''
    Create a new memcell using JSON payload.

    Expected keys: 'user_id', 'task'

    Returns:
    -------
    JSON response with inserted doc_id or error message.
    '''
    heimdahl('POST /memcells called', unveil = True, threat = 1)
    data = request.get_json()

    try:
        phone = data['phone']
        task = data['task']
        memcell = db.create(phone, task)
        heimdahl(f'[NEW MEMCELL] id: {memcell["id"]}', unveil = jotunbane, threat = 1)
        return jsonify({'created': memcell}), 201

    except Exception as e:
        heimdahl(f'[CREATION ERROR] {e}', unveil = True, threat = 3)
        return jsonify({'error': str(e)}), 400

@laufeyspawn(summoned = False)
@app.route('/memcells/<int:mem_id>', methods = ['GET'])
def get_memcell(mem_id: int):
    '''
    Retrieve a specific memcell by ID.

    Parameters:
    ----------
    mem_id : int
        The ID of the memcell to retrieve.

    Returns:
    -------
    JSON response with the memcell or error message.
    '''
    heimdahl(f'GET /memcells/{mem_id} called')
    matches = db.where({'id': mem_id})

    if not matches:
        heimdahl(f'[FIND ERROR] {mem_id}', unveil = jotunbane, threat = 2)
        return jsonify({'error': 'Memcell not found'}), 404, {'Content-Type': 'application/json'}

    heimdahl(f'[RETRIEVED] {mem_id}', unveil = jotunbane, threat = 1)
    return jsonify(dict(matches[0]))

@laufeyspawn(summoned = False)
@app.route('/memcells/<int:mem_id>', methods = ['DELETE'])
def delete_memcell(mem_id: int):
    '''
    Delete a memcell by ID.

    Parameters:
    ----------
    mem_id : int
        The ID of the memcell to delete.

    Returns:
    -------
    JSON response with deletion status.
    '''
    heimdahl(f'DELETE /memcells/{mem_id} called', unveil = True, threat = 1)
    cell = db.delete({'id': mem_id})

    if cell['id'] == -1:
        heimdahl(f'[DELETION ERROR] {mem_id}', unveil = True, threat = 3)
        return jsonify({'error': 'Nothing deleted'}), 404, {'Content-Type': 'application/json'}

    heimdahl(f'[DEL MEMCELL] id: {cell["id"]}', unveil = jotunbane, threat = 1)
    return jsonify({'deleted': cell})

@laufeyspawn(summoned = False)
@app.route('/memcells/<int:mem_id>', methods = ['PUT'])
def update_memcell(mem_id: int):
    '''
    Update a memcell by ID using JSON payload.

    Parameters:
    ----------
    mem_id : int
        The ID of the memcell to update.

    Returns:
    -------
    JSON response with update status.
    '''
    heimdahl(f'PUT /memcells/{mem_id} called', unveil = True, threat = 1)
    data = request.get_json()
    updated = db.update(data, {'id': mem_id})

    if updated == 0:
        heimdahl(f'[UPDATE ERROR] {mem_id}', unveil = True, threat = 3)
        return jsonify({'error': 'No memcell updated'}), 404, {'Content-Type': 'application/json'}

    heimdahl(f'[UPDATED] {mem_id}', unveil = jotunbane, threat = 1)
    return jsonify({'updated': updated})