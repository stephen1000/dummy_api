import os
import random
from glob import glob

from flask import Flask, request

app = Flask(__name__)

SUPER_SECRET_API_KEY = "12345"
FATES = [os.path.basename(x) for x in glob("static/*")]
FATE_OPTIONS = "".join(
    f'<option value="{i}">{fate.split(" ")[0]}</option>' for i, fate in enumerate(FATES)
)

with open(os.path.join(os.path.dirname(__file__), "facts.txt"), "r") as f:
    FACTS = [line for line in f]


@app.route("/", methods=["GET", "POST"])
def test_security():
    if request.method == "GET":
        return (
            "<h1>welcome to the super cool api site</h1>"
            "<p>what is your api key?</p>"
            '<form method="POST">'
            "<label>Choose your fate: "
            '<select name="fate">'
            '<option value="-1">random</option>'
            f"{FATE_OPTIONS}"
            "</select>"
            "<br>"
            "<label>Api key, plz: "
            '<input name="apikey" type="password"/>'
            '<input type="submit"/>'
            "</label>"
            "</form>"
        )
    elif request.method == "POST":
        apikey = request.form.get("apikey")
        if apikey == SUPER_SECRET_API_KEY:
            fate = request.form.get("fate")
            if fate == "-1":
                fate = random.randint(0, len(FATES) - 1)
            fact = random.choice(FACTS)
            return (
                f'<a href="/"><img src="/static/{FATES[int(fate)]}" /></a><p>Fun fact: {fact}</p>'
            )
        else:
            return '<a href="/">D:</a>'
    return "Error 400"
