package trade

func filterTxns(sku string, txns []Transaction) (result []Transaction) {
	for _, txn := range txns {
		if txn.sku == sku {
			result = append(result, txn)
		}
	}
	return
}

func sumOf(currency string, txns []Transaction, rates RateList) (result float64) {
	ratemap := rates.ToMap()
	for _, txn := range txns {
		result = result + ratemap.Convert(currency, txn)
	}
	return result
}

func SalesTotal(sku string, currency string, rates RateList, txns []Transaction) float64 {
	relatedTxns := filterTxns(sku, txns)
	return sumOf(currency, relatedTxns, rates)
}
