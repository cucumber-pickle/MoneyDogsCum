import requests
import json
import os
from colorama import *
from datetime import datetime
from core.helper import get_headers, countdown_timer, extract_user_data, config
import random

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
        data = json.dumps({'encodedMessage': query})
        self.headers.update({
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        })

        try:
            response = self.session.post(url, headers=self.headers, data=data, timeout=10)  # Set timeout
            data = response.json()
            if response.status_code == 200:
                return data['token']
            else:
                return None
        except requests.exceptions.Timeout:
            self.log("Request timed out. Please check your network connection or proxy settings.")
            return None
        except requests.exceptions.RequestException as e:
            self.log(f"An error occurred: {e}")
            return None

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

    def user_info(self, token: str):
        url = 'https://api.moneydogs-ton.com/rankings/deposits/me'
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
        
    def get_tasks(self, token: str):
        url = 'https://api.moneydogs-ton.com/tasks'
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
        if response.status_code == 201:
            return True
        elif response.status_code == 200:
            try:
                data = response.json()
                return data
            except ValueError:
                return True
        else:
            return False

    def save(self, id, token):
        tokens = json.loads(open("tokens.json").read())
        tokens[str(id)] = token
        open("tokens.json", "w").write(json.dumps(tokens, indent=4))

    def process_query(self, query: str, id: str):

        #проверяем есть ли токен в токенс, если нет, то логинимся и сохряняем новый
        token = self.get(id)
        if token is None:
            token = self.get_token(query)
            if token is None:
                return False
            self.save(id, token)

        if token:
            user_info = self.user_info(token)
            if user_info:
                first_name = user_info['firstName']
                balance = f"{user_info['score']:.4f}"
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {first_name} {Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT}] {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {balance} MDOGS {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )
            else:
                self.log(f"[ User Not Found ]")

            print(
                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.YELLOW + Style.BRIGHT}[ Get Daily Check-in... ]{Style.RESET_ALL}",
                end="\r",
                flush=True
            )
            countdown_timer(2)
            checkin = self.daily_checkin(token)
            if checkin:
                reward = checkin['rewardMdogs']
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Check-in{Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT} Success {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {reward} MDOGS {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )
            else:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Check-in{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Already Check-in Today {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}      "
                )

            print(
                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.YELLOW + Style.BRIGHT}[ Get Available Tasks... ]{Style.RESET_ALL}",
                end="\r",
                flush=True
            )
            countdown_timer(2)
            tasks = self.get_tasks(token)
            manual_task = False
            if tasks:
                for task in tasks:
                    task_id = task['id']
                    title = task['title']

                    if task['code'] is None:
                        print(
                            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Task{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}is Strarting...{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}",
                            end="\r",
                            flush=True
                        )
                        countdown_timer(2)
                        complete_task = self.complete_tasks(token, task_id)

                        if complete_task:
                            reward = int(task['rewardMdogs'])
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}is Completed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {reward} MDOGS {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}          "
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT}is Failed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}                          "
                            )
                    else:
                        manual_task = True

                if manual_task:
                    self.log(f"{Fore.YELLOW + Style.BRIGHT}[Other tasks require authentication]{Style.RESET_ALL}")
        else:
            self.log(f"{Fore.RED+Style.BRIGHT}[Check Proxy!]{Style.RESET_ALL}")


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

                        self.process_query(query, user_id)

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
    moneydogs = MoneyDOGS()
    moneydogs.clear_terminal()
    moneydogs.welcome()
    moneydogs.main()