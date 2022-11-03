from flask import Flask, request, render_template


def getJson():
    return [{
        "href": "/read",
        "type": "GET"
    },
        {
            "href": "/read_one/<id>",
            "type": "GET"
        },
        {
            "href": "/create",
            "type": "POST"
        },
        {
            "href": "/delete/<id>",
            "type": "DELETE"
        },
        {
            "href": "/update/<id>",
            "type": "PUT"
        }
    ]


zpravy = {}

app = Flask(__name__)


@app.route('/read', methods=["GET"])
def get_read():
    return {"m": zpravy, "links": getJson(1)}


@app.route('/api/v2/read_one/<id>', methods=["GET"])
def get_read_one(id):
    if id < -1:
        return {"error": "Id nesmi byt zaporne"}
    else:
        return {"m": zpravy[int(id)], "links": getJson(id)}


count = 0


@app.route('/api/v2/create', methods=["POST"])
def post_create():
    global count
    count += 1
    req = request.get_json()
    item = req["text"]
    zpravy[count] = item

    return {"m": "prvek byl uspesne pridan", "links": getJson(1)}


@app.route('/api/v2/delete/<id>', methods=["DELETE"])
def delete(id):
    if id < -1:
        return {"error": "Id nesmi byt zaporne"}
    else:
        zpravy.pop(int(id))
        return {"m": f"prvek byl uspesne smazan","links": getJson(id)} + {"prve:":f"{zpravy[int(id)]}"}


@app.route('/api/v2/delete_all', methods=["DELETE"])
def deleteAll():
    zpravy.clear()
    return {"m": "Prvky byly uspesne smazane", "links": getJson(id)}


@app.route('/api/v2/update/<id>', methods=["PUT"])
def update(id):
    if id < -1:
        return {"error": "Id nesmi byt zaporne"}
    else:
        req = request.get_json()
        item = req["text"]
        zpravy[int(id)] = item
        return {"m": "Uprava probehla uspesne", "links": getJson(id)}


@app.route('/api/v2/doc')
def documentation():
    return render_template('doc.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)


## 3 zlepsini
##1. moznost stazeni dokumentace
##2 ohlidani
##3. dict musi obsahovat id
