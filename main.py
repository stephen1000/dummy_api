import os
import random
from glob import glob

from flask import Flask, Response, request

app = Flask(__name__)

print('Startin up!!!!')

SUPER_SECRET_API_KEY = "12345"
FATES = [os.path.basename(x) for x in glob("static/*")]
FATE_OPTIONS = "".join(
    f'<option value="{i}">{fate.split(" ")[0]}</option>' for i, fate in enumerate(FATES)
)

with open(os.path.join(os.path.dirname(__file__), "facts.txt"), "r") as f:
    FACTS = [line for line in f]


@app.route("/", methods=["GET", "POST"])
def index():
    accept = request.headers.get('Accept')
    if accept == 'application/json':
        return index_json()
    if request.method == "GET":
        return Response(
            (
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
            ),
            status=200,
            mimetype="text/html",
        )
    elif request.method == "POST":
        apikey = request.form.get("apikey")
        if apikey == SUPER_SECRET_API_KEY:
            fate = request.form.get("fate")
            if fate == "-1" or fate is None:
                fate = random.randint(0, len(FATES) - 1)
            fact = random.choice(FACTS)
            return Response(
                f'<a href="/"><img src="/static/{FATES[int(fate)]}" /></a><p>Fun fact: {fact}</p>',
                status=200,
                mimetype="text/html",
            )
        else:
            return '<p>Bad API key! get outta here!</p><p><a href="/">Go back home.</a></p>'
    return Response("Error 400- Bad request", status=400, mimetype="text/html")



def index_json():
    if request.method == "GET":
        return Response(
            {"fates": dict((i, fate) for i,fate in enumerate(FATES))},
            status=200,
            mimetype="application/json",
        )
    if request.method == "POST":
        apikey = request.headers.get("X-API-KEY")
        if apikey != SUPER_SECRET_API_KEY:
            response = Response(
                {"error": "Unauthorized"}, status=401, mimetype="application/json"
            )
            response.headers.add("Authenticate", "X-API-KEY")
            return response
        return Response({'fact':random.choice(FACTS)}, status=200, mimetype='application/json')
