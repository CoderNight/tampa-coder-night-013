package trade

type Conversions map[string]float64

type RateMap map[string]Conversions

type RateList struct {
	Rates []Rate `xml:"rate"`
}

type Rate struct {
	from       string
	to         string
	conversion float64
}

func (rs *RateList) Length() int {
	return len(rs.Rates)
}

func (m *RateMap) LookupConversion(from string, txn Transaction) (float64, bool) {
	conversions := (*m)[txn.Unit()]
	lookup, ok := conversions[from]
	if ok {
		return lookup * txn.Value(), true
	}
	for knownUnit, knownConversionRate := range conversions {
		conversion, ok := m.LookupConversion(knownUnit, txn)
		if ok {
			return knownConversionRate * conversion, true
		}
	}
	return 0.0, false
}

func (m *RateMap) Convert(currency string, txn Transaction) float64 {
	if txn.HasUnit(currency) {
		return txn.Value()
	} else {
		conversion, _ := m.LookupConversion(currency, txn)
		return conversion
	}
}

func (rates *RateList) Filter(currency string) (result RateList) {
	for _, rate := range rates.Rates {
		if rate.from == currency {
			result.Rates = append(result.Rates, rate)
		}
		if rate.to == currency {
			newConversion := 0.0
			if rate.conversion > 0 {
				newConversion = 1.0 / rate.conversion
			}
			result.Rates = append(result.Rates, Rate{rate.to, rate.from, newConversion})
		}
	}
	return
}

func (rs *RateList) ToMap() (result RateMap) {
	result = map[string]Conversions{}
	for _, rate := range rs.Rates {
		conversions := map[string]float64{}
		for _, conv := range rs.Filter(rate.from).Rates {
			conversions[conv.to] = conv.conversion
		}
		result[rate.from] = conversions
	}
	return
}
