class CurrencyConverter
  require 'rexml/document'
  require 'set'

  def build_table(xml)
    table = {}
    doc = REXML::Document.new(xml)
    doc.root.get_elements('rate').each do |e|
      from = e.get_text('from').to_s
      to = e.get_text('to').to_s
      conversion = e.get_text('conversion').to_s.to_f
      table[from] ||= {}
      table[from][to] = conversion
    end
    table
  end

  def build_permutations(table)
    s = Set.new
    table.each do |k, v|
      s.add(k)
      v.keys.each { |k| s.add(k) }
    end
    s.to_a.repeated_permutation(2) do |to, from|
      next if to == from
      table[to] ||={}

      unless table[to][from]
        table[to][from] = nil
      end
    end
    table
  end

  def convert_through(from_a, to_a, from_b, to_b)
    (to_a / from_a.to_f) * (to_b / from_b.to_f)
  end

  def convert_opposite_currency(from_currency, to_currency)
    1.0 / (to_currency / from_currency)
  end

  def find_common_currency(from, to, table)
    table[from].keys.each do |k|
      return k if table[k].has_key?(to)
    end
    return nil
  end
end
