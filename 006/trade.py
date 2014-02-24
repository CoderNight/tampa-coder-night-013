'''
Created on Jan 27, 2014

@author: Chris
'''

import os
import csv
import decimal
import operator
import itertools
from bs4 import BeautifulSoup
from collections import namedtuple

Transaction = namedtuple('Transaction', ['store', 'sku', 'amount','currency']) 
Rate 				= namedtuple('rate', ['TO', 'FROM', 'EXCHANGE_RATE']) # caps, cause namedtuple has weird _ restrictions


def load_csv(filename):
	''' loads a csv file from the examples dir'''
	_path = os.path.join('examples', filename)
	with open(_path, 'rb') as f:
		csvreader = csv.reader(f, delimiter=',')
		return [x for x in csvreader][1:]
	
def load_xml(filename):
	''' loads an xml file from the examples dir'''
	_path = os.path.join('examples', filename)
	with open(_path, 'rb') as f:
		return BeautifulSoup(f.read())
	
def xml_to_list(xml_rates):
	''' Converts the input XML into a flat list '''
	_to = lambda x: x.find('to').get_text()
	_from = lambda x: x.find('from').get_text()
	_amount = lambda x: float(x.find('conversion').get_text())
	return [Rate(_to(rate), _from(rate),  _amount(rate))
					for rate in xml_rates.find_all('rate')]
				
def build_rates_cache(rates):
	''' 
	Builds a dictionary cache for quick lookup and 
	storage of previously calculated conversion rates
	
	Key style: 
		FROM_%s_TO_%s
	e.g.
		FROM_CAD_TO_USD
	Returns: 
		dictionary of Rates mapped to their values
	''' 
	
	return {'FROM_%s_TO_%s' % (_from, _to) : val 
					for (_to, _from, val) in rates}
	
def format_transaction_details(transaction_details):
	''' 
	Splits the joined amount/currency column into two fields 
	to make parsing/searching easier. 
	e.g. ['store', 'sku', '18.23 USD'] becomes ['store', 'sku', '18.23', 'USD'] 
		 
	Returns rows as a namedtuple for conveinent access
	'''
	for row in transaction_details:
		store, sku, amount = row 
		money, currency = amount.split()
		yield Transaction(store, sku, float(money), currency)

def round_(n):
	''' 
	Rounds to the nearest even number according to 'bankers rule'
	
	Args: 
		n	-> Number to round
	Returns: 
		Rounded Decimal
	'''
	decimal.getcontext().rounding = decimal.ROUND_HALF_UP
	return decimal.Decimal(n).quantize(
																decimal.Decimal('.01'), 
																rounding=decimal.ROUND_HALF_EVEN)
	
def my_terrible_search_function_helper(rates, _to, _from, prev_rate, p=[]):
	''' 
	helper function for the rate search. It's exactly the same as 
	its parent method, but stores all of its results in a list.   
	'''
	rates_with_TOs = [rate for rate in rates if rate.TO == _to and (prev_rate.TO != rate.FROM or rate.TO != prev_rate.FROM)]
	for rate in rates_with_TOs: 
		if rate.FROM != _from:
			p.append(rate)
			my_terrible_search_function_helper(rates, rate.FROM, _from, rate, p)
			return p
		else:
			p.append(rate)
			return p

def my_terrible_search_function(rates, _to, _from):
	''' 
	This is the best I could come up with after... 4... hours..
	Inefficiently finds a conversion path between the FROM and TO 
	currencies. 
	
	Algorithm: 
		Find all RATES which have the same TO field as the target currency. 
		For each rate in the found RATES, repeat the same search pattern, but 
		using the rate's TO field. 
		 
	'''
	rates_with_matching_to_fields = [rate for rate in rates if rate.TO == _to]
	for rate in rates_with_matching_to_fields: 
		output = []
		if rate.FROM != _from:
			output.append(rate)
			output.extend(my_terrible_search_function_helper(rates, rate.FROM, _from, rate, []))
			if _from in [rate.FROM for rate in output]:
				return output
			continue
	return None


def find_curreny_conversion(rates, _to, _from, cache):
	''' 
	Checks the cache for the currency conversion. If not 
	found, it then searches the rates listing for a possible 
	match.
	
	Args: 
		rates	-> list of all available currency rates
		_to 	-> target currency
		_from	-> Currency from which we're converting
		cache -> previously found conversions
	
	Returns 
		Float currency conversion value
	'''
	if _from == _to:
		return 1 	# multiplicative identity, not a status code
	key = 'FROM_%s_TO_%s' % (_from,_to)
	if key not in cache:
		results = my_terrible_search_function(rates, _to, _from)
		if not results:
			return None
		new_rate = reduce(operator.mul, 
										[r.EXCHANGE_RATE for r in results])
		cache[key] = new_rate 
	return cache[key]
	
def calculate_grand_total(transactions, sku, rates, cache):
	for transaction in transactions: 
		if transaction.sku == sku: 
			yield round_(transaction.amount * find_curreny_conversion(rates, 'USD', transaction.currency, cache))

def display_total(sku, total):
	msg = 'Grand total for {sku}: {total}'
	print msg.format(sku=sku, total=total)
	
if __name__ == '__main__':
	transactions = format_transaction_details(load_csv('TRANS.csv'))
	rates = xml_to_list(load_xml('RATES.xml'))
	cache = build_rates_cache(rates)
	target_sku = 'DM1182'
	
	total = sum(calculate_grand_total(transactions, target_sku))
	display_total(target_sku, total)
			
	
	
	
	
	
	
	
	
	
	
	


