# EDGAR CIK to TSV

This script parses fund holdings pulled from the SEC's EDGAR, given a ticker or CIK, and writes a .tsv file from them.
Because some funds have inconsistent tags on their 13F XML (e.g. Peak6 Investments LLC), the program will use the most
tags possible, and fill in missing tags with N/A for holdings which do not have the tag.

### Features

The script will take up to two command line arguments, the CIK and a filename (if desired). If the CIK is valid,
the program will write a new TSV .txt file in the local directory with the given filename. If no filename is provided,
the CIK will be the filename. Note the script overwrites any existing file in the directory with the same name.

Currently, only the most recent 13F is parsed. This can be modified by changing the generate_most_recent_13f function.
Future functionality can modify this to be easier to specify, possibly as a command line argument.

### Usage

To use, navigate to the directory where the script is located.

Then, run cikparser.py [CIK] [optional filename]:

```
cikparser.py 0001166559 Gates_Foundation
```

### Bugs

Most of the potential bugs are related to the requests library, and are handled by the try/except statements. The
exceptions are generalized - future versions of the script can give more specific error feedback.

The script is heavily tailored to the sec.gov/EDGAR webpage and format. Future changes to the website could potentially
break the functionality.

### Future improvements

XML files with inconsistent tags between holdings are handled as mentioned above. The current version of this script
assumes there is one holding with tags that encompass all others (the maximum). This is true for the 10 funds provided,
but may not be for all funds.

One possible way to handle differing formats is to put all tags into a Set, and use a Set that covers all possible tags.
Empty tags can be filled in with N/A, as the current script does. The current implementation is O(N^3), which may be able to
be improved.

Another way is to leave the formats as they come, and allow the user to interpret the data themselves. This would be less
error prone.

XML parsing is handled by the xml package, which is part of the Standard Library. lxml can be used if more speed is desired.

### Dependencies

-beautifulsoup4
-requests
