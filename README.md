## New World Server Status Checker

A simple web scraper used to check if a New World server is full. Default argument is Tumtum. Automatically checks every 30 seconds so I don't upset Amazon, I guess, but I'm sure they can easily handle the traffic.

### Usage

In an active Python environment/instance:
```
import serverstatus
serverstatus.get_status()
```
This will check Tumtum by default. To check another server, such as City of Brass:
```
serverstatus.get_status("City of Brass")
```
Note that the checker is case sensitive.