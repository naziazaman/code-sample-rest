import argparse
import requests
import json
from db import load_data

URL = 'http://127.0.0.1:8080/products'

class App:
	def __init__(self):
		self._session = requests.Session()

	def create_product(self):
		pid = get_input("{}".format("Enter product ID: "))
		pname = get_input("{}".format("Enter product Name: "))
		pprice = get_input("{}".format("Enter product Price: "))
		response = self._session.post(URL, params={'id': pid, 'name': pname, 'price': pprice})
		print response.text

	def update_product(self, pid):
		pname = get_input("{}".format("Enter new product Name: "))
		pprice = get_input("{}".format("Enter new product Price: "))
		response = self._session.put(URL+'/'+str(pid), params={'name': pname, 'price': pprice})
		print response.text

	def delete_product(self, pid):
		response = self._session.delete(URL+'/'+str(pid))
		print response.text

	def list_products(self, page=1):
		response = self._session.get(URL+'?page={}'.format(page))
		print response.text

	def view_product(self, pid):
		response = self._session.get(URL+'/'+str(pid))
		print response.text

def get_input(question):
    return raw_input(question)

def main():
	parser = argparse.ArgumentParser()
	actions = parser.add_mutually_exclusive_group()
	actions.add_argument('-i', '--importdata',
                         action='store',
                         help='import data to the database')
	actions.add_argument('-a', '--add',
                         action='store_true',
                         help='add a product to the database')
	actions.add_argument('-u', '--update', type=int,
                         help='update a product in the database')
	actions.add_argument('-d', '--delete', type=int,
                         help='delete a product from the database')
	actions.add_argument('-l', '--listproducts', type=int,
                         help='list the products in the database')
	actions.add_argument('-p', '--viewproduct', type=int,
                         help='view product details')

	args = parser.parse_args()
	app = App()

	if args.importdata:
		load_data()

	if args.add:
		app.create_product()

	if args.update:
		app.update_product(args.update)

	if args.delete:
		app.delete_product(args.delete)

	if args.listproducts:
		app.list_products(args.listproducts)

	if args.viewproduct:
		app.view_product(args.viewproduct)

if __name__ == '__main__':
	main()