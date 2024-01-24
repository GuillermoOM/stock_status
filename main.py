import requests
import os
from bs4 import BeautifulSoup

api = os.getenv("MYNOTIFY_API_KEY")

if (api == None):
    raise Exception("API key env variable not found!")
else:
    url = "https://www.nflshop.com/pittsburgh-steelers/mens-pittsburgh-steelers-nike-white-game-custom-jersey/t-58603783+p-265660026024+z-8-1127655157"
    session = requests.Session()
    session.headers.update({
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'
    })
    response = session.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    print(f"Response OK?: {response.ok}")
    # print(response.status_code)
    # print(soup.prettify())
    print(f"Page Title: {soup.html.head.title.string}")

    result = ""
    notification_type = ""

    if (soup.html.head.title.string != "Access Denied" and response.ok):

        size_found = soup.find("a", attrs={"aria-label":"Size L "})

        if size_found:
            notification_type = "success"
            result = f"Size In Stock!"
            print(f"\n\033[92m{result}\033[0m")

        else:
            notification_type = "warning"
            result = f"Size NOT In Stock!"
            print(f"\n\033[31m{result}\033[0m")

    else:
        notification_type = "error"
        result = "Error: Access Denied!"
        print(f"\n\033[31m{result}\033[0m")

    requests.post('https://api.mynotifier.app',
                    {
                    "apiKey": api,
                    "message": result,
                    "description": "Steelers Jersey Status",
                    "type": notification_type,
                    })