#-------------------------------------------------
#
# Project created by QtCreator 2014-02-18T18:53:02
#
#-------------------------------------------------

greaterThan(QT_MAJOR_VERSION, 4): cache()

QT       += core xml xmlpatterns

QT       -= gui

TARGET = international-trade
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app

CONFIG(debug, debug|release) {
    DESTDIR = build/debug
} else {
    DESTDIR = build/release
}

OBJECTS_DIR = $$DESTDIR/.obj
MOC_DIR = $$DESTDIR/.moc
RCC_DIR = $$DESTDIR/.qrc
UI_DIR = $$DESTDIR/.ui

SOURCES += main.cpp \
    currency.cpp \
    xmlratereader.cpp \
    xmldomratereader.cpp \
    transactions.cpp \
    xqueryratereader.cpp

HEADERS += \
    currency.h \
    xmlratereader.h \
    xmldomratereader.h \
    transactions.h \
    xqueryratereader.h
