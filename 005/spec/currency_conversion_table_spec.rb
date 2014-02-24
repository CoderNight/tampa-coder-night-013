require_relative '../international_trade'

class InternationalTrade
  describe CurrencyConversionTable do
    before(:each) do
      conv1 = { conversion: '2.00', from: 'TestCurrency', to: 'TestCurrency2' }
      conv2 = { conversion: '2.00', from: 'TestCurrency2', to: 'TestCurrency3' }
      @table = CurrencyConversionTable.new conv1, conv2
    end

    describe 'Currency converison' do
      it 'converts currency' do
        value = @table.convert(from: 'TestCurrency', to: 'TestCurrency2', amount: '1.00')
        expect(value).to eq BigDecimal('2.00')
      end

      describe 'When no direct conversion is available' do
        it 'infers a conversion' do
          table = @table
          value = table.convert(from: 'TestCurrency', to: 'TestCurrency3', amount: '1.00')
          expect(value).to eq BigDecimal('4.00')
        end

        it 'adds a direct conversion once one is inferred' do
          table = @table
          expect(find_conversion(table, 'TestCurrency', 'TestCurrency3')).to be nil
          table.convert(from: 'TestCurrency', to: 'TestCurrency3', amount: '1.00')
          new_conversion = find_conversion(table, 'TestCurrency', 'TestCurrency3')
          expect(new_conversion).to_not be nil
        end

        def find_conversion(table, from, to)
          table.find {|conv| conv.from == from && conv.to == to }
        end
      end
    end
  end
end
