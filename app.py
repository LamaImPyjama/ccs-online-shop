from datetime import datetime
from flask import Flask, render_template, request, jsonify, make_response
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import requests

credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=getenv('KEYVAULTURL'), credential=credential)
blob_storage = getenv('BLOBSTORAGE')
logistic_system = getenv('LOGISTICSYSTEM')

dbusername = secret_client.get_secret("dbusername")
dbusername.value
dbpassword = secret_client.get_secret("dbpassword")
dbpassword.value
dburl = secret_client.get_secret("dburl")
dburl.value
db = secret_client.get_secret("db")
db.value


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://" + dbusername.value + ":" + dbpassword.value + "@" + dburl.value + ":5432/" + db.value
# 
# 
# db = SQLAlchemy(app)
# class Item(db.Model):
#     __tablename__ = 'items'
#     id = db.Column(db.Integer, primary_key=True)
#     item_id = db.Column(db.Integer)
#     name = db.Column(db.String)
#     description = db.Column(db.String)
# with app.app_context():
#     db.create_all()


def query_logistic_system(item_id):
    stock = requests.get(logistic_system + "items/" + str(item_id))
    stock = stock.json()
    return stock['stock']


def update_logistic_system(item_id):
    response = requests.patch(logistic_system + "items/" + str(item_id))
    response = response.json()
    return response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/items')
def get_items():
#    result = Item.query.all()
    items = []
#    for item in result:
#        o = {}
#        o['item_id'] = item.item_id
#        o['name'] = item.name
#        o['description'] = item.description
#        o['thumbnail'] = blob_storage + str(item.item_id) + ".jpg"
#        o['stock'] = query_logistic_system(item.item_id)
#
#        items.append(o)
#
    return make_response(jsonify(items), 200)


@app.route('/api/items/<item_id>', methods=['PATCH'])
def order_item(item_id):
    item_id = int(item_id)
    update_logistic_system(item_id)
    return jsonify("success")