#include "transactions.h"

#include <math.h> // fabs, ceil, floor, round

#include <QFile>
#include <QByteArray>
#include <QStringList>
#include <QDebug>

#include "currency.h"

double roundToEven(double value) {
    // Only need tie-breaker if the fraction is 0.5 exactly, then return nearest even
    if (qFuzzyCompare(fabs(value - trunc(value)), 0.5)) {
        qDebug("***** rounding tie-breaker *****");
        if (int(ceil(value)) % 2 == 0)
            return ceil(value);
        return floor(value);
    }
    return round(value);
}

void visuallyCheckRounding() {
    QList<double> nums;
    nums << 24.50 << 23.67 << 23.50 << 23.35 << 23.00 << 0 << -23.00 << -23.35 << -23.50 << -23.67 << -24.50;
    foreach (double f, nums)
        qDebug() << f << roundToEven(f);
}

// Read in a csv file containing transactions in the following format:
// location,item_sku,sales_amount currency_code
// Total all sales for a given item_sku in the requested currency
double totalTransactions(QString filename, QString item, QString currency) {
    // for each line, split, if matches item, get currency, convert, add to total
    double sum = 0.0;
    QFile csv(filename);
    csv.open(QIODevice::ReadOnly);
    while (true) {
        QString line = csv.readLine();
        if (line.isEmpty())
            break;
        QStringList split = line.split(QRegExp("[, \n]"));
        if (split.size() < 4 || split[1] != item)
            continue;
        bool ok = false;
        double amount = split[2].toDouble(&ok);
        Currency *c = Currency::get(split[3]);
        if (!ok) {
            qDebug() << "Failed to parse amount:" << split[2];
            continue;
        }
        if (!c)
            continue;
        sum += roundToEven(amount * c->to(currency) * 100.0) / 100.0;
    }
    return sum;
}
