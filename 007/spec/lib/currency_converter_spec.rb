require 'spec_helper'
require 'currency_converter'

describe CurrencyConverter do

  before(:each) do
    @cc = CurrencyConverter.new
  end

  let(:xml_text) { IO.read(fixture('SAMPLE_RATES.xml')) }

  let(:table) do
    {
      'AUD' => { 'CAD' => 1.0079 },
      'CAD' => { 'USD' => 1.0090 },
      'USD' => { 'CAD' => 0.9911 },
    }
  end

  let(:permutations) do
    {
      'AUD' => { 'CAD' => 1.0079, 'USD' => nil },
      'CAD' => { 'USD' => 1.0090, 'AUD' => nil },
      'USD' => { 'CAD' => 0.9911, 'AUD' => nil },
    }
  end

  it "builds an initial table from XML" do
    expect(@cc.build_table(xml_text)).to eql(table)
  end

  it "builds all permutations" do
    expect(@cc.build_permutations(table)).to eql(permutations)
  end

  it "finds common currency shared by USD and AUD" do
    expect(@cc.find_common_currency('USD', 'AUD', permutations)).to eql('CAD')
  end

  it "converts through 2 currencies" do
    pending
    expect(@cc.convert_through(1, 2, 1, 2)).to eql(4.0)
  end

  it "reverses the rate" do
    pending
    expect(@cc.convert_opposite_currency(1,2)).to eql(0.5)
  end

end
