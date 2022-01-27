import os
import uuid

from application import app


def save_file(request_files, key: str):
    file = request_files[key]
    file_ext = os.path.splitext(file.filename)[1]
    filename = str(uuid.uuid4()) + str(file_ext)
    file_upload_path = os.path.join(os.getcwd(), "application/",
                                    app.config['UPLOAD_FOLDER'])
    os.makedirs(file_upload_path, exist_ok=True)
    filepath = os.path.join(file_upload_path, filename)
    file.save(filepath)
    stored_filename = "uploads/%s" % filename
    return stored_filename

