
## Instructions for running mah code:

$ go run readfile.go RATES.xml TRANS.csv

The printout will be the number of rates that successfully parsed, the number of transactions successfully parsed, and the sum of the sales.


## Notes about this attempt

I went into this with the intent of getting better at thinking about interfaces and less coupling between go types.

This project does not successfully perform its task because it can't find conversions, however it parses all fields successfully.

The Parsing is probably the bigger accomplishment, even if the interfaces aren't that grand.

I might just have time to do a lua implementation before the meetup, and maybe Gavin will be a buddy ol' pal to me.
