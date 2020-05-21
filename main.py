# -*- coding: utf-8 -*-
#!/usr/bin/python3
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

def next_menu(options):
	# TODO: accept dict with multiples options and their menus
	pass

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
			if not path.exists("data.json"):
				data = {}
				data["stocks"] = {}
			else:
				data = self.load("data.json")

			# if key exists
			if id.upper() in data["stocks"].keys():
				# if currency is equal
				if currency in data["stocks"][id.upper()]:
					data["stocks"][id.upper()][currency]["date"] = timestamp
					data["stocks"][id.upper()][currency]["amount"] = data["stocks"][id.upper()][currency]["amount"] + amount
				# other currency
				else:
					data["stocks"][id.upper()][currency] = {}
					data["stocks"][id.upper()][currency] = {
						"date": timestamp,
						"amount": amount
					}
			# if key not exists
			else:
				data["stocks"][id.upper()] = {}
				data["stocks"][id.upper()][currency] = {
					"date": timestamp,
					"amount": amount
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
		print("2. Show existing stocks.")
		print("3. Remove stock.")

		option = raw_input("\n> Select option: ")

		dict = {
			"1": lambda: self.add_menu(),
			"2": lambda: self.existing_menu(),
			"3": lambda: self.remove_menu()
		}

		return dict.get(option, lambda: 'Invalid')()

	def add_menu(self):
		self.header_menu()
		id = raw_input("> Enter id of stock: ")
		self.header_menu()
		amount = input("> Amount: ")
		self.header_menu()
		currency = input("> Currency value: ")
		self.header_menu()
		currency = "{:.2f}".format(currency)
		option = raw_input(
"""ID: {0}
Amount: {1}
Currency: {2}
\nThis is correct? ([y]/n): """.format(id.upper(), amount, currency))
		timestamp = get_timestamp()
		f = lambda t, i, a, c: "\n[Saved] {0} | {1} - {2} @ ${3}".format(t, i.upper(), a, c)
		yes = ("y", "yes", None)
		no = ("n", "no")
		actions_yes = [
			raw_input(f(timestamp, id.upper(), amount, str(currency)) + "\n> Press any key to continue..."),
			self.add(timestamp, id.upper(), amount, str(currency)),
			self.home_menu()
		]
		actions_no = [
			raw_input("> Operation aborted. Press any key to continue...\n"),
			self.add_menu()
		]

		return (option, yes, no, actions_yes, actions_no)

	def existing_menu(self):
		self.header_menu()
		data = self.load("data.json")
		stocks = {}

		for i, stock in enumerate(data['stocks'].items()):
			stocks[i + 1] = stock[0]
			print("{}. {}".format(i + 1, stock[0]))
		option = input("\n> ")

		self.header_menu()
		id = stocks[option]
		print("{0} {1} {0}".format("=" * 3, id))
		for currency in data['stocks'][id].keys():
			date = data['stocks'][id][currency]["date"]
			amount = data['stocks'][id][currency]["amount"]
			print("Date: {}".format(date))
			print("Amount: {} @ Currency: ${}".format(amount, currency))
			if len(data['stocks'][id].keys()) > 1:
				print("")

		o = raw_input("\n> Press any key to back to main menu...")

		return self.home_menu()

	def remove_menu(self):
		self.header_menu()

def main():
	s = Stock()

	try:
		while True:
			# next_menu(s.home_menu())
			s.home_menu()

	except Exception as e:
		print(str(e))


if __name__ == "__main__":
	main()
