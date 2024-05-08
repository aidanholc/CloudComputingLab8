from flask import Flask, request, jsonify, render_template
from service import BlogPoster
from models import Schema
import json

app = Flask(__name__)
@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
    return response

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/<name>")
def hello_name(name):
    return "Hello " + name

@app.route("/blogs", methods=["GET"])
def list_blog():
    return render_template("blogs.html", form_data=BlogPoster().list())

@app.route("/blogs", methods=["POST"])
def create_blog():
    created_info = jsonify(BlogPoster().create(jsonify(request.form)))
    return list_blog()

@app.route("/blogs/<item_id>", methods=["PUT"])
def update_item(item_id):
    return jsonify(BlogPoster().update(item_id, request.get_json()))

@app.route("/blogs/<item_id>", methods=["GET"])
def get_item(item_id):
    return jsonify(BlogPoster().get_by_id(item_id))

@app.route("/blogs/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    return jsonify(BlogPoster().delete(item_id))
if __name__ == "__main__":
    Schema()
    app.run(debug=True, host='127.0.0.1', port=5000)