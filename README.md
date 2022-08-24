# Brokerage Calculator

### Disclaimer
This script is intended for Samco Broker, if you're using a different broker your charges might be different. I named the variable pretty well, so you can tweak the numbers according to your usecase, or simply raise an issue, I might add it if I feel like it.

Basically wrote it for personal use, instead of checking there website after every trade. I decided to write a small python script to calculate.

### Usage
```bash
$ python3 calc.py -h
Usage: calc.py [-h] [-i [INTRADAY ...]] [-d [DELIVERY ...]] [-c [CASHPLUS ...]] [-o [OPTIONS...]]
   
    Samco Brokerage Calculator

    optional arguments:
    -h, --help            show this help message and exit
    -i [INTRADAY ...], --intraday [INTRADAY ...]
                          For equities intraday.
    -d [DELIVERY ...], --delivery [DELIVERY ...]
                          For equities delivery.
    -c [CASHPLUS ...], --cashplus [CASHPLUS ...]
                          For cashplus delivery.
    -o [OPTIONS ...], --options [OPTIONS ...]
                          For options intraday/delivery.
    -a [ADDORDER ...], --addorder [ADDORDER ...]
                        Add this order to journal.
```

For further usage help, you can execute the program with desired argument.

### Misc. Tip
You can add this file to your `.bashrc` or `.zshrc` if you're ZSH user, to use it as a command line tool, instead of navigating to that folder everytime.
```
alias calc="python3 [PATH_TO_CALC.PY]"
```
