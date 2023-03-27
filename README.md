# PassGenius
PassGenius is a command-line tool for generating and saving strong passwords. The program does not store passwords but generates them based on a master password and the service URL.


## Installation
Clone the repository to your local machine:

```shell
git clone https://github.com/TE1ch0st/passgenius.git
```
## Usage
PassGenius can be used for generating secure passwords and can also replace compromised passwords with new ones if necessary.

## Help Command
```shell
python3 PassGenius.py --help

List of Commands:
        -h --help : Display help message
        gen : Password generation tool
         rep (replace) : Password replacement tool

    -----------------------------
    gen (generate) [flags] - Password generation
         -d --Domain [url] : Service URL
         -s --Secret [password] : Master password for generation
         -l --Len [number] : Password length (Default: 25)

    -----------------------------
    rep (replace) [flag] - Password replacement
         -p --Password [you_password] : Password to be replaced

```

## License
Licensed under the Apache License, Version 2.0

---
Copyright © 2023 TE1ch0st. All rights reserved.