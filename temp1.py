from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return "EASYWAYTOWIN"


@app.route("/ru")
def index_ru():
    return render_template("qrru.html", title="Gosuslugi")


@app.route("/en")
def index_en():
    return render_template("qren.html", title="Gosuslugi")


@app.route("/base")
def index_base():
    return render_template("qrbase.html", title="Gosuslugi")


def main():
    app.run(port=8080, host='192.168.0.99')  # 178.205.11.108


if __name__ == '__main__':
    main()
