from flask import Blueprint, render_template, flash, redirect, url_for, current_app, send_from_directory
from werkzeug.utils import secure_filename
import os
from ..forms import UploadPDFForm, UploadImageForm
import qrcode

main = Blueprint('main', __name__)

def generate_qr_code(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    qr_folder = os.path.join(current_app.root_path, 'static', 'qr-codes')
    os.makedirs(qr_folder, exist_ok=True)

    img_path = os.path.join(qr_folder, f"{filename}.png")
    img.save(img_path)

    return filename  # имя файла без пути

@main.route('/', methods=['GET', 'POST'])
def index():
    pdf_form = UploadPDFForm()
    image_form = UploadImageForm()

    if pdf_form.validate_on_submit():
        file = pdf_form.pdf_file.data
        filename = secure_filename(file.filename)

        # Путь для загрузки PDF в безопасную папку
        upload_folder = os.path.join('/tmp', 'uploads', 'pdfs')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        # Проверка: файл реально сохранился?
        if not os.path.exists(file_path):
            flash('Ошибка при сохранении PDF!', 'danger')
            return redirect(url_for('main.index'))

        # Генерация QR-кода на внешний URL PDF-файла
        pdf_url = url_for('main.serve_pdf', filename=filename, _external=True)
        qr_filename = os.path.splitext(filename)[0]
        generate_qr_code(pdf_url, qr_filename)

        flash('PDF успешно загружен и QR-код сгенерирован!', 'success')
        return redirect(url_for('main.show_qr', filename=qr_filename))

    if image_form.validate_on_submit():
        file = image_form.image_file.data
        filename = secure_filename(file.filename)
        upload_folder = os.path.join('/tmp', 'uploads', 'images')
        os.makedirs(upload_folder, exist_ok=True)
        file.save(os.path.join(upload_folder, filename))
        flash('Изображение загружено!', 'success')
        return redirect(url_for('main.index'))

    return render_template('main/index.html',
                           pdf_form=pdf_form,
                           image_form=image_form)

@main.route('/qr/<filename>')
def show_qr(filename):
    qr_folder = os.path.join(current_app.root_path, 'static', 'qr-codes')
    qr_path = os.path.join(qr_folder, f"{filename}.png")

    if not os.path.exists(qr_path):
        flash('QR-код не найден!', 'danger')
        return redirect(url_for('main.index'))

    qr_image_url = url_for('static', filename=f'qr-codes/{filename}.png')

    return render_template('main/qr_display.html',
                           qr_image_url=qr_image_url,
                           filename=filename)

@main.route('/serve-pdf/<filename>')
def serve_pdf(filename):
    pdf_folder = os.path.join('/tmp', 'uploads', 'pdfs')
    return send_from_directory(pdf_folder, filename)
