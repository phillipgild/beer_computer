# Øl Computeren

A simple Python application to scan users and items.

## Requirements

- Python 3.x installed

---

## Installation & Setup

To clone the repository, open the terminal and run:

```bash
git clone https://github.com/phillipgild/beer_computer.git
cd beer_computer
```

## Mac OS and Linux Setup

To install the required packages for Mac OS/Linux, run the following command in the repository folder

```bash
python -m pip install -r requirements.txt
```

## Windows Setup

## Create scripts to run the programs

1. **Go to the folder 'run_setup'**
2. **On Mac-OS,  double-click run_setup_mac.command  \
     On Windows, double-click run_setup_windows.bat  \
     On Linux,   double-click run_setup_linux.sh**
3. **On Mac-OS,  go to 'mac_scripts'     and run the desired program(s)  \
     On Windows, go to 'windows_scripts' and run the desired program(s)  \
     On Linux,   go to 'linux_scripts'   and run the desired program(s)**


# How to use

## Modify users and actions

To use this series of scripts, one should modify two files:

the file; users_and_items/users.csv; should be modified with the desired names of the users. The keys do not need to be touched, but they can be.

the file; users_and_items/items.csv; should be modified with the desired names of the items. The keys do not need to be touched, but they can be.
The price and amount is only important for post-processing and does not need to be considered before generating codes and using the scanner.

## Run the desired programs to generate qr codes or barcodes and the scanner

IMPORTANT; Once qr codes or barcodes are generated. One should NOT modify:
users or keys in users_and_items/users.csv
items or keys in users_and_items/items.csv
You should not have any duplicate user or item names or duplicate keys !!!

Now the user can generate qr codes or barcodes and gather them in for example a word document and print them. They can be directly scanned by a scanner.

## Post-processing

If post-processing is desired, one should modify one file:
In users_and_items/items.csv;
one should modify the price to be the amount the item costs (not considering losses, i.e. missing items)
Also the amount should be modified to the total amount of items gone (So bought_amount - returned_amount)


# Functionalities

## scanner

The scanner application is the main program for the qr code / barcode scanner.

Upon startup, it will read all .csv files in the 'exports' folder and preload the leaderboard to this state.
It will do so based on the users and actions found in the 'users_and_items/users.csv' and 'users_and_items/items.csv'
Also a set of hardcoded actions exist in the 'users_and_items/no_touch/ardcoded_actions.csv' file. This is used in the scanner and elsewhere.
This should not be modified on use. If additional actions are required, they should be added to the repository.

Whenever .csv files are exported, they will be written to the 'exports' folder with a unique name to avoid overrides.
.csv files are only exported if the state of users_actions has changed since last export to avoid duplicate actions.

If the scanner program is shut down, it will export a .csv file before it exits to avoid data loss.

The leaderboard is updated whenever an action is performed and is ordered from top to bottom in terms of the total amount of actions.
Currently each action weights the same. This can be changed if desired. e.g. if sodas are supposed to not count in the total.

## generate_barcodes and generate_qr_codes

The qr code / barcode generators both read from the users and actions found in the 'users_and_items/users.csv' and 'users_and_items/items.csv'.
Also a set of hardcoded actions exist in the 'users_and_items/no_touch/ardcoded_actions.csv' file. This is used in the scanner and elsewhere.
This should not be modified on use. If additional actions are required, they should be added to the repository.

qr codes are written to the 'qr_codes' folder with their unique names as .png files
barcodes are written to the 'barcodes' folder with their unique names as .png files

## find_prices_divide_losses_equally

This script performs post-processing of all scanned actions for all users who have scanned a non-zero amount of items.
it reads from users and actions found in the 'users_and_items/users.csv' and 'users_and_items/items.csv'.

It will find the amount all the users has scanned for and the total price of "missing" items.
i.e. non-scanned items that is declared missing in 'users_and_items/items.csv'.

The script will divide the price of "missing" items evenly across all users who has a non-zero total amount of scans.

The result is written to 'prices/user_costs.csv' where the price can be seen easily for all users that are supposed to pay.
