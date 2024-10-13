
import shutil
from colorama import *
from datetime import datetime, time
from fake_useragent import FakeUserAgent
from time import sleep
import json
import os
import pytz
import random
import requests
import sys

from tzlocal import get_localzone


class Tomarket:
    def __init__(self) -> None:
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'api-web.tomarket.ai',
            'Origin': 'https://mini-app.tomarket.ai',
            'Referer': 'https://mini-app.tomarket.ai/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': FakeUserAgent().random
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_timestamp(self, message, timezone=''):
        if timezone == '':
            local_tz = get_localzone()
        else:
            local_tz = pytz.timezone(timezone)

        now = datetime.now(local_tz)
        timestamp = now.strftime(f'%X')

        print(
            f"{Fore.BLUE + Style.BRIGHT}[ {timestamp} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{message}",
            flush=True
        )

    def daily_claim(self, token: str):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/daily/claim'
        data = json.dumps({'game_id': 'fa873d13-d831-4d6f-8aee-9cff7a1d0db1'})
        self.headers.update({
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        })
        response = requests.post(url=url, headers=self.headers, data=data)
        response.raise_for_status()
        daily_claim = response.json()
        if 'status' in daily_claim:
            if daily_claim['status'] in [0, 200]:
                self.print_timestamp(
                    f"{Fore.GREEN + Style.BRIGHT}[ Daily Claimed ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}[ Points {daily_claim['data']['today_points']} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.BLUE + Style.BRIGHT}[ Day {daily_claim['data']['today_game']} ]{Style.RESET_ALL}"
                )
            elif daily_claim['status'] == 400 or daily_claim['message'] == 'already_check':
                self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Already Check Daily Claim ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error Daily Claim ]{Style.RESET_ALL}")
        elif 'code' in daily_claim:
            if daily_claim['code'] == 400 or daily_claim['message'] == 'claim throttle':
                self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Daily Claim Throttle ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error Daily Claim ]{Style.RESET_ALL}")
        else:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error Daily Claim ]{Style.RESET_ALL}")

    def check_free_spins(self,token, query: str):
        url="https://api-web.tomarket.ai/tomarket-game/v1/user/tickets"

        data = json.dumps({'init_data': query, 'language_code': 'en'})

        self.headers.update({
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        })
        response = requests.post(url=url, data=data , headers=self.headers)
        response.raise_for_status()
        result = response.json()
        if(result['status'] == 0):
            if(result['data']['ticket_spin_1'] > 0):
                spins = result['data']['ticket_spin_1']
                self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ {spins} Spins Available ]{Style.RESET_ALL}")

                for i in range(spins):
                    self.print_timestamp(f"{Fore.BLUE + Style.BRIGHT}[ Claiming Spin {i+1} ]{Style.RESET_ALL}")
                    self.use_free_spins(token=token)
                    sleep(2)

                self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Claimed {spins} Spins ]{Style.RESET_ALL}")

            else:
                self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ No Free Spins Available ]{Style.RESET_ALL}")
        else:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error Check Free Spins ]{Style.RESET_ALL}")

    def use_free_spins(self, token: str):
        url="https://api-web.tomarket.ai/tomarket-game/v1/spin/raffle"

        data = json.dumps({'category': 'ticket_spin_1'})

        self.headers.update({
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        })
        response = requests.post(url=url, data=data , headers=self.headers)
        response.raise_for_status()
        result = response.json()
        if(result['status'] == 0):
            spin_result = result['data']['results'][0]
            self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Successfully Recieved {spin_result['type']} | Amount {spin_result['amount']} 🎉 ]{Style.RESET_ALL}")
        else:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error Use Free Spins: {result['message']} ]{Style.RESET_ALL}")
    
    def rank_data(self, token: str):
        url="https://api-web.tomarket.ai/tomarket-game/v1/rank/data"
        self.headers.update({
            'Authorization': token
            , 'Content-Length': '0'
        })
        response = requests.post(url=url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    

    def rank_upgrade(self, token: str, stars: int):
        url="https://api-web.tomarket.ai/tomarket-game/v1/rank/upgrade"


        data = json.dumps({
            'stars': stars
        })

        self.headers.update({
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        })
        response = requests.post(url=url, data=data , headers=self.headers)
        response.raise_for_status()
        return response.json()


    def user_balance(self, token: str):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/user/balance'
        self.headers.update({
            'Authorization': token,
            'Content-Length': '0'
        })
        response = requests.post(url=url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def farm_start(self, token: str):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/farm/start'
        data = json.dumps({'game_id': '53b22103-c7ff-413d-bc63-20f6fb806a07'})
        self.headers.update({
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        })
        response = requests.post(url=url, headers=self.headers, data=data)
        response.raise_for_status()
        farm_start = response.json()
        if 'status' in farm_start:
            if farm_start['status'] == 0:
                self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Farm Started ]{Style.RESET_ALL}")
                farm_end_at = datetime.fromtimestamp(farm_start['data']['end_at'])
                timestamp_farm_end_at = farm_end_at.strftime('%X %Z')
                self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Farm Can Claim At {timestamp_farm_end_at} ]{Style.RESET_ALL}")
            elif farm_start['status'] == 500 or farm_start['message'] == 'game already started':
                self.print_timestamp(f"{Fore.MAGENTA + Style.BRIGHT}[ Farm Already Started ]{Style.RESET_ALL}")
                farm_end_at = datetime.fromtimestamp(farm_start['data']['end_at'], pytz.timezone('Asia/Jakarta'))
                timestamp_farm_end_at = farm_end_at.strftime('%X %Z')
                self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Farm Can Claim At {timestamp_farm_end_at} ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error Farm Start ]{Style.RESET_ALL}")
        else:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error Farm Start ]{Style.RESET_ALL}")

    def farm_claim(self, token: str):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/farm/claim'
        data = json.dumps({'game_id': '53b22103-c7ff-413d-bc63-20f6fb806a07'})
        self.headers.update({
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        })
        response = requests.post(url=url, headers=self.headers, data=data)
        response.raise_for_status()
        farm_claim = response.json()
        if 'status' in farm_claim:
            if farm_claim['status'] == 0:
                self.print_timestamp(
                    f"{Fore.GREEN + Style.BRIGHT}[ Farm Claimed {farm_claim['data']['points']} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.BLUE + Style.BRIGHT}[ Starting Farm ]{Style.RESET_ALL}"
                )
                self.farm_start(token=token)
            elif farm_claim['status'] == 500 or farm_claim['message'] == 'farm not started or claimed':
                self.print_timestamp(f"{Fore.MAGENTA + Style.BRIGHT}[ Farm Not Started ]{Style.RESET_ALL}")
                self.farm_start(token=token)
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error Farm Claim ]{Style.RESET_ALL}")
        elif 'code' in farm_claim:
            if farm_claim['code'] == 400 or farm_claim['message'] == 'claim throttle':
                self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Farm Claim Throttle ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error Farm Claim ]{Style.RESET_ALL}")
        else:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error Farm Claim ]{Style.RESET_ALL}")

    def game_play(self, token: str):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/game/play'
        data = json.dumps({'game_id': '59bcd12e-04e2-404c-a172-311a0084587d'})
        self.headers.update({
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        })
        response = requests.post(url=url, headers=self.headers, data=data)
        response.raise_for_status()
        game_play = response.json()
        if 'status' in game_play:
            if game_play['status'] == 0:
                self.print_timestamp(
                    f"{Fore.GREEN + Style.BRIGHT}[ Game Started ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.BLUE + Style.BRIGHT}[ Please Wait 30 Seconds ]{Style.RESET_ALL}"
                )
                sleep(33)
                self.game_claim(token=token, points=random.randint(6000, 6001))
            elif game_play['status'] == 500 or game_play['message'] == 'no chance':
                self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ No Chance To Start Game ]{Style.RESET_ALL}")
        else:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error Game Play ]{Style.RESET_ALL}")

    def game_claim(self, token: str, points: int):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/game/claim'
        data = json.dumps({
            'game_id': '59bcd12e-04e2-404c-a172-311a0084587d',
            'points': points
        })
        self.headers.update({
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        })
        response = requests.post(url=url, headers=self.headers, data=data)
        response.raise_for_status()
        game_claim = response.json()
        if 'status' in game_claim:
            if game_claim['status'] == 0:
                self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Game Claimed {game_claim['data']['points']} ]{Style.RESET_ALL}")
            elif game_claim['status'] == 500 or game_claim['message'] == 'game not start':
                self.print_timestamp(f"{Fore.MAGENTA + Style.BRIGHT}[ Game Not Started ]{Style.RESET_ALL}")
                self.game_play(token=token)
        elif 'code' in game_claim:
            if game_claim['code'] == 400 or game_claim['message'] == 'claim throttle':
                self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Farm Claim Throttle ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error Game Claim ]{Style.RESET_ALL}")
        else:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error Game Claim ]{Style.RESET_ALL}")

    def tasks_list(self, token: str):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/tasks/list'
        data = json.dumps({'language_code': 'en'})
        self.headers.update({
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        })
        response = requests.post(url=url, headers=self.headers, data=data)
        response.raise_for_status()
        
        tasks_list = response.json()

        if 'data' in tasks_list and isinstance(tasks_list['data'], dict):
            for category, tasks in tasks_list['data'].items():
                if category == '3rd':
                    if isinstance(tasks, dict):
                        for task_id, tp_tasks_list in tasks.items():
                            for task in tp_tasks_list:
                                if isinstance(task, dict) and 'endTime' in task and task['endTime']:
                                    end_time = datetime.strptime(task['endTime'], '%Y-%m-%d %H:%M:%S')
                                    if end_time < datetime.now():
                                        continue
                                if task['status'] == 0 and task['type'] == "mysterious":
                                    self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Claiming '{task['title']}' ]{Style.RESET_ALL}")
                                    self.tasks_claim(token=token, task_id=task['taskId'])
                                elif task['status'] == 0:  # Ensure this checks all types
                                    self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Starting '{task['title']}' ]{Style.RESET_ALL}")
                                    start_task = self.tasks_start(token=token, task_id=task['taskId'])
                                    if start_task['status'] == 0:
                                        if start_task['data']['status'] == 1:
                                            self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Checking '{task['title']}' ]{Style.RESET_ALL}")
                                            sleep(task['waitSecond'] + 3)
                                            self.tasks_check(token=token, task_id=task['taskId'])
                                        elif start_task['data']['status'] == 2:
                                            self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Claiming '{task['title']}' ]{Style.RESET_ALL}")
                                            self.tasks_check(token=token, task_id=task['taskId'])
                                    elif start_task['status'] == 500 and start_task['message'] == 'Handle user\'s task error':
                                        self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Finish This Task By Itself ]{Style.RESET_ALL}")
                                    else:
                                        self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error Tasks Start ]{Style.RESET_ALL}")
                                elif task['status'] == 1:
                                    self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ You Haven't Finish Or Start '{task['title']}' ]{Style.RESET_ALL}")
                                    self.tasks_check(token=token, task_id=task['taskId'])
                                elif task['status'] == 2:
                                    self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Claiming '{task['title']}' ]{Style.RESET_ALL}")
                                    self.tasks_check(token=token, task_id=task['taskId'])

                if isinstance(tasks, list):
                    for task in tasks:
                        if isinstance(task, dict) and 'endTime' in task and task['endTime']:
                            end_time = datetime.strptime(task['endTime'], '%Y-%m-%d %H:%M:%S')
                            if end_time < datetime.now():
                                continue
                        if task['status'] == 0 and task['type'] == "mysterious":
                            self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Claiming '{task['title']}' ]{Style.RESET_ALL}")
                            self.tasks_claim(token=token, task_id=task['taskId'])
                        elif task['status'] == 0:  # Ensure this checks all types
                            self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Starting '{task['title']}' ]{Style.RESET_ALL}")
                            start_task = self.tasks_start(token=token, task_id=task['taskId'])
                            if start_task['status'] == 0:
                                if start_task['data']['status'] == 1:
                                    self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Checking '{task['title']}' ]{Style.RESET_ALL}")
                                    sleep(task['waitSecond'] + 3)
                                    self.tasks_check(token=token, task_id=task['taskId'])
                                elif start_task['data']['status'] == 2:
                                    self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Claiming '{task['title']}' ]{Style.RESET_ALL}")
                                    self.tasks_check(token=token, task_id=task['taskId'])
                            elif start_task['status'] == 500 and start_task['message'] == 'Handle user\'s task error':
                                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Finish This Task By Itself ]{Style.RESET_ALL}")
                            else:
                                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error Tasks Start ]{Style.RESET_ALL}")
                        elif task['status'] == 1:
                            self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ You Haven't Finish Or Start '{task['title']}' ]{Style.RESET_ALL}")
                            self.tasks_check(token=token, task_id=task['taskId'])
                        elif task['status'] == 2:
                            self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Claiming '{task['title']}' ]{Style.RESET_ALL}")
                            self.tasks_check(token=token, task_id=task['taskId'])
        else:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error: 'data' not found or is not a dictionary ]{Style.RESET_ALL}")




    def tasks_start(self, token: str, task_id: int):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/tasks/start'
        data = json.dumps({'task_id': task_id})
        self.headers.update({
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        })
        response = requests.post(url=url, headers=self.headers, data=data)
        response.raise_for_status()
        return response.json()

    def tasks_check(self, token: str, task_id: int):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/tasks/check'
        data = json.dumps({'task_id': task_id})
        self.headers.update({
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        })
        response = requests.post(url=url, headers=self.headers, data=data)
        response.raise_for_status()
        tasks_check = response.json()
        if 'status' in tasks_check:
            if 'status' in tasks_check['data']:
                if tasks_check['data']['status'] == 0:
                    self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Starting Task ]{Style.RESET_ALL}")
                    self.tasks_start(token=token, task_id=task_id)
                elif tasks_check['data']['status'] == 1:
                    self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ This Task Still Haven't Finished ]{Style.RESET_ALL}")
                elif tasks_check['data']['status'] == 2:
                    self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Claiming Task ]{Style.RESET_ALL}")
                    self.tasks_claim(token=token, task_id=task_id)
                elif tasks_check['data']['status'] == 3:
                    self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ This Task Already Claimed ]{Style.RESET_ALL}")
                else:
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error Tasks Check ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error Tasks Check ]{Style.RESET_ALL}")
        else:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error Tasks Check ]{Style.RESET_ALL}")

    def tasks_claim(self, token: str, task_id: int):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/tasks/claim'
        data = json.dumps({'task_id': task_id})
        self.headers.update({
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        })
        response = requests.post(url=url, headers=self.headers, data=data)
        response.raise_for_status()
        tasks_claim = response.json()
        if 'status' in tasks_claim:
            if tasks_claim['status'] == 0:
                self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Claimed ]{Style.RESET_ALL}")
            elif tasks_claim['status'] == 500 and tasks_claim['message'] == 'You haven\'t start this task':
                self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ You Haven't Start This Task ]{Style.RESET_ALL}")
                self.tasks_start(token=token, task_id=task_id)
            elif tasks_claim['status'] == 500 and tasks_claim['message'] == 'You haven\'t finished this task':
                self.tasks_check(token=token, task_id=task_id)
            elif tasks_claim['status'] == 500 and tasks_claim['message'] == 'Task is not within the valid time':
                self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ You Haven't Finished This Task ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error Tasks Claim ]{Style.RESET_ALL}")
        else:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error Tasks Claim ]{Style.RESET_ALL}")

    def set_queries(self):
        try:
            with open('query.txt', 'r', encoding='utf-8') as file:
                queries = file.readlines()

            if len(queries) == 0:
                print("\n")
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ No queries found in query.txt! ]{Style.RESET_ALL}")
                
                if os.path.exists('data.json'):
                    try:
                        with open('data.json', 'r', encoding='utf-8') as data_file:
                            accounts = json.load(data_file)
                            
                        if len(accounts) == 0:
                            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ No accounts found in data.json. Exiting... ]{Style.RESET_ALL}")
                            print("\n")
                            self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Please Edit query.txt file ]{Style.RESET_ALL}")
                            print("\n")
                            exit(0)
                        else:
                            print("\n")
                            self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Found {len(accounts)} accounts in data.json. Continuing... ]{Style.RESET_ALL}")
                    except json.JSONDecodeError as e:
                        self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error decoding JSON. Exiting... ]{Style.RESET_ALL}")
                        exit(1)
                else:
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ data.json does not exist. Exiting... ]{Style.RESET_ALL}")
                    exit(0) 

            else:
                print("\n\n")
                self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Found {len(queries)} queries ]{Style.RESET_ALL}")


            if os.path.exists('data.json'):
                try:
                    with open('data.json', 'r', encoding='utf-8') as data_file:
                        accounts = json.load(data_file) 

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    accounts = []
            else:
                accounts = []

            for index, query in enumerate(queries):
                query = query.strip()

                invite_codes = [
                    "0000u8O2",
                    "0000u6qY",
                ]
                
                selected_invite_code = random.choice(invite_codes)

                payload = {
                    "init_data": query,
                    "invite_code": selected_invite_code,
                    "from": "",
                    "is_bot": False
                }

                url = 'https://api-web.tomarket.ai/tomarket-game/v1/user/login'
                self.headers.update({'Content-Type': 'application/json'})

                try:
                    response = requests.post(url=url, headers=self.headers, json=payload)
                    
                    response.raise_for_status()
                    data = response.json()
                    
                    token = data['data']['access_token']
                    name = data['data']['fn'] + ' ' + data['data']['ln']

                    self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Found an account : {name} ]{Style.RESET_ALL}")

                    if any(account['name'] == name for account in accounts):
                        print("\n")
                        self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Account '{name}' already exists ]{Style.RESET_ALL}")
                        for account in accounts:
                            if account['name'] == name:
                                if account['token'] != token:
                                    accounts[accounts.index(account)] = {
                                        'name': account['name'],
                                        'token': token,
                                        'query': account['query']
                                    }
                                    with open('data.json', 'w', encoding='utf-8') as data_file:
                                        json.dump(accounts, data_file, indent=4)
                                    self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Updated Account Token ]{Style.RESET_ALL}")
                                    print("\n")
                        continue

                    accounts.append({
                        'name': name,
                        'token': token,
                        'query': query
                    })
                except Exception as e:
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error processing account for query '{index + 1}' line ]{Style.RESET_ALL}")
                    exit(1)


            with open('data.json', 'w', encoding='utf-8') as data_file:
                json.dump(accounts, data_file, indent=4)

        except Exception as e:
            print(f"An error occurred: {e}")


    def main(self):
        self.welcome_msg()
        self.set_queries()
        try:
            accounts = json.load(open('data.json', 'r', encoding='utf-8'))

            for account in accounts:
                self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ '{account['name']}' account detected from data.json ]{Style.RESET_ALL}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading accounts: {e}")
            return

        for account in accounts:
            print("\n")
            self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Using '{account['name']}' account ]{Style.RESET_ALL}\n")

            # Daily claim
            self.daily_claim(token=account['token'])

            # User balance info
            balance = self.user_balance(token=account['token'])
            self.print_timestamp(
                f"{Fore.CYAN + Style.BRIGHT}[ Balance - {balance['data']['available_balance']} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.CYAN + Style.BRIGHT}[ Play Passes - {balance['data']['play_passes']} ]{Style.RESET_ALL}"
            )

            rank_info = self.rank_data(token=account['token'])

            current_rank = rank_info['data']['currentRank']
            
            self.print_timestamp(
                f"{Fore.CYAN + Style.BRIGHT}[ Current Rank - {current_rank['name']} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.CYAN + Style.BRIGHT}[ Level - {current_rank['level']} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.CYAN + Style.BRIGHT}[ Unused Stars - {rank_info['data']['unusedStars']} ]{Style.RESET_ALL}"
            )

            # Check free spins
            self.check_free_spins(token=account['token'], query=account['query'])

            # Farming tasks
            local_tz = get_localzone()

            if 'farming' in balance['data']:
                now = datetime.now(local_tz)
                farm_end_at = datetime.fromtimestamp(balance['data']['farming']['end_at'], local_tz)

                if now >= farm_end_at:
                    self.farm_claim(token=account['token'])
                else:
                    
                    timestamp_farm_end_at = farm_end_at.strftime('%X %Z')
                    self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Farm Can Claim At {timestamp_farm_end_at} ]{Style.RESET_ALL}")
            else:
                 self.farm_start(token=account['token'])

            # Playing passes
            while balance['data']['play_passes'] > 0:
                self.game_play(token=account['token'])
                balance['data']['play_passes'] -= 1

            # Tasks
            self.tasks_list(token=account['token'])

            
            rank_updated_info = self.rank_data(token=account['token'])
            unused_stars = rank_updated_info['data']['unusedStars']

            if unused_stars > 0:
                self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Upgrading Rank... ]{Style.RESET_ALL}")
                upgrade_level = self.rank_upgrade(token=account['token'], stars=unused_stars)

                if upgrade_level['status'] == 0:
                    self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Rank Upgraded by {unused_stars} Stars ]{Style.RESET_ALL}")

            else:
                self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Not Enough Stars to Upgrade Rank ]{Style.RESET_ALL}")

        print("\n")
        # Final message before restart
        self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Process Complete ]{Style.RESET_ALL}")
        self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ You claimed everything. You can Stop the bot now ]{Style.RESET_ALL}")
        self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Restarting in 3 Hours ]{Style.RESET_ALL}")

        # Sleep and restart the process after a delay
        sleep((3 * 3600) + 10)
        self.clear_terminal()
    
    def welcome_msg(self):
        columns, _ = shutil.get_terminal_size()

        text = """
 ____  _____  __  __    __    ____  _  _  ____  ____ 
(_  _)(  _  )(  \/  )  /__\  (  _ \( )/ )( ___)(_  _)
  )(   )(_)(  )    (  /(__)\  )   / )  (  )__)   )(  
 (__) (_____)(_/\/\_)(__)(__)(_)\_)(_)\_)(____) (__)                                      
        """

        for line in text.splitlines():
            print(f"{Fore.CYAN + Style.BRIGHT} {line[:columns]}")
        sleep(2)
        print(f"{Fore.CYAN + Style.BRIGHT}[ Created by {Fore.MAGENTA + Style.BRIGHT}DaΣmøn (@NotMrStrange on TG) {Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}")
        print(f"{Fore.CYAN + Style.BRIGHT}[ Telegram Group : {Fore.MAGENTA + Style.BRIGHT}https://t.me/yk_daemon {Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}")
        print(f"{Fore.CYAN + Style.BRIGHT}[ Youtube : {Fore.MAGENTA + Style.BRIGHT}https://youtube.com/@yk-daemon {Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}")
        print(f"{Fore.CYAN + Style.BRIGHT}[ YesCoin Script : {Fore.MAGENTA + Style.BRIGHT}https://youtu.be/G_0KPU2p8ow {Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}")
        print(f"{Fore.CYAN + Style.BRIGHT}[ Script updated on : {Fore.MAGENTA + Style.BRIGHT}13 October 2024 {Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}")

        sleep(2)

if __name__ == '__main__':
    while True:
        try:
            init(autoreset=True)
            tomarket = Tomarket()
            tomarket.main()
        except KeyboardInterrupt:
            tomarket.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ See You 👋🏻 ]{Style.RESET_ALL}")
            sys.exit(0)
        except (Exception, requests.ConnectionError, requests.JSONDecodeError) as e:
            tomarket.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
            tomarket.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Please Retry After Some Time ]{Style.RESET_ALL}")
            exit(1)

