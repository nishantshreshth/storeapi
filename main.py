
from flask import Flask, jsonify, abort, request, make_response, url_for, render_template
from flask.ext.httpauth import HTTPBasicAuth
from user import User
from store import Store
import json

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username!=None:
        u=User()
        return u.get_api_key(username)
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 401)
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)


@app.route('/store/api/items/', methods = ['POST'])
@auth.login_required
def create_item():
    if not request.json or not 'name' in request.json or not 'price' in request.json or not 'description' in request.json:
        abort(400)
    item = {
        'name': request.json['name'].lower(),
        'description': request.json.get('description', ""),
        'price':request.json.get('price'),
        'quantity': request.json.get('quantity'),
        'seller':request.json.get('seller'),
        'category': request.json.get('category')
        }
    item =  Store.insert_item(item)
    return jsonify(item), 201



@app.route('/store/api/items/search/', methods=['GET'])
@auth.login_required
def get_search():
    query=request.args.to_dict()
    resp=Store.search_items(query)
    print "RESP"
    print resp
    return jsonify({'ITEMS' : resp}), 200



@app.route('/store/api/items/', methods = ['GET'])
@auth.login_required
def get():
    items=Store.get_all()
    return jsonify({'ITEMS':items}), 200


@app.route('/store/api/items/<item_id>', methods = ['PUT'])
@auth.login_required
def update(item_id):
    temp = request.json
    if len(temp) > 6 or "_id" in temp or len(temp)<1:
        abort(400)
    res = Store.update(str(item_id),temp)
    if res==404:
        abort(404)
    print res
    return jsonify(res), 200



@app.route('/store/api/items/<item_id>', methods = ['DELETE'])
@auth.login_required
def delete(item_id):
    if not item_id:
        abort(400)
    else:
        res = Store.delete_item(item_id)
        if res == 200:
            return jsonify({"Ok":"Deleted"}), 200
        abort(404)

@app.route('/', methods = ['GET', 'POST'])
def index():
    info=None
    if request.method =='POST':
        name=request.form['name']
        email=request.form['email']
        passwrd=request.form['pswd']
        if not name or not email or not passwrd:
            info="Fields cannot Be Blank"
        else:
            u=User()
            info=u.create(name,email,passwrd)
    return render_template('index.html',info=info)

if __name__ == '__main__':
    app.run(debug = True)