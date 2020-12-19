import yaml
import os
from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

class UploadFile(Resource):
    def post(self):
        with open(os.path.dirname(__file__) + '/../../../../../config.yaml') as file:
            path = yaml.load(file,Loader=yaml.FullLoader)
        print(path["path"]["upload_file_path"])
        print(request.args)
        if 'file' not in request.files:
            return 404
        file = request.files['file']
        filename = secure_filename(file.filename)
        if filename == "":
            return 404
        if file and self.allowed_file(file.filename):
            file.save(os.path.join(path["path"]["upload_file_path"], filename))
            return 200
        else:
            print("Not allowed file to upload")
            return 406


    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS    