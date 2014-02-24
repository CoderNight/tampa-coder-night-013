doc('doc/RATES.xml')//rate/concat(string-join(*[self::from or self::to or self::conversion]/string(), ','), '\n')

