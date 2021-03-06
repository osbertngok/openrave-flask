from flask import request, Blueprint, current_app

import bson.json_util
import json
import datetime
import os
from os import listdir
from os.path import isfile, join
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
                transform = body.GetTransform().tolist()
                processed_transform = None
                if len(transform) == 4:
                    processed_transform = {
                        "r1": transform[0],  # need confirmation on this
                        "r2": transform[1],
                        "r3": transform[2],
                        "r4": transform[3]
                    }
                else:
                    processed_transform = {
                        "r1": transform[0],  # need confirmation on this
                        "r2": transform[1],
                        "r3": transform[2],
                    }
                item = {
                    "name": body.GetName(),
                    "transform": processed_transform,
                    "is_robot": body.IsRobot(),
                    "dof": body.GetDOF() if body.IsRobot() else None
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
        UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
        if isfile(join(UPLOAD_FOLDER, filename)):
            os.remove(join(UPLOAD_FOLDER, filename))
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
            retrieved_scenes.append(json.loads(bson.json_util.dumps(scene)))
        return json.dumps(retrieved_scenes)
    if request.method == 'DELETE':
        if current_app.config['TESTING']:
            current_app.collection.delete_many({})
            UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
            for f in listdir(UPLOAD_FOLDER):
                if isfile(join(UPLOAD_FOLDER, f)):
                    os.remove(join(UPLOAD_FOLDER, f))
            return json.dumps({"success": True})
        else:
            return json.dumps({"success": False, "error": "Not in test environment"})
    return json.dumps({"success": False, "error": "Unknown method or not in test environment"})
