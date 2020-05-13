# EDGAR CIK to TSV

This script parses fund holdings pulled from the SEC's EDGAR, given a ticker or CIK, and writes a .tsv file from them. Because some funds have inconsistent tags on their 13F XML, the program will use the most tags possible, and fill in missing tags with N/A for holdings which do not have the tag. Note the script overwrites any existing file in the directory with the same name.

### Usage

To use, navigate to the directory where the script is located.

Then, run cikparser.py [CIK] [optional filename]:

```
python cikparser.py 0001166559 Gates_Foundation
```

### Dependencies

beautifulsoup4, requests
