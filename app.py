from flask import Flask, request, make_response, render_template, flash, url_for, send_file
from werkzeug.utils import secure_filename
import json
import checker
import uuid
import os
from transliterate import translit
from transliterate.exceptions import LanguageDetectionError

import config
from MemFiles import MemFileManager, MemFile

app = Flask(__name__, static_folder="static", static_url_path="")
app.secret_key = config.secret
app.mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        selected_boxes = request.form.getlist("parameters_checkbox")
        print(selected_boxes)
        try:
            file = request.files['userDocument']
            try:
                sec_name = translit(file.filename, reversed=True)
            except LanguageDetectionError:
                sec_name = file.filename
            sec_name = secure_filename(sec_name)
            print(f"Received file {sec_name}")
            uid = uuid.uuid4().hex
            # res = checker.file_check_interface(file, mock=False)
            res = checker.file_check_interface(file, selected_boxes, mock=False)
            link = f"{request.host}{url_for('whats_wrong', review_id=uid)}"
            json_resp = res.json_result(link)
            print(link)
            mem_file = MemFile(name=sec_name, file=res.processed_file, url=link)
            app.mem_file_manager.add_file(uid, mem_file)
            # flash(link)
            return json_resp
        except Exception as e:
            raise
            print(f"Error occurred: {e}")
            return make_response("", 400)
    elif request.method == "GET":
        return render_template("page.html")


@app.route("/api/getfeedback/<review_id>", methods=["GET"])
def whats_wrong(review_id):
    review_id = str(review_id)
    mem_file = app.mem_file_manager.get_file(review_id)
    if mem_file is None:
        return make_response("", 410)
    attachment_filename = f"Review_{mem_file.name}"
    return send_file(mem_file.file, mimetype=app.mime, as_attachment=True, attachment_filename=attachment_filename)


@app.before_first_request
def startup():
    app.mem_file_manager = MemFileManager()


if __name__ == '__main__':
    app.run(host='0.0.0.0')

# todo: использовать только review_id или только uid
# todo: использовать только link или только url
# todo: не вылавливает выравнивание для таблиц
# todo: не вылавливает размер шрифта
# todo: не вылавливает точки в конце названия раздела
# todo: писать непечатаемым текстом?
