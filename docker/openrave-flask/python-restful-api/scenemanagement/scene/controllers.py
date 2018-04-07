from flask import request, Blueprint, current_app

import bson.json_util
import json
import datetime
import os
import openravepy

bp = Blueprint('bp', __name__)


def scene_parser(file_path, filename):
    ret = {
        "createdDateTime": datetime.datetime.now(),
        "filename": filename,
        "bodies": []
    }
    try:
        env = openravepy.Environment()
        env.Load(file_path)
        with env:
            for body in env.GetBodies():
                item = {
                    "name": body.GetName()
                }
                ret['bodies'].append(item)
    except openravepy.openrave_exception as e:
        print(e)
    return ret


@bp.route('/scenes/<string:filename>', methods=['GET', 'DELETE'])
def scene_filename_handler(filename):
    if request.method == 'GET':
        selected_scene = current_app.collection.find_one({"filename": filename})
        return bson.json_util.dumps(selected_scene)
    if request.method == 'DELETE':
        current_app.collection.delete_one({"filename": filename})
        return '{"success": true}'


@bp.route('/scenes', methods=['GET', 'DELETE', 'POST'])
def scenes_handler():
    if request.method == 'POST':
        if 'file' not in request.files:
            return json.dumps({"success": False, "error": "No file specified"}), 400
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return json.dumps({"success": False, "error": "No file specified"}), 400
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        if os.path.exists(file_path):
            return json.dumps({"success": False, "error": "file already exists"}), 400
        file.save(file_path)
        uploaded_scene = scene_parser(file_path, file.filename)
        inserted_id = current_app.collection.insert_one(uploaded_scene).inserted_id
        return json.dumps({"success": True, "filename": file.filename})
    if request.method == 'GET':
        retrieved_scenes = []
        for scene in current_app.collection.find():
            retrieved_scenes.append(scene)
        return json.dumps(retrieved_scenes)
    if request.method == 'DELETE':
        if current_app.config['TESTING']:
            current_app.collection.delete_many({})
            return json.dumps({"success": True})
        else:
            return json.dumps({"success": False, "error": "Not in test environment"})
    return json.dumps({"success": False, "error": "Unknown method or not in test environment"})
