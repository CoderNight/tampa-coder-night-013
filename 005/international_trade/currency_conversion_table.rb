class InternationalTrade
  class CurrencyConversionTable
    include Enumerable
    attr_reader :items

    class ConversionItem
      attr_reader :conversion, :from, :to
      def initialize(attrs={})
        @conversion = attrs.fetch(:conversion)
        @from = attrs.fetch(:from)
        @to   = attrs.fetch(:to)
      end
    end

    def initialize(*items)
      @items = items.collect { |item| ConversionItem.new(item) }
    end

    def each(&block)
      @items.each {|item| block.call(item) }
    end

    def convert(opts={})
      from   = opts.fetch(:from)
      to     = opts.fetch(:to)
      amount = opts.fetch(:amount)
      conversion_item = find_conversion(from, to)
      BigDecimal(amount.to_s) * BigDecimal(conversion_item.conversion.to_s)
    end

  private

    def add(conv)
      @items << conv
    end

    def find_conversion(from, to)
      find {|conv| conv.from == from && conv.to == to } ||
        inferred_conversion(from, to)
    end

    def converts_from(from)
      reject {|conv| conv unless conv.from == from }
    end

    def converts_to(to)
      reject {|conv| conv unless conv.to == to }
    end


    def inferred_conversion(from, to)
      intermediate1 = converts_from(from).
        find {|conv| converts_to(to).collect{|conv2| conv2.to == to }.any? }
      intermediate2 = converts_to(to).find {|conv| conv.from == intermediate1.to } ||
        inferred_conversion(intermediate1.to, to)

      build_inferred_conversion(from, to, intermediate1, intermediate2)
    end

    def build_inferred_conversion(from, to, conv1, conv2)
      conversion = conv1.conversion.to_f * conv2.conversion.to_f
      conversion_item = ConversionItem.new(from: from, to: to, conversion: conversion)
      add(conversion_item)
      conversion_item
    end
  end
end
