## New World Server Status Checker

A simple web scraper used to check if a New World server is full. Default server to check is Aaru. Automatically rechecks every 30-60 seconds depending on server status.

### Usage

CLI examples:
```
python status.py -s Isabella
```
```
python status.py -s "El Dorado"
```

In an active Python environment/instance:
```
import status
status.get_status()
```
This will check Aaru by default. To check another server, such as City of Brass:
```
status.get_status("City of Brass")
```
Note that the server name is case sensitive.