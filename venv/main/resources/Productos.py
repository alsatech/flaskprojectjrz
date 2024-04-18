from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ProductModel
from main.auth.decorators import role_required

class Producto(Resource):
    def get(self, id):
        producto = db.session.query(ProductModel).get_or_404(id)
        try:
            return producto.to_json()
        except:
            return 'Resource not found', 404
    
    #EDITAR 
    @role_required(roles=["admin"])
    def put (self, id):
        producto = db.session.query(ProductModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(producto, key, value)
        try:
            db.session.add(producto)
            db.session.commit()
            return producto.to_json(), 201
        except:
            return '',404
        
    #BORRAR
    @role_required(roles=["admin"])
    def delete(self, id):
        producto = db.session.query(ProductModel).get_or_404(id)
        try:
            db.session.delete(producto)
            db.session.commit()
        except:
            return '', 404

class Productos(Resource):
    # OBTENER
    def get(self):
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 5))
        
        productos = ProductModel.query.paginate(page=page, per_page=per_page, error_out=True)

        return jsonify({
            'productos': [producto.to_json() for producto in productos.items],
            'total': productos.total,
            'pages': productos.pages,
            'page': page
        })


    #ENVIAR
    @role_required(roles=["admin"])
    def post(self):
        producto = ProductModel.from_json(request.get_json())
        db.session.add(producto)
        db.session.commit()
        return producto.to_json(), 201
    