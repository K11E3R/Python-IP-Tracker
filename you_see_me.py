#!/usr/bin/env python3

"""
YouSeeMe - Python IP Tracker

Author: K11E3R (https://github.com/K11E3R)
Description: This script allows users to track IP information using various APIs.

"""
import asyncio
import importlib.util
import os
import subprocess
import sys

import aiohttp
import colorama

# Function to check and install required libraries if not present


def check_install_libraries(libraries):
    """
    Checks if required libraries are installed and installs them if missing.

    Args:
        libraries (list): List of library names to check.

    Returns:
        bool: True if all libraries are installed, False otherwise.
    """
    missing_libraries = []
    for lib in libraries:
        spec = importlib.util.find_spec(lib)
        if spec is None:
            missing_libraries.append(lib)
            print(f"{colorama.Fore.YELLOW}Library '{lib}' is not installed.")

    if missing_libraries:
        print(colorama.Fore.YELLOW + "Attempting to install missing libraries...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install"] + missing_libraries
            )
        except subprocess.CalledProcessError:
            print(
                colorama.Fore.RED
                + "Failed to install missing libraries. Please install manually."
            )
            return False
    return True


# Check and install required libraries
required_libraries = ["aiohttp", "colorama"]
if not check_install_libraries(required_libraries):
    sys.exit(1)

# List of API URLs to test and use
API_URLS = [
    "https://api.ipdata.co/",
    "https://ipinfo.io/",
    "https://ipapi.co/",
    "https://freegeoip.app/json/",
    "https://api.ipgeolocation.io/ipgeo",
    "https://extreme-ip-lookup.com/json/",
    "https://ipwhois.app/json/",
]


def clear_screen():
    """Function to clear the screen based on OS type."""
    os.system("cls" if os.name == "nt" else "clear")


async def check_api_access(session, url):
    """Async function to check if the API URL is accessible.

    Args:
        session (aiohttp.ClientSession): The HTTP client session.
        url (str): The API URL to check.

    Returns:
        bool: True if the API URL is accessible, False otherwise.
    """
    try:
        async with session.get(url, timeout=10) as response:
            return response.status == 200
    except aiohttp.ClientError:
        return False
    except asyncio.TimeoutError:
        return False


MAX_RETRY_ATTEMPTS = 3


async def fetch_ip_data(session, url, ip):
    """Async function to fetch IP data from API.

    Args:
        session (aiohttp.ClientSession): The HTTP client session.
        url (str): The API URL to fetch data from.
        ip (str): The IP address to fetch data for.

    Returns:
        dict: The IP data if fetched successfully, None otherwise.
    """
    retry_count = 0
    while retry_count < MAX_RETRY_ATTEMPTS:
        try:
            async with session.get(f"{url}{ip}", timeout=10) as response:
                if response.status == 200:
                    return await response.json()
                print(
                    colorama.Fore.YELLOW
                    + f"Failed to fetch data from {url}. Retrying..."
                )
        except aiohttp.ClientError:
            print(colorama.Fore.YELLOW + f"Failed to connect to {url}. Retrying...")
        except asyncio.TimeoutError:
            print(
                colorama.Fore.YELLOW
                + f"Timeout occurred while connecting to {url}. Retrying..."
            )

        retry_count += 1

    return None


def print_ip_data(values):
    """Function to print IP data.

    Args:
        values (dict): The IP data to print.
    """
    if values:
        print("------------------------------------")
        print(f" {colorama.Fore.GREEN}IP           :  {values.get('ip')}")
        print(f" {colorama.Fore.GREEN}City         :  {values.get('city')}")
        print(f" {colorama.Fore.GREEN}Region       :  {values.get('region')}")
        print(f" {colorama.Fore.GREEN}Country      :  {values.get('country_name')}")
        print(f" {colorama.Fore.GREEN}Continent    :  {values.get('continent_name')}")
        print(f" {colorama.Fore.GREEN}Time Zone    :  {values.get('time_zone')}")
        print(f" {colorama.Fore.GREEN}Currency     :  {values.get('currency')}")
        print(f" {colorama.Fore.GREEN}Calling Code :  +{values.get('calling_code')}")
        print(f" {colorama.Fore.GREEN}Organisation :  {values.get('organisation')}")
        print(f" {colorama.Fore.GREEN}ASN          :  {values.get('asn')}")
        print("------------------------------------")
    else:
        print(colorama.Fore.RED + "No data found for the provided IP.")


async def test_api_urls():
    """Async function to test API URLs for accessibility.

    Returns:
        list: List of accessible API URLs.
    """
    async with aiohttp.ClientSession() as session:
        accessible_urls = []
        for url in API_URLS:
            access_allowed = await check_api_access(session, url)
            if access_allowed:
                accessible_urls.append(url)
                print(colorama.Fore.GREEN + f"API URL {url} is accessible.")
            else:
                print(
                    colorama.Fore.YELLOW
                    + f"API URL {url} is not accessible or requires authorization."
                )

        return accessible_urls


async def main():
    """Main asynchronous function to run the program."""
    clear_screen()
    colorama.init(autoreset=True)
    print(
        colorama.Fore.RED
        + """
▓██   ██▓ ▒█████   █    ██   ██████ ▓█████ ▓█████  ███▄ ▄███▓▓█████
 ▒██  ██▒▒██▒  ██▒ ██  ▓██▒▒██    ▒ ▓█   ▀ ▓█   ▀ ▓██▒▀█▀ ██▒▓█   ▀
  ▒██ ██░▒██░  ██▒▓██  ▒██░░ ▓██▄   ▒███   ▒███   ▓██    ▓██░▒███
  ░ ▐██▓░▒██   ██░▓▓█  ░██░  ▒   ██▒▒▓█  ▄ ▒▓█  ▄ ▒██    ▒██ ▒▓█  ▄
  ░ ██▒▓░░ ████▓▒░▒▒█████▓ ▒██████▒▒░▒████▒░▒████▒▒██▒   ░██▒░▒████▒
   ██▒▒▒ ░ ▒░▒░▒░ ░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░░░ ▒░ ░░░ ▒░ ░░ ▒░   ░  ░░░ ▒░ ░
 ▓██ ░▒░   ░ ▒ ▒░ ░░▒░ ░ ░ ░ ░▒  ░ ░ ░ ░  ░ ░ ░  ░░  ░      ░ ░ ░  ░
 ▒ ▒ ░░  ░ ░ ░ ▒   ░░░ ░ ░ ░  ░  ░     ░      ░   ░      ░      ░
 ░ ░         ░ ░     ░           ░     ░  ░   ░  ░       ░      ░  ░
 ░ ░

                    Python IP Tracker - K11E3R
    """
    )

    # Test API URLs for accessibility
    accessible_urls = await test_api_urls()
    if not accessible_urls:
        print(colorama.Fore.RED + "No accessible API URLs found. Exiting.")
        return

    async with aiohttp.ClientSession() as session:
        while True:
            ip = input("Enter target IP address (or 'exit' to quit): ").strip()
            if ip.lower() == "exit":
                break

            if not ip:
                print(colorama.Fore.RED + "Please enter a valid IP address.")
                continue

            # Fetch IP data from accessible URLs
            ip_data = None
            for url in accessible_urls:
                ip_data = await fetch_ip_data(session, url, ip)
                if ip_data:
                    break

            print_ip_data(ip_data)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(colorama.Fore.RED + "\nProgram terminated by user.")
