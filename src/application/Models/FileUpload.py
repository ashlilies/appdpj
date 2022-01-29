# Ashlee
# Provides quick-and-easy file upload from Flask.

import os
import uuid

from application import app


# Returns a stored relative filepath in the static folder.
def save_file(request_files, key: str) -> str:
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


# Deletes a file in the uploads folder.
def delete_file(stored_filename: str):
    static_dir = os.path.join(os.getcwd(), "application/static")
    filepath = os.path.join(static_dir, stored_filename)
    try:
        os.remove(filepath)
    except OSError:
        pass
