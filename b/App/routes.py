from flask import request, jsonify
from .config import LOG, db, app

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

@app.route('/memcells', methods = ['GET'])
def get_all_memcells():
    '''
    Return all memcells in the database.

    Returns:
    -------
    JSON response containing all memcells.
    '''
    LOG.debug('GET /memcells called')
    return jsonify([dict(cell) for cell in db.all])


@app.route('/memcells', methods = ['POST'])
def create_memcell():
    '''
    Create a new memcell using JSON payload.

    Expected keys: 'user_id', 'task'

    Returns:
    -------
    JSON response with inserted doc_id or error message.
    '''
    LOG.debug('POST /memcells called')
    data = request.get_json()

    try:
        user = data['user']
        task = data['task']
        doc_id = db.create(user, task)
        LOG.info(f'Created memcell: doc_id = {doc_id}')
        return jsonify({'doc_id': doc_id}), 201

    except Exception as e:
        LOG.error(f'Failed to create memcell: {e}')
        return jsonify({'error': str(e)}), 400


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
    LOG.debug(f'GET /memcells/{mem_id} called')
    matches = db.where({'id': mem_id})

    if not matches:
        LOG.warning(f'Memcell not found: id = {mem_id}')
        return jsonify({'error': 'Memcell not found'}), 404

    LOG.info(f'Retrieved memcell: id = {mem_id}')
    return jsonify(dict(matches[0]))


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
    LOG.debug(f'DELETE /memcells/{mem_id} called')
    deleted = db.delete({'id': mem_id})

    if deleted == 0:
        LOG.warning(f'No memcell deleted: id = {mem_id}')
        return jsonify({'error': 'Nothing deleted'}), 404

    LOG.info(f'Memcell deleted: id = {mem_id}')
    return jsonify({'deleted': deleted})


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
    LOG.debug(f'PUT /memcells/{mem_id} called')
    data = request.get_json()
    updated = db.update(data, {'id': mem_id})

    if updated == 0:
        LOG.warning(f'No memcell updated: id = {mem_id}')
        return jsonify({'error': 'No memcell updated'}), 404

    LOG.info(f'Memcell updated: id = {mem_id}')
    return jsonify({'updated': updated})
