import argparse
import time
import urllib.request

from bs4 import BeautifulSoup, element


def main(server: str = "Aaru"):
    full = True
    while full:
        url = "https://www.newworld.com/en-us/support/server-status"
        response = urllib.request.urlopen(url)
        webContent = response.read()
        try:
            print("Attempting to obtain server list.")
            soup = BeautifulSoup(webContent, "html.parser")
            print("Server list obtained.")
        except Exception as e:
            print("An error occurred parsing the webpage:")
            raise e
        server_list = soup.find_all(
            "div", class_="ags-ServerStatus-content-responses-response-server"
        )
        server_names = soup.find_all(
            "div", class_="ags-ServerStatus-content-responses-response-server-name"
        )
        last_update = soup.find(
            class_="ags-ServerStatus-content-lastUpdated"
        ).text.strip()
        server_index = -1
        nw_servers = [server.text.strip() for server in server_names]
        for i, _ in enumerate(server_list):
            if server in nw_servers:
                server_index = i
        server_info = server_list[server_index]
        server_statuses = get_status(server_info)
        if server_index == -1:
            message = (
                f"{server} is not a valid server name. "
                f"Please ensure the name matches *exactly* what is shown on the server list ({url})."
            )
            print(message)
            full = False
        if "Full" in server_statuses:
            print(
                f"{server} is full as of {last_update}.\n"
                "Automatically checking again in 30 seconds."
            )
            time.sleep(30)
        if "Online" in server_statuses:
            print(f"{server} has room!")
            full = False
        if "Maintenance" in server_statuses:
            print(
                f"{server} is under maintenance as of {last_update}.\n"
                "Automatically checking again in 60 seconds."
            )
            time.sleep(60)
        if "Character transfer is unavailable" in server_statuses:
            print("Character transfer is currently unavailable for this server.")
            full = False
        else:
            print(
                f"Unexpected response for server status(es): "
                + ", ".join(server_statuses)
            )
            full = False
        print("—" * 60)


def get_status(server_status):
    server_status_classes = []
    for tag in server_status:
        if isinstance(tag, element.Tag):
            titles = tag.find_all("div")
            for title in titles:
                status = title.get("title")
                if isinstance(status, list):
                    for s in status:
                        server_status_classes.append(s)
                else:
                    server_status_classes.append(title.get("title"))
    return server_status_classes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Retrieve the status of a New World Server."
    )
    parser.add_argument("-s", type=str, help="server name", metavar="server")
    args = parser.parse_args()
    main(args.s)
