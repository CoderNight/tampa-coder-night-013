package trade

import (
	"errors"
	"strconv"
	"strings"
)

type Transaction struct {
	store string
	sku   string
	cost  Cost
}

type Cost struct {
	value float64
	unit  string
}

type tRecord []string

type cRecord []string

type TransactionReader interface {
	Read() ([]string, error)
}

func (t *Transaction) Value() float64 {
	return t.cost.value
}

func (t *Transaction) Unit() string {
	return t.cost.unit
}

func (t *Transaction) HasUnit(unit string) bool {
	return t.cost.unit == unit
}

func (r cRecord) ReadCost() Cost {
	value, _ := strconv.ParseFloat(r[0], 64)
	return Cost{value, r[1]}
}

func (r tRecord) ReadTransaction() (Transaction, error) {
	cr := cRecord(strings.Split(r[2], " "))
	if len(cr) < 2 {
		return Transaction{}, errors.New("bad cost")
	}
	return Transaction{r[0], r[1], cr.ReadCost()}, nil
}

func ParseTransactions(reader TransactionReader) (txns []Transaction) {
	for {
		txnRecord, status := reader.Read()
		if status != nil {
			break
		}
		if len(txnRecord) < 3 {
			continue
		}
		if txn, err := tRecord(txnRecord).ReadTransaction(); err == nil {
			txns = append(txns, txn)
		}
	}
	return
}
