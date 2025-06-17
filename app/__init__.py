from flask import Flask
from .routes.main import main
import os

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '123456767890'

    # Безопасная папка загрузки
    upload_folder = '/tmp/uploads/pdfs' if not app.debug else 'pdf-files'
    qr_folder = os.path.join(app.root_path, 'static', 'qr-codes')

    app.config['UPLOAD_FOLDER'] = upload_folder
    app.config['QR_CODE_FOLDER'] = qr_folder
    app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

    # Создаём папки (даже в /tmp)
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(qr_folder, exist_ok=True)

    app.register_blueprint(main)

    return app
