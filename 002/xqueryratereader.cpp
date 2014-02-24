#include "xqueryratereader.h"

#include <QtXmlPatterns/QXmlQuery>
#include <QStringList>
#include <QFileInfo>
#include <QDebug>

#include "currency.h"

// Notes: my biggest issue with this design is that the different pieces of
//        each rate are pulled out separately. I would prefer one query that
//        pulled them out in sets.
void readRatesUsingXQuery(const QFileInfo file) {
    const QString queryUrl = QString("doc('%1')//rate/%2/string()").arg(file.absoluteFilePath());

    typedef QPair<QStringList &, QString> QueryPair;
    QList<QueryPair> queries;
    QStringList from, to, conversion;
    queries << QueryPair(from, "from") << QueryPair(to, "to") << QueryPair(conversion, "conversion");
    QXmlQuery query;
    foreach (QueryPair pair, queries) {
        query.setQuery(queryUrl.arg(pair.second));
        query.evaluateTo(&pair.first);
    }
    if (to.size() != from.size() || to.size() != conversion.size())
        return;
    for (int i = 0; i < to.size(); ++i)
        Currency::addRate(from.at(i), to.at(i), conversion.at(i));
}

// Same as method above but without any pizzazz. Note that it's only one line shorter.
void readRatesUsingXQuery_expanded(const QFileInfo file) {
    const QString queryUrl = QString("doc('%1')//rate/%2/string()").arg(file.absoluteFilePath());

    QStringList from, to, conversion;
    QXmlQuery query;
    query.setQuery(queryUrl.arg("from"));
    query.evaluateTo(&from);
    query.setQuery(queryUrl.arg("to"));
    query.evaluateTo(&to);
    query.setQuery(queryUrl.arg("conversion"));
    query.evaluateTo(&conversion);
    if (to.size() != from.size() || to.size() != conversion.size())
        return;
    for (int i = 0; i < to.size(); ++i)
        Currency::addRate(from.at(i), to.at(i), conversion.at(i));
}

void readRatesUsingXQuery2(const QFileInfo file) {
    const QString queryUrl = QString("doc('%1')//rate/string-join((from, to, conversion)/string(), ',')")
                             .arg(file.absoluteFilePath());

    QStringList rates;
    QXmlQuery query;
    query.setQuery(queryUrl);
    query.evaluateTo(&rates);
    foreach (const QString &rate, rates) {
        QStringList values = rate.split(',');
        if (values.size() != 3)
            continue;
        Currency::addRate(values[0], values[1], values[2]);
    }
}
