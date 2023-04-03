# PassGenius
PassGenius is a command-line tool for generating and saving secure passwords. The program does not store passwords, but generates them based on the master password and the URL of the service.


## Installation
Clone the repository to your local machine:

```shell
git clone https://github.com/TE1ch0st/passgenius.git
```
## Usage
PassGenius can be used to generate secure passwords, and also allows you to replace compromised passwords with new ones, if necessary.

---

# CLI Version
## Help Command
```shell
python3 PassGenius.py --help

List of commands
     -h --help : Help Guide
     gen : Password Generation Tool
         rep (replace) : Password Replacement Tool

    -----------------------------
    gen (generate) [flags] - Password Generation
         -d --Domain [url] :  Website URL
         -s --Secret [password] : Master Password for Generation
         -l --Len [number] : Password length (Default: 25)

    -----------------------------
    rep (replace) [flag] - Password Replacement
         -p --Password [you_password] : Password to be replaced
```
---

# WEB Version
<div align="center">
    <img src="https://raw.githubusercontent.com/TE1ch0st/passgenius/main/assets/web.png" width="300">
</div>

---

# DESKTOP Version

<div align="center">
    <img src="https://raw.githubusercontent.com/TE1ch0st/passgenius/main/assets/win.png" width="300">
</div>

___

## License
Licensed under the Apache License, Version 2.0

---
Copyright © 2023 TE1ch0st. All rights reserved.