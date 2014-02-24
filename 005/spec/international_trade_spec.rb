require_relative '../international_trade'

describe InternationalTrade do
  before :each do
    sale_item = Struct.new(:amount, :sku, :store)
    sales = [] << sale_item.new('1.00 TestCurrency', '1000', 'MyStore')
    sales << sale_item.new('1.00 TestCurrency', '1000', 'MyStore')
    conversions = InternationalTrade::CurrencyConversionTable.new
    conv_item = Struct.new(:from, :to, :conversion)
    conversions.add conv_item.new('TestCurrency', 'TestCurrency2', '2.00')

    @trader = InternationalTrade.new(sales, conversions)
  end

  it 'adds sales for a given sku' do
    total = @trader.sum_sales_for('1000', 'TestCurrency')
    expect(total).to eq BigDecimal('2').to_s('F')

    total = @trader.sum_sales_for('1000', 'TestCurrency2')
    expect(total).to eq BigDecimal('4').to_s('F')
  end
end
