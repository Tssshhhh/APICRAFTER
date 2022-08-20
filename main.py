from config import HOSTNAME, URL_PATH, FIRST_PAGE, LAST_PAGE, LIMIT_PER_KEY, MAX_PAGES
from dumps_reader import create_excel
from exceptions import *
import json
import requests
from requests.exceptions import ConnectTimeout
import time


def get_keys() -> list:
    api_keys_list = []
    with open('keys.txt', 'r') as f:
        keys = f.read()
    for _ in range(keys.count("\n")):
        key = keys.split("\n")[_]
        api_keys_list.append(key.replace('"', ''))
    return api_keys_list


def parse_api(keys_list: list, start: int, end: int, limit: int, max_pages: int) -> None:
    if (len(keys_list) * limit) < end:
        print(f"!!!\nWARNING, NOT ENOUGH KEYS ({len(keys_list)}) FOR PARSING {end} PAGES\n"
              f"YOUR NEED {end // limit + 1 - len(keys_list)} KEYS MORE\n"
              f"WOULD YOU LIKE TO CONTINUE AND GET ONLY {len(keys_list) * limit} PAGES? (y/n)")
        yn = input()
        if yn == "y":
            pass
        else:
            print('\nGET MORE KEYS BY USING get_api_keys.bat')
            return

    for APIKEY in keys_list:
        print('NEW KEY:', APIKEY)
        time.sleep(2)
        counter = 1
        dump_list = []
        try:
            for i in range(start, end):
                try:
                    if i > max_pages:
                        raise LASTPAGE
                    if counter % limit == 0:
                        raise LIMIT_PAGES
                    query = f'&max_results=20&page={i}'
                    result = requests.get(f"https://{HOSTNAME}/{URL_PATH}{APIKEY}{query}").json()['_items']
                    print(f'PAGE: {i}')
                    dump_list.extend(result)
                    counter += 1
                except LIMIT_PAGES:
                    print('GOT PAGES LIMIT')
                    with open(f'dumps/{APIKEY}_{start}_{end}.json', 'w', encoding='utf-8') as f:
                        json.dump(dump_list, f)
                    start = i
                    end += limit
                    break
                except KeyError:
                    print('MAX REQUEST FOR API KEY', APIKEY)
                    with open(f'dumps/{APIKEY}_{start}_{end}.json', 'w', encoding='utf-8') as f:
                        json.dump(dump_list, f)
                    start = i
                    end = i + limit
                    break
            else:
                print('RANGE ENDED')
                with open(f'dumps/{APIKEY}_{start}_{end}.json', 'w', encoding='utf-8') as f:
                    json.dump(dump_list, f)
                break
        except LASTPAGE:
            print('GOT LASTPAGE OF API')
            break
        except ConnectTimeout:
            print("CONNECT TIMEOUT")
            print(f"LAST SAVED PAGE: {end}")
            break

    create_excel()


if __name__ == "__main__":
    api_keys_list = get_keys()
    parse_api(api_keys_list, FIRST_PAGE, LAST_PAGE, LIMIT_PER_KEY, MAX_PAGES)

