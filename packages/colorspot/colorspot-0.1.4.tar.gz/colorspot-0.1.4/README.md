# ColorSpot

This script is a command line DX cluster client. It adds the following benefits to the default telnet stream:

  * displays the DX station's country
  * displays the DX station's continent
  * displays if the DX station uses LotW
  * downloads your LotW QSL file and marks all lines with countries that need to be confirmed (optional)
  * displays lines in different colors depending on the continent or band (user configurable)

# Screnshot

![screenshot](/screenshot.png?raw=true "screenshot")

# Limitations

The following limitations are present:

  * read-only: you can't send commands to the dx cluster server via this tool
  * no filters: you need to configure your filter on the server

# Installation

ColorSpot needs Python 3 and the following libraries:

 * colored
 * requests

Furthermore, you need an account at LotW for some of teh features.

Before installing ColorSpot, please make sure that pip, setuptools and wheel are installed and up-to-date:

```
# python3 -m pip install --upgrade pip setuptools wheel
```

Finally, install ColorSpot with pip:

```
# python3 -m pip install colorspot
```

# Updating

To update colorspot, execute the following command:

```
# python3 -m pip install --upgrade colorspot
```

# Usage

 * execute the application with "colorspot"
 * colorspot creates a default config file and states its location (e.g. _~/.colorspot.ini_)
 * adapt _~/.colorspot.ini_ to your needs. Important setting are:
    * cluster/host and cluster/port: Change this if you want to use another cluster server
    * cluster/user: Enter here your call sign
    * lotw/user: Enter here your lotw user name (your call sign). Leave at "N0CALL" to disable this feature.
    * lotw/password: Enter here your lotw password
    * lotw/mode: Enter here the mode you would like to filter the QSL download from LotW
 * execute the application again with "colorspot"

# License

see ![LICENSE](LICENSE)
