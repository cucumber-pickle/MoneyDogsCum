import requests
import json
import os
from colorama import *
from datetime import datetime, timedelta, timezone
from core.helper import get_headers, countdown_timer, extract_user_data, config
import random
import time
from platform import system as s_name
from os import system as sys

class MoneyDOGS:
    def __init__(self):
        self.headers = None
        self.session = requests.Session()

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        banner = f"""{Fore.GREEN}
         ██████  ██    ██   ██████  ██    ██  ███    ███  ██████   ███████  ██████  
        ██       ██    ██  ██       ██    ██  ████  ████  ██   ██  ██       ██   ██ 
        ██       ██    ██  ██       ██    ██  ██ ████ ██  ██████   █████    ██████  
        ██       ██    ██  ██       ██    ██  ██  ██  ██  ██   ██  ██       ██   ██ 
         ██████   ██████    ██████   ██████   ██      ██  ██████   ███████  ██   ██     
            """
        print(Fore.GREEN + Style.BRIGHT + banner + Style.RESET_ALL)
        print(Fore.GREEN + f" Money Dogs")
        print(Fore.RED + f" FREE TO USE = Join us on {Fore.GREEN}t.me/cucumber_scripts")
        print(Fore.YELLOW + f" before start please '{Fore.GREEN}git pull{Fore.YELLOW}' to update bot")
        print(f"{Fore.WHITE}~" * 60)

    def set_proxy(self, proxy):
        self.session.proxies = {
            "http": proxy,
            "https": proxy,
        }
        if '@' in proxy:
            host_port = proxy.split('@')[-1]
        else:
            host_port = proxy.split('//')[-1]
        return host_port

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def get(self, id):
        tokens = json.loads(open("tokens.json").read())
        if str(id) not in tokens.keys():
            return None

        return tokens[str(id)]

    def get_token(self, query: str):
        url = 'https://api.moneydogs-ton.com/sessions'
        data = json.dumps({'encodedMessage': query, 'retentionCode': '48cdRxLi'})
        self.headers.update({
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        })

        response = self.session.post(url, headers=self.headers, data=data)
        data = response.json()
        if response.status_code == 200:
            return data['token']
        else:
            return None

    def user_info(self, token: str):
        url = 'https://api.moneydogs-ton.com/mdogs-deposits'
        self.headers.update({
            'Content-Length': '0',
            'Content-Type': 'application/json',
            'X-Auth-Token': token
        })

        response = self.session.get(url, headers=self.headers)
        data = response.json()
        if response.status_code == 200:
            return data
        else:
            return None

    def daily_checkin(self, token: str):
        url = 'https://api.moneydogs-ton.com/daily-check-in'
        self.headers.update({
            'Content-Length': '0',
            'Content-Type': 'application/json',
            'X-Auth-Token': token
        })

        response = self.session.post(url, headers=self.headers)
        data = response.json()
        if response.status_code == 200:
            return data
        else:
            return None

    def get_tasks(self, token: str, task_type: str = 'all'):
        base_url = 'https://api.moneydogs-ton.com/tasks'
        url = f"{base_url}?isFeatured=true" if task_type == 'featured' else base_url
        self.headers.update({
            'Content-Length': '0',
            'Content-Type': 'application/json',
            'X-Auth-Token': token
        })

        response = self.session.get(url, headers=self.headers)
        data = response.json()
        if response.status_code == 200:
            return data
        else:
            return None

    def complete_tasks(self, token: str, task_id: str):
        url = f'https://api.moneydogs-ton.com/tasks/{task_id}/verify'
        self.headers.update({
            'Content-Type': 'application/json',
            'X-Auth-Token': token
        })

        response = self.session.post(url, headers=self.headers)
        if response.status_code in [200, 201]:
            return True
        else:
            return None

    def process_query(self, query: str):
        token = self.get_token(query)
        if not token:
            self.log(
                f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT} Query ID Isn't Valid {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
            )
            return

        if token:
            user = self.user_info(token)
            if user:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {user['user']['firstName']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {user['remainingAmount']:.4f} $MDOGS {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )
                time.sleep(1)

                checkin = self.daily_checkin(token)
                if checkin:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Check-in{Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {checkin['rewardMdogs']} $MDOGS {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                else:
                    now = datetime.now(timezone.utc)
                    checkin_time = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0,
                                                                     microsecond=0).strftime('%x %X %Z')
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Check-in{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Not Time to Claim {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [ Next Claim at{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {checkin_time} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(1)

                for type in ['featured', 'all']:
                    tasks = self.get_tasks(token, type)
                    if tasks:
                        for task in tasks:
                            task_id = str(task['id'])

                            if task:
                                verify = self.complete_tasks(token, task_id)
                                if verify:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {task['title']} {Style.RESET_ALL}"
                                        f"{Fore.GREEN + Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {task['rewardMdogs']:.1f} $MDOGS {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Tasks{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {task['title']} {Style.RESET_ALL}"
                                        f"{Fore.RED + Style.BRIGHT}Isn't Completed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                                time.sleep(1)
                    else:
                        if tasks == 'featured':
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Partner Tasks{Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT} Is Completed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ General Tasks{Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT} Is Completed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                            )
            else:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )
    def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            with open('proxies.txt', 'r') as file:
                proxies = [line.strip() for line in file if line.strip()]

            while True:
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Proxy's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(proxies)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-----------------------------------------------------------------------{Style.RESET_ALL}")

                for i, query in enumerate(queries):
                    query = query.strip()
                    if query:

                        self.log(
                            f"{Fore.GREEN + Style.BRIGHT}Account: {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{i+1} / {len(queries)}{Style.RESET_ALL}"
                        )

                        if len(proxies) >= len(queries):
                            proxy = self.set_proxy(proxies[i])# Set proxy for each account
                            self.log(
                                f"{Fore.GREEN + Style.BRIGHT}Use proxy: {Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
                            )
                        else:
                            self.log(Fore.RED + "Number of proxies is less than the number of accounts. Proxies are not used!")

                        print(f"{Fore.YELLOW + Style.BRIGHT}[ Getting User Query... ]{Style.RESET_ALL}", end="\r",
                              flush=True)

                        user_info = extract_user_data(query)
                        user_id = str(user_info.get('id'))

                        self.headers = get_headers(user_id)
                        try:
                            self.process_query(query)
                        except Exception as e:
                            self.log(f"{Fore.RED + Style.BRIGHT}An error process_query: {e}{Style.RESET_ALL}")

                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}----------------------------------------------------------------------------{Style.RESET_ALL}")

                        account_delay = config['account_delay']
                        countdown_timer(random.randint(min(account_delay), max(account_delay)))

                cycle_delay = config['cycle_delay']
                countdown_timer(random.randint(min(cycle_delay), max(cycle_delay)))

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Money DOGS - BOT{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    if s_name() == 'Windows':
        sys(f'cls && title Money Dogs')
    else:
        sys('clear')
    moneydogs = MoneyDOGS()
    moneydogs.clear_terminal()
    moneydogs.welcome()
    moneydogs.main()