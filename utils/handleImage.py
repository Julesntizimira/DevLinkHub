from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def handleImage(file, item_id, model_type=None):
    ''' handle image upload storage'''
    if file and allowed_file(file.filename):
        unique_filename = item_id + '.' + file.filename.rsplit('.', 1)[1].lower()
        filename = secure_filename(unique_filename)
        if model_type:
            path = f'webdynamic/static/images/profiles'
        else:
            path = f'webdynamic/static/images'
        file.save(os.path.join(path, filename))
        return f'images/{filename}' if model_type is None else f'images/profiles/{filename}'
    return None