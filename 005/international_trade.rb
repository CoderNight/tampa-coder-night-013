require 'csv'
require 'bigdecimal'

class InternationalTrade
  require_relative 'international_trade/sales_transactions'
  require_relative 'international_trade/currency_conversion_table'

  attr_reader :transactions, :conversions

  def initialize(transactions, conversions)
    @transactions = transactions
    @conversions  = conversions
  end

  def sum_sales_for(sku, currency)
    sku_items = transactions.reject {|t| t if t.sku != sku }
    total = sku_items.inject(BigDecimal('0')) do |result, sku_item|
      converted_value = convert_currency(amount: sku_item.amount,as: currency)
      result + converted_value
    end
    total.round(2, BigDecimal::ROUND_HALF_EVEN).to_s('F')
  end

private
  def convert_currency(opts={})
    as     = opts.fetch(:as)
    amount, from_currency = *(opts.fetch(:amount).split)

    as == from_currency ? BigDecimal(amount) :
      conversions.convert(from: from_currency, to: as, amount: amount)
  end
end
