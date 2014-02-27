package main

import (
	. "./trade"
	csv "encoding/csv"
	xml "encoding/xml"
	"io/ioutil"
	"os"
)

func getFiles() (ratesFile *os.File, txnFile *os.File) {
	ratesFileName, txnFileName := os.Args[1], os.Args[2]
	ratesFile, _ = os.Open(ratesFileName)
	txnFile, _ = os.Open(txnFileName)
	return
}

func Unmarshal(file *os.File, v interface{}) {
	b, _ := ioutil.ReadAll(file)
	xml.Unmarshal(b, v)
}

func getRates(file *os.File) RateList {
	rates := RateList{}
	Unmarshal(file, &rates)
	return rates
}

func getTransactions(file *os.File) []Transaction {
	txnReader := csv.NewReader(file)
	return ParseTransactions(txnReader)
}

func main() {
	rateFile, txnFile := getFiles()
	defer rateFile.Close()
	defer txnFile.Close()
	rates := getRates(rateFile)
	txns := getTransactions(txnFile)
	print(rates.Length(), " rates known\n")
	print(len(txns), " transactions parsed\n")
	print("DM1182 total : $", SalesTotal("DM1182", "USD", rates, txns), "\n")
}
