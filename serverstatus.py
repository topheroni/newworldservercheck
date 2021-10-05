from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
import time

def get_status(server="Tumtum"):
    """Checks whether a server is full or not. Default server to check is Tumtum.
    A specific server can be set in the function argument."""
    full = True # keep checking until the server has space
    while full:
        url = "https://www.newworld.com/en-us/support/server-status"
        response = urllib.request.urlopen(url)
        webContent = response.read()
        try:
            print("Getting servers...")
            soup = BeautifulSoup(webContent, 'html.parser')
            print("Server status info obtained.")
        except:
            print("An error occurred. Trying again in 5 seconds")
            time.sleep(5)

        server_list = soup.find_all('div', class_='ags-ServerStatus-content-responses-response-server')
        server_names = soup.find_all('div', class_='ags-ServerStatus-content-responses-response-server-name')
        last_update = soup.find(class_='ags-ServerStatus-content-lastUpdated').text.strip()

        server_index = -1
        for i in range(len(server_list)):
            if server in server_names[i].text.strip():
                server_index = i

        if server_index == -1:
            message = server+f""" is not a valid server name.
            Please make sure the name matches exactly what is shown on the server list ({url})."""
            return message

        server_status_classes = server_list[server_index].div.div.get('class')
        if 'ags-ServerStatus-content-responses-response-server-status--full' in server_status_classes:
            print(server+" is FULL.")
            print(last_update)
            print("Checking again in 30 seconds.")
            print("—"*60)
            time.sleep(30)
        if 'ags-ServerStatus-content-responses-response-server-status--up' in server_status_classes:
            print(server+" is NOT full!")
            full = False
    return