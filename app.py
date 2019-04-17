from flask import Flask, render_template, request, url_for
import sqlGenerator

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/product/<name>")
def product(name):
    return render_template("product.html", name=name)


@app.route("/", methods=["GET", "POST"])
def get_data():
    if request.method == "GET":
        username = request.form.get("username")
        password = request.form.get("password")
'''
@app.context_processor
def context_processor():
    return dict(name='vale')

'''

if __name__ == "__main__":
    app.run(debug=True)