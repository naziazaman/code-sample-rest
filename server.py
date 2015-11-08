import cherrypy
import json
import math
import os
from bson.objectid import ObjectId

from config import *
from data_validators import validate_data

class Product:
    @cherrypy.expose
    def index(self):
        return open('index.html')

class ProductAPI:
    exposed = True
    
    def get_products(self, page, json_data=False):
        """Returns data based on pagination value and query parameters
        """
        page = int(page)
        offset = (page - 1) * PRODUCTS_PER_PAGE
        limit = page * PRODUCTS_PER_PAGE

        total_products = products.find().sort('price', pymongo.ASCENDING)
        items = list(total_products)[offset:limit]
        total_records = total_products.count()
        total_page = math.ceil(total_products.count()/float(PRODUCTS_PER_PAGE))

        item_dict = {'products': [
                       {'id': str(item.get('_id')),
                       'name': item.get('name'),
                       'price': item.get('price'),
                       'delivery': item.get('delivery'),
                       'sizes': item.get('sizes')} for item in items]}
        if json_data:
            data = {'page': page,
                    'total': total_page,
                    'records': total_records,
                    'rows': item_dict['products']}
            return json.dumps(data)
        else:
            return '{0}'.format(json.dumps(item_dict, indent=4, separators=(',', ': ')))


    def GET(self, *vpath, **params):
        json_data = True if str(params.get('type', '')) == 'json' else False

        if len(vpath) == 0:
            return '{0}'.format(self.get_products(params.get('page', 1), json_data=True))
        else:
            _id = vpath[0] if vpath[0].isdigit() else None
            if _id:
                item = products.find_one({'_id': ObjectId(_id)})
                if item:
                    return '{0}'.format(json.dumps(item, indent=4, separators=(',', ': ')))
                else:
                    return 'No product was found with ID {0}.'.format(_id)


    def POST(self, **kwargs):
        data = validate_data(**kwargs)
        _id = products.insert(data)

        return 'A new product with ID {0} has been created'.format(_id)


    def PUT(self, id, **kwargs):
        try:
            product = products.find_one({'_id': ObjectId(id)})
            
            if product:
                data = validate_data(**kwargs)
                products.update({'_id': product['_id']}, {'$set': data})
                product = products.find_one({'id': ObjectId(id)})
                return 'Product with ID {0} has been updated:\n{1}'.format(id, json.dumps(product, indent=4, separators=(',', ': ')))
            else:
                return 'No product with the ID {0} found'.format(id)
        except Exception, e:
            print e


    def DELETE(self, id):
        product = products.find_one({'_id': ObjectId(id)})
        if product:
            products.remove({'_id': ObjectId(id)})
            return 'Product with ID {0} has been deleted'.format(id)
        else:
            return 'No product with the ID {0} was found'.format(id)


def main():
    """
    cherrypy.tree.mount(
        ProductAPI(),
        '/products',
        {
            '/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
        }
    )
    cherrypy.engine.start()
    cherrypy.engine.block()
    """

    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/products': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    webapp = Product()
    webapp.products = ProductAPI()
    cherrypy.quickstart(webapp, '/', conf)

if __name__ == '__main__':
    main()