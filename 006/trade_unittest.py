'''
Created on Jan 27, 2014

@author: Chris
'''

import os 
import csv 
from trade import *
import unittest


class Test(unittest.TestCase):
	sample_trans = format_transaction_details(load_csv('SAMPLE_TRANS.csv'))
	sample_rates = xml_to_list(load_xml('SAMPLE_RATES.xml'))
	
	trans = format_transaction_details(load_csv('TRANS.csv'))
	rates = xml_to_list(load_xml('RATES.xml'))
	
	target_sku = 'DM1182'

	def setUp(self):
		self.sample_cache = build_rates_cache(self.sample_rates)
		self.cache = build_rates_cache(self.rates)
		
	def tearDown(self):
		self.sample_cache = None
		self.cache = None
	
	def test_half_to_even_round_returns_0_from_0(self):
		num = round_(0.0)
		self.assertEqual(num, 0)
		
	def test_half_to_even_rounds_two_decimal_places_correctly(self):
		a = float(round_(54.1754))
		b = float(round_(343.2050))
		c = float(round_(106.2038))
		self.assertEqual(a, 54.18)
		self.assertEqual(b, 343.20)
		self.assertEqual(c, 106.20)
		
	def test_cache_formats_keys_correctly(self):
		test_data = [('USD', 'EUR', 52.23)]
		expected_key = 'FROM_EUR_TO_USD'
		c = build_rates_cache(test_data)
		self.assertTrue(expected_key in c)
		
	def test_format_transaction_details__returns_split_fields(self):
		test_data =[['store', 'sku', '18.23 USD']] 
		expected = Transaction('store', 'sku', 18.23, 'USD')
		actual 	 = next(format_transaction_details(test_data))
		self.assertEqual(expected, actual)
		
	def test_find_curreny_conversion__matching_to_from_fields__returns_one(self):
		self.assertEqual(find_curreny_conversion(None, 'USD', 'USD', None), 1)
		
	def test_find_curreny_conversion__no_match__returns_none(self):
		self.assertEqual(find_curreny_conversion(self.rates, 'USD', 'ZZZ', self.cache), None)
		
	def test_find_curreny_conversion__finds_match_2_levels_deep__returns_proper_amount(self):
		expected = 1.0169711
		result = find_curreny_conversion(self.rates, 'USD', 'AUD', self.cache)
		self.assertEqual(expected, result)
	
	def test_find_curreny_conversion__finds_match_3_levels_deep__returns_proper_amount(self):
		expected = 1.36701255262
		actual   = find_curreny_conversion(self.rates, 'USD', 'EUR', self.cache)
		self.assertEqual(round(actual,len('36701255262')), expected)
		
	def test_calculate_grand_total__sample_trans__returns_134_22(self):
		target_sku = 'DM1182'
		total = sum(calculate_grand_total(self.sample_trans, target_sku, self.sample_rates, self.sample_cache))	
		self.assertEqual(float(total), 134.22)
	

if __name__ == "__main__":
		#import sys;sys.argv = ['', 'Test.testName']
		unittest.main()