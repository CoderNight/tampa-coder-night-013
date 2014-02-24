#include <QCoreApplication>
#include <QStringList>
#include <QDebug>

#include "xmlratereader.h"
#include "xmldomratereader.h"
#include "xqueryratereader.h"
#include "transactions.h"

#include "currency.h"

void readRates(const QString filename) {
    // Three of the different ways we can parse XML in Qt.
    // All are equivalent, Dom and XQuery are much smaller,
    // with Dom being easier to understand, but Xquery being
    // much more powerful in fewer lines.

    //readRatesUsingXQuery(filename);
    readRatesUsingXQuery2(filename);

    //XmlRateReader reader(filename);
    //reader.read();

    //readRatesFromXml(filename);
}

void runAllCombinations(const QString filename) {
    // Do all combinations to see if any of them trigger a rounding tie-breaker
    // Answer: nope
    QString b = "DM1182 DM1210 DM1230 DM1294 DM1537 DM1541 DM1724 DM1759 DM1786 DM1873";
    foreach (const QString &item_sku, b.split(" "))
        foreach (const QString &code, Currency::currencies())
            printf("%s %s %.2f\n",
                   qPrintable(item_sku),
                   qPrintable(code),
                   (float)totalTransactions(filename, item_sku, code));
}

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);
    QString currency("USD"), sku("DM1182");
    QStringList args = a.arguments();
    switch(args.size()) {
    default:
        qDebug() << "Usage:" << qPrintable(args[0]) << "rates.xml transactions.csv [sku [currency]]";
        return 1;
    case 5:
        currency = args[4];
    case 4:
        sku = args[3];
    case 3:
        break;
    }

    readRates(args[1]);

    // Read in sales csv and find total sales in currency for sku
    printf("%.2f\n", (float)totalTransactions(args[2], sku, currency));

    //runAllCombinations(args[2]);
    return 0;
}
