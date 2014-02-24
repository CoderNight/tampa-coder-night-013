from collections import defaultdict
from csv import reader
from decimal import Decimal, ROUND_HALF_EVEN
from xml.etree import ElementTree
from traceback import format_exc


class InternationalTrade():
    """Solve InternationTrade puzzle.

    This class implements a solution to the coding challenged posed at:
        http://www.puzzlenode.com/puzzles/1-international-trade

    As stated there:
        "You have been given two files. The first is an XML file containing the conversion rates
         for exchanging one currency with another. The second is a CSV file containing sales data
         by transaction for an international business. Your goal is to parse all the transactions
         and return the grand total of all sales for a given item.

         Problem:
             What is the grand total of sales for item DM1182 across all stores in USD currency?"

    An added feature of this implementation is to optionally output any of three types of
    debugging info. This is especially helpful to understand what is happening in the recursive
    method used to derive missing conversion rate values.

    Attributes:
        rates (defaultdict of Decimal): Dictionary of conversion rates, keyed by ('from', 'to').
        currencies (set or str): Set of all the encountered currencies.

        verboseRates (bool): Whether to output debug info while learning rates.
        verboseMissing (bool): Whether to output debug info while deriving missing rates.
        verboseTrans  (bool): Flag used to output debug info while scanning transactions.

    """

    rates = defaultdict(Decimal)
    currencies = set()

    verboseRates = False
    verboseMissing = False
    verboseTrans = False

    def __init__(self, verboseRates=False, verboseMissing=False, verboseTrans=False):
        """Inits InternationalTrade with debugging flags.

        Args:
            verboseRates (opt bool): Whether to output debug info while getting input rates.
            verboseMissing (opt bool): Whether to output debug info  while deriving missing rates.
            verboseTrans (opt bool): Whether to output debug info while getting and tallying
                                     transactions.

        """

        self.verboseRates = verboseRates
        self.verboseMissing = verboseMissing
        self.verboseTrans = verboseTrans


    def deriveMissingRate(self, tried, frm, to, indent=0):
        """Recursively derive a missing conversion rate.

        This method recursively derives a missing conversion rate value. The algorithm used is:
            1. If there is a conversion rate value from currency 'frm' to currency 'to', stop
               recursing and return the conversion rate.
            2. Add currency 'frm' to the set of tried currencies.
            3. Use the set of tried currencies to create a set of untried currencies.
            4. For each of the currencies in the set in untried ones:
                4a. If there's is a known conversion to the 'to' currency:
                    4a1. Recursively attempt to find a conversion to currency 'to'.
                    4a2. If that returned a value, save and return the conversion rate.
            5. If no conversion was found for any of the untried values, stop recursing and return
               None signal that there is no conversion from currency 'frm' to currency 'to'.

        Side-effect: Note that to avoid repeating any derivations, any intermediate missing rates
        that are derived in the course of deriving the requested missing rate are saved in the
        dictionary as they are encountered.

        Args:
            tried (set of str): Set of currencies that have already been tried
                                and don't need to be considered.
            frm (str): Currency that needs to be converted.
            to (str): Desired output currency.
            indent (optional int): Number of indents to use for debugging output.

        Returns:
            The derived missing conversion rate or None if unable to derive rate.
        """

        if self.verboseMissing: print "%sAttempting to derive %s-->%s" % ("  " * indent, frm, to)

        # If there's a direct conversion, just return it:
        if self.rates[(frm, to)]:
            return self.rates[(frm, to)]

        tried.add(frm)
        untried = self.currencies - tried - {to}

        # Recursively try every combination:
        for nextFrm in untried:
            if self.verboseMissing: print "%s Considering %s-->%s" % ("  " * indent, frm, nextFrm)

            if self.rates[(frm, nextFrm)]:
                nextRate = self.deriveMissingRate(tried, nextFrm, to, indent+1)

                # If there's a conversion rate, use it to derive the missing conversion rate,
                #     saving the value for possible future use:
                if nextRate:
                    self.rates[(frm, to)] = self.rates[(frm, nextFrm)] * nextRate
                    if self.verboseMissing:
                        print "%s  Setting %s-->%s = %s" % ("  " * indent, frm, to,
                                                            self.rates[(frm, to)])
                    return self.rates[(frm, to)]

        else:
            # No solution found; give up:
            if self.verboseMissing: print "%s Path %s-->%s didn't work" % ("  " * indent, frm, to)
            return None


    def getRates(self, ratesFile, findMissing=False):
        """Input and build a dictionary or rates.

        Read in the specified rates XML file, which is formatted like the
        following, and build a conversion rates dictionary.

            <rates>
              <rate>
                <from>AUD</from>
                <to>CAD</to>
                <conversion>1.0079</conversion>
              </rate>
              <rate>
                <from>CAD</from>
                <to>USD</to>
                <conversion>1.0090</conversion>
              </rate>
              <rate>
                <from>USD</from>
                <to>CAD</to>
                <conversion>0.9911</conversion>
              </rate>
            </rates>

        Args:
            ratesFile(str); Name of the files with the rates data.
            FindMissing (opt bool): Whether to preemptively derive all the missing conversion rates.


        Returns:
            Nothing

        Raises:
            IOError: Unable to open and read in rates from the file.
        """
        try:
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
                            if self.verboseRates: print
                            self.rates[(frm, to)] = self.deriveMissingRate(set(), frm, to, 0)

            if self.verboseRates:
                print
                for rate in sorted(self.rates.items()):
                    if rate[0][0] != rate[0][1]:
                        print "%s-->%s = %s" % (rate[0][0], rate[0][1], rate[1])
                print

            return

        except IOError as e:
            print "Unable to open and read conversion rates\n(%s)" % e
            raise SystemExit


    def getTransactions(self, transFile):
        """Opens and reads transactions from a file.

        Read in the specified transactions CSV file, which is formatted like the
        following, and return a generator that can be use to iterate the file:

            store,sku,amount
            Utica,DM1759,84.16 CAD
            Albany,DM1786,91.34 AUD
            Albany,DM1724,27.19 USD

        Args:
            transFile (str): A path to the transactions file.

        Yields:
            A tuple with the following:

            amt (Decimal): Amount converted into a Decimal value.
            sku (str): Items SKU number.
            currency (str): Transaction's currency type.

        Raises:
            IOError: Unable to open and read in transaction from the file.

        """
        try:
            with open(transFile) as csvfile:
                while True:

                    (store, sku, amount) = reader(csvfile).next()

                    try:
                        (amt, currency) = amount.split()
                    except ValueError:
                        # Ignore header row and other bad input lines
                        continue

                    if self.verboseTrans: print "%s %s of item %s was sold in %s" \
                                                % (amt, currency, sku, store)

                    yield (Decimal(amt), sku, currency)

        except IOError as e:
            print "Unable to open and read transactions\n(%s)" % e
            raise #SystemExit



    def tallyTransactions(self, transFile, item, toCurrency):
        """Computes a tally of items sold.

        Iterate the specified transaction file and calculate, in the specified
        currency, the total amount spent for specified item.

        Args:
            transFile (str): A path to the transactions file.
            item (str): The SKU of the desired item or None for all items.
            toCurrency (str): The currency in which to calculate the total.

        Returns:
            The total amount of the items sold expressed in the desired currency.

        Raises:
            MissingConversionError: A transaction's currency can't be converted.

        """

        total = Decimal(0);

        for amt, sku, transCurrency in self.getTransactions(transFile):
            if not item or sku == item:
                # This could also be handled by just setting conversion to self to 1.0:
                if transCurrency == toCurrency:
                    subtotal = Decimal(amt)

                else:
                    # Derive a missing conversion rates on demand:
                    if not self.rates[(transCurrency, toCurrency)]:
                        if not self.deriveMissingRate(set(), transCurrency, toCurrency):
                            print "\nNo conversion found for %s-->%s" % (transCurrency, toCurrency)
                            raise SystemExit

                    subtotal = Decimal(amt * self.rates[(transCurrency, toCurrency)])

                total += subtotal.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)

        if self.verboseTrans:
            print "\n%s %s of item %s was sold\n" % (total, toCurrency, item)

        return total


if __name__ == '__main__':
    try:
        it = InternationalTrade(verboseRates=True, verboseMissing=True, verboseTrans=True)
        rates = it.getRates("data/SAMPLE_RATES.xml", findMissing=True)
        print "Sample files: %s" % it.tallyTransactions("data/SAMPLE_TRANS.csv", "DM1182", "USD")

        it = InternationalTrade()
        rates = it.getRates("data/RATES.xml")
        print "Real files: %s" % it.tallyTransactions("data/TRANS.csv", "DM1182", "USD")

    # TODO: Add/use a custom exception:
    except SystemExit:
        print "\nAborting!\n"

    except Exception as e:
        print "\n%s\nUnhandled exception; aborting!\n\n" % format_exc()
