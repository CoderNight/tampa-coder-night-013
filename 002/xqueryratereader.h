#ifndef XQUERYRATEREADER_H
#define XQUERYRATEREADER_H

#include <QFileInfo>

// Note: you can pass a filename (as a QString) to these methods

void readRatesUsingXQuery(const QFileInfo file);
void readRatesUsingXQuery_expanded(const QFileInfo file);

void readRatesUsingXQuery2(const QFileInfo file);

#endif // XQUERYRATEREADER_H
