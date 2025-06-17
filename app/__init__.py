from flask import Flask, request, jsonify, render_template
from .routes.main import main
import os

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '123456767890'
    app.config['UPLOAD_FOLDER'] = 'pdf-files'
    app.config['QR_CODE_FOLDER'] = os.path.join('static', 'qr-codes')  # Сохраняем в static/qr-codes
    app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB максимальный размер файла

    # Создаем необходимые папки
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['QR_CODE_FOLDER'], exist_ok=True)

    app.register_blueprint(main)

    return app
    