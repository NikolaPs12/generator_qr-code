from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

class UploadPDFForm(FlaskForm):
    pdf_file = FileField(
        "PDF File",
        validators=[
            FileRequired("Пожалуйста, выберите PDF-файл"),
            FileAllowed(['pdf'], "Только PDF файлы!")
        ]
    )
    submit_pdf = SubmitField("Загрузить PDF")

class UploadImageForm(FlaskForm):
    image_file = FileField(
        "Image File",
        validators=[
            FileRequired("Пожалуйста, выберите изображение"),
            FileAllowed(['jpg', 'jpeg', 'png'], "Только изображения!")
        ]
    )
    submit_image = SubmitField("Создать QR-код")