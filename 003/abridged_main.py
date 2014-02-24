from collections import defaultdict
from csv import reader
from decimal import Decimal, ROUND_HALF_EVEN
from xml.etree import ElementTree


class InternationalTrade():
    rates = defaultdict(Decimal)
    currencies = set()

    def deriveMissingRate(self, tried, frm, to):
        if self.rates[(frm, to)]:
            return self.rates[(frm, to)]

        tried.add(frm)
        untried = self.currencies - tried - {to}

        for nextFrm in untried:
            if self.rates[(frm, nextFrm)]:
                nextRate = self.deriveMissingRate(tried, nextFrm, to)
                if nextRate:
                    self.rates[(frm, to)] = self.rates[(frm, nextFrm)] * nextRate
                    return self.rates[(frm, to)]
        else:
            return None


    def getRates(self, ratesFile, findMissing=False):
        for rate in ElementTree.parse(ratesFile).getroot().iter('rate'):
            frm = rate.find('from').text
            to = rate.find('to').text
            self.rates[frm, to] = Decimal(rate.find('conversion').text)

            self.currencies.add(frm)
            self.currencies.add(to)

        if findMissing:
            for frm in self.currencies:
                for to in self.currencies:
                    if frm != to and not self.rates[(frm, to)]:
                        self.rates[(frm, to)] = self.deriveMissingRate(set(), frm, to, 0)
        return


    def getTransactions(self, transFile):
        with open(transFile) as csvfile:
            while True:
                (_store, sku, amount) = reader(csvfile).next()

                try:
                    (amt, currency) = amount.split()
                except ValueError:
                    continue

                yield (Decimal(amt), sku, currency)


    def tallyTransactions(self, transFile, item, toCurrency):
        total = Decimal(0);

        for amt, sku, transCurrency in self.getTransactions(transFile):
            if not item or sku == item:
                if transCurrency == toCurrency:
                    subtotal = Decimal(amt)

                else:
                    if not self.rates[(transCurrency, toCurrency)]:
                        if not self.deriveMissingRate(set(), transCurrency, toCurrency):
                            print "\nNo conversion found for %s-->%s" % (transCurrency, toCurrency)
                            raise SystemExit

                    subtotal = Decimal(amt * self.rates[(transCurrency, toCurrency)])

                total += subtotal.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)

        return total


if __name__ == '__main__':
    it = InternationalTrade()
    rates = it.getRates("data/SAMPLE_RATES.xml")
    print "Sample files: %s" % it.tallyTransactions("data/SAMPLE_TRANS.csv", "DM1182", "USD")

    it = InternationalTrade()
    rates = it.getRates("data/RATES.xml")
    print "Real files: %s" % it.tallyTransactions("data/TRANS.csv", "DM1182", "USD")