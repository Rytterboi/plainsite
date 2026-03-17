from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profil/")
def profil():
    return render_template("profil.html")


@app.route("/ydelser/")
def ydelser():
    return render_template("ydelser.html")


@app.route("/terapiformer/")
def terapiformer():
    return render_template("terapiformer.html")


@app.route("/praktisk-info/")
def praktisk_info():
    return render_template("praktisk_info.html")


@app.route("/pris-og-betaling/")
def pris_og_betaling():
    return render_template("pris_og_betaling.html")


@app.route("/afbud/")
def afbud():
    return render_template("afbud.html")


@app.route("/kontakt/")
def kontakt():
    return render_template("kontakt.html")


@app.route("/book-en-tid/")
def book_en_tid():
    return render_template("book_en_tid.html")


@app.route("/vilkaar-og-betingelser/")
def vilkaar():
    return render_template("vilkaar.html")


@app.route("/bliv-en-aktivpsykolog/")
def bliv_aktivpsykolog():
    return render_template("bliv_aktivpsykolog.html")


if __name__ == "__main__":
    app.run(debug=True)
