from flask import request, Blueprint, current_app

import bson.json_util
import json
import datetime

bp = Blueprint('bp', __name__)


def scene_parser(file):
    return {"createdDateTime": datetime.datetime.now(), "filename": file.filename,
            "bodies": [{"name": "body1", "tranformation": "rotate", "robot": False}]}


@bp.route('/scene/<string:filename>', methods=['GET', 'DELETE'])
def scene_handler(filename):
    if request.method == 'GET':
        selected_scene = current_app.collection.find_one({"filename": filename})
        return bson.json_util.dumps(selected_scene)
    if request.method == 'DELETE':
        current_app.collection.delete_one({"filename": filename})
        return '{"success": true}'


@bp.route('/scene', methods=['POST'])
def scene_post_handler():
    if request.method == 'POST':
        if 'file' not in request.files:
            return '{"success": false}', 400
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return '{"success": false}', 400
        uploaded_scene = scene_parser(file)
        inserted_id = current_app.collection.insert_one(uploaded_scene).inserted_id
        return json.dumps({"success": True, "filename": file.filename})


@bp.route('/scenes', methods=['GET', 'DELETE'])
def scenes_handler():
    if request.method == 'GET':
        retrieved_scenes = []
        for scene in current_app.collection.find():
            retrieved_scenes.append(scene.__dict__)
        return json.dumps(retrieved_scenes)
    if request.method == 'DELETE':
        if current_app.config['TESTING']:
            current_app.collection.delete_many({})
            return json.dumps({"success": True})
        else:
            return json.dumps({"success": False, "error": "Not in test environment"})
    return json.dumps({"success": False, "error": "Unknown method or not in test environment"})
