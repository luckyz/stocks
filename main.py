# -*- coding: utf-8 -*-
#!/usr/bin/python
import json
import os
import os.path as path
from datetime import datetime
from time import sleep
import logging


def get_timestamp():
	timestamp_now = datetime.now()
	timestamp = timestamp_now.strftime("%d/%m/%Y %H:%M:%S")

	return timestamp

def next_menu(option):
	for x in range(len(option)):
		# data[x]:
		# 0: option
		# 1: "yes" options
		# 2: "no" options
		# 3: actions_yes
		# 4: actions_no
		data[x] = option[x]

	if data[0] in data[1]:
		return data[3]

	elif data[0] in data[2]:
		return data[4]

class Stock(object):
	def __init__(self):
		super(Stock, self).__init__()

	def save(self, data, filename="data.json"):
		try:
			with open(filename, "w") as file:
				return json.dump(data, file, indent=4, ensure_ascii=False)

		except Exception:
			return None

	def load(self, filename="data.json"):
		with open(filename, "r") as file:
			return json.load(file)

	def add(self, timestamp, id, amount, currency):
		try:
			if not path.exists('data.json'):
				data = {}
				data['stocks'] = {}
			else:
				data = self.load('data.json')

			# if key exists
			if id.upper() in data['stocks'].keys():
				modify = data['stocks'][id.upper()]
				if currency in modify[currency]:
					modify[currency]['amount'] =+ amount
				else:
					modify[currency] = {}
					modify[currency] = {
						'date': timestamp,
						'amount': amount
					}
			# if key not exists
			else:
				data['stocks'][id.upper()] = {}
				data['stocks'][id.upper()][currency] = {
					'date': timestamp,
					'amount': amount
				}

		except Exception as e:
			logging.exception(e)
			
		return self.save(data)

	def header_menu(self):
		os.system("clear")
		print("{0} STOCKS MANAGER {0}\n".format("=" * 7))

	def home_menu(self):
		self.header_menu()
		print("1. Add stock.")
		print("2. Remove stock.")
		option = input("\n> Select option: ")

		return (option, (1,), (2,), (self.add_menu(),), (self.remove_menu(),))

	def add_menu(self):
		self.header_menu()
		id = raw_input("\n> Enter id of stock: ")
		self.header_menu()
		amount = input("\n> Amount: ")
		self.header_menu()
		currency = input("\n> Currency value: ")
		self.header_menu()
		currency = "{:.2f}".format(currency)
		option = raw_input(
"""ID: {0}
Amount: {1}
Currency: {2}
\nThis is correct? ([y]/n): """.format(id.upper(), amount, currency))
		timestamp = get_timestamp()
		f = lambda t, i, a, c: "\n[Saved] {0} | {1} - {2} @ ${3}".format(t, i.upper(), a, c)
		yes = ('y', 'yes', None)
		no = ('n', 'no')
		actions_yes = [
			raw_input(f(timestamp, id.upper(), amount, currency) + "\n> Press any key to continue..."),
			self.add(timestamp, id.upper(), amount, str(currency)),
			self.home_menu()
		]
		actions_no = [
			raw_input("> Operation aborted. Preass any key to continue...\n"),
			self.add_menu()
		]

		return (option, yes, no, actions_yes, actions_no)

	def remove_menu(self):
		self.header_menu()

def main():
	s = Stock()
	try:
		while True:
			next_menu(s.home_menu())

	except Exception as e:
		print(str(e))


if __name__ == '__main__':
	main()
