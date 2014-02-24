#!/usr/bin/env ruby
require_relative '../international_trade'
require 'active_support/core_ext'


TRANSACTION_DATA = ARGV[0] || 'TRANS.csv'
CONVERSION_DATA  = ARGV[1] || 'RATES.xml'

transactions = InternationalTrade::SalesTransactions.new(CSV.read(TRANSACTION_DATA))

# Lets' cheat here and use ActiveSupport instead of Nokogiri
#conversion_rate_data = Nokogiri::XML(File.open(CONVERSION_DATA)).xpath('//rates/rate').
#    collect {|rate_doc| rate_doc.inner_text.split }

conversion_rate_data = Hash.from_xml(File.open(CONVERSION_DATA))['rates']['rate'].
  map(&:symbolize_keys)
conversions = InternationalTrade::CurrencyConversionTable.new(*conversion_rate_data)

puts InternationalTrade.new(transactions, conversions).sum_sales_for('DM1182', 'USD')
