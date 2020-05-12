from flask import Flask, request, make_response, render_template
from werkzeug.utils import secure_filename
import json
import checker
import uuid


app = Flask(__name__, static_folder="static", static_url_path="")


@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        try:
            file = request.files['userDocument']
            file.filename = uuid.uuid4().hex
            name = secure_filename(file.filename)
            print(f"Received file {name}")
            file.save(name)
            res = checker.file_check_interface(file)
            res = json.dumps(res)
            return res
        except Exception as e:
            print(f"Error occurred: {e}")
            return make_response("", 400)
    elif request.method == "GET":
        return render_template("page.html")


if __name__ == '__main__':
    app.run()
