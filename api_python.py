from flask import Flask, request, render_template
import requests
import json

flask_app = Flask(__name__)
ruta = "https://integracion-rick-morty-api.herokuapp.com/api/"


@flask_app.route("/")
def index():
    url_episodios = ruta + "episode"
    resultados = []
    while True:
        try:
            response_episodios = requests.get(url_episodios)
        except requests.ConnectionError:
            return "Error de conexión"
        contenido_index = json.loads(response_episodios.text)
        sgte = contenido_index["info"]["next"]
        resultados += contenido_index["results"]
        if not sgte:
            break
        else:
            url_episodios = sgte
            continue
    return render_template("index.html", episodios=resultados)


@flask_app.route("/episodio/<id>")
def episodio(id):
    url_episodio = ruta + f"episode/{id}"
    try:
        response_episodio = requests.get(url_episodio)
    except requests.ConnectionError:
        return "Error de conexión"
    contenido_episodio = json.loads(response_episodio.text)
    personajes_ids = []
    for personaje in contenido_episodio["characters"]:
        personaje_split = personaje.split("/")
        id_buscado = personaje_split[-1]
        personajes_ids.append(int(id_buscado))
    url_personajes = ruta + f"character/{personajes_ids}"
    try:
        response_personajes = requests.get(url_personajes)
    except requests.ConnectionError:
        return "Error de conexión"
    contenido_personajes = json.loads(response_personajes.text)
    return render_template("episodio.html", episodio=contenido_episodio, personajes=contenido_personajes)


@flask_app.route("/personaje/<id>")
def personaje(id):
    url_personaje = ruta + f"character/{id}"
    try:
        personaje_response = requests.get(url_personaje)
    except requests.ConnectionError:
        return "Error de conexión"
    contenido_personaje = json.loads(personaje_response.text)
    episodios_ids = []
    for episodio in contenido_personaje["episode"]:
        episodio_split = episodio.split("/")
        id_buscado = episodio_split[-1]
        episodios_ids.append(int(id_buscado))
    url_episodios = ruta + f"episode/{episodios_ids}"
    try:
        episodios_response = requests.get(url_episodios)
    except requests.ConnectionError:
        return "Error de conexión"
    contenido_episodios = json.loads(episodios_response.text)

    return render_template("personaje.html", personaje=contenido_personaje, episodios=contenido_episodios)


@flask_app.route("/lugar/<id>")
def lugar(id):
    url_lugar = ruta + f"location/{id}"
    try:
        lugar_response = requests.get(url_lugar)
    except requests.ConnectionError:
        return "Error de conexión"
    contenido_lugar = json.loads(lugar_response.text)
    residentes_ids = []
    for residente in contenido_lugar["residents"]:
        residente_split = residente.split("/")
        residentes_ids.append(int(residente_split[-1]))
    url_residentes = ruta + f"character/{residentes_ids}"
    try:
        residentes_response = requests.get(url_residentes)
    except requests.ConnectionError:
        return "Error de conexión"
    contenido_residentes = json.loads(residentes_response.text)

    return render_template("lugar.html", lugar=contenido_lugar, residentes=contenido_residentes)


@flask_app.route("/busqueda", methods=["POST"])
def busqueda():
    str_busqueda = request.form["content"]

    url_episodios = ruta + f"episode/?name={str_busqueda}"
    resultados_episodios = []
    while True:
        try:
            response_episodios = requests.get(url_episodios)
        except requests.ConnectionError:
            return "Error de conexión"
        contenido_episodios = json.loads(response_episodios.text)
        if "error" in contenido_episodios:
            break
        sgte = contenido_episodios["info"]["next"]
        resultados_episodios += contenido_episodios["results"]
        if not sgte:
            break
        else:
            url_episodios = sgte
            continue

    url_personajes = ruta + f"character/?name={str_busqueda}"
    resultados_personajes = []
    while True:
        try:
            response_personajes = requests.get(url_personajes)
        except requests.ConnectionError:
            return "Error de conexión"
        contenido_personajes = json.loads(response_personajes.text)
        if "error" in contenido_personajes:
            break
        sgte = contenido_personajes["info"]["next"]
        resultados_personajes += contenido_personajes["results"]
        if not sgte:
            break
        else:
            url_personajes = sgte
            continue

    url_lugares = ruta + f"location/?name={str_busqueda}"
    resultados_lugares = []
    while True:
        try:
            response_lugares = requests.get(url_lugares)
        except requests.ConnectionError:
            return "Error de conexión"
        contenido_lugares = json.loads(response_lugares.text)
        if "error" in contenido_lugares:
            break
        sgte = contenido_lugares["info"]["next"]
        resultados_lugares += contenido_lugares["results"]
        if not sgte:
            break
        else:
            url_lugares = sgte
            continue

    return render_template("busqueda.html", episodios=resultados_episodios, personajes=resultados_personajes, lugares=resultados_lugares)


if __name__ == "__main__":
    flask_app.run(debug=True)

