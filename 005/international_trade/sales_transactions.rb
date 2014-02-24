class InternationalTrade
  class SalesTransactions
    include Enumerable
    TransactionItem = Struct.new(:store, :sku, :amount)

    attr_reader :transactions

    def initialize(items)
      @transactions = items.collect {|transaction| TransactionItem.new(*transaction) }
    end

    def each(&block)
      @transactions.each {|transaction| block.call(transaction) }
    end
  end
end
