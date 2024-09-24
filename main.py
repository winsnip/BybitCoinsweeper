import os, json, time, requests, crayons, sys
from datetime import datetime
import urllib.parse

def url_decode(encoded_url):
    return urllib.parse.unquote(encoded_url)

def print_banner():
    print(crayons.blue('██     ██ ██ ███    ██ ███████ ███    ██ ██ ██████  '))
    print(crayons.blue('██     ██ ██ ████   ██ ██      ████   ██ ██ ██   ██ '))
    print(crayons.blue('██  █  ██ ██ ██ ██  ██ ███████ ██ ██  ██ ██ ██████  '))
    print(crayons.blue('██ ███ ██ ██ ██  ██ ██      ██ ██  ██ ██ ██ ██      '))
    print(crayons.blue(' ███ ███  ██ ██   ████ ███████ ██   ████ ██ ██      '))
    print()
    print("Join our Telegram channel: https://t.me/winsnip")


class ByBit:
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,vi-VN;q=0.6,vi;q=0.5",
            "Content-Type": "application/json",
            "Origin": "https://bybitcoinsweeper.com",
            "Referer": "https://bybitcoinsweeper.com/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": '"Android"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Linux; Android 14; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.146 Mobile Safari/537.36"
        }
        self.info = {"score": 0}

    def log(self, message, level):
        levels = {
            "INFO": crayons.cyan,
            "ERROR": crayons.red,
            "SUCCESS": crayons.green,
            "WARNING": crayons.yellow
        }
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{crayons.white(current_time)} | {levels.get(level, crayons.cyan)(level)} | {message}")

    def wait(self, seconds):
        for i in range(seconds, 0, -1):
            timestamp = time.strftime("%H:%M:%S", time.localtime())
            sys.stdout.write(f"\r[{timestamp}] [*] Waiting {i} seconds to continue...")
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write("\r")
        sys.stdout.flush()

    def login(self, user_data):
        url = "https://api.bybitcoinsweeper.com/api/auth/login"
        payload = {
            "firstName": user_data["first_name"],
            "lastName": user_data.get("last_name", ""),
            "telegramId": str(user_data["id"]),
            "userName": user_data["username"]
        }

        try:
            response = self.session.post(url, json=payload, headers=self.headers)
            if response.status_code == 201:
                data = response.json()
                self.headers['Authorization'] = f"Bearer {data['accessToken']}"
                return {
                    "success": True,
                    "accessToken": data['accessToken'],
                    "refreshToken": data['refreshToken'],
                    "userId": data['id']
                }
            else:
                return {"success": False, "error": "Unexpected status code"}
        except requests.RequestException as error:
            return {"success": False, "error": str(error)}

    def score(self):
        for i in range(3):
            try:
                gametime = int(time.time()) % 211 + 90
                score = int(time.time()) % 301 + 600

                self.log(f"Starting game {i + 1}/3. Play time: {gametime} seconds", 'INFO')
                self.wait(gametime)

                game_data = {
                    'gameTime': gametime,
                    'score': score
                }

                res = self.session.patch('https://api.bybitcoinsweeper.com/api/users/score', json=game_data, headers=self.headers)

                if res.status_code == 200:
                    self.info["score"] += score
                    self.log(f"Game Played Successfully: received {score} points | Total: {self.info['score']}","SUCCESS")
                elif res.status_code == 401:
                    self.log('Token expired, need to self.log in again', "ERROR")
                    return False
                else:
                    self.log(f"An Error Occurred With Code {res.status_code}", 'ERROR')

                self.wait(5)
            except requests.RequestException:
                self.log('Too Many Requests, Please Wait', 'WARNING')
                self.wait(60)
        return True

    def main(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()
        data_file = os.path.join(os.path.dirname(__file__), 'data.txt')
        with open(data_file, 'r', encoding='utf8') as f:
            data = [line.strip() for line in f if line.strip()]

        while True:
            proxies = [line.strip() for line in open('proxy.txt') if line.strip()]
            for i, init_data in enumerate(data):
                proxy = proxies[(i - 1) % len(proxies)] if proxies else None
                if proxy:
                    self.session.proxies.update({'http': proxy, 'https': proxy})
                decoded = url_decode(init_data)
                finaldat = (url_decode(decoded))
                user_data = json.loads(finaldat.split('user=')[1].split('&')[0])
                self.log(f"========== Account {i + 1} | {user_data['first_name']} ==========", 'INFO')
                self.log(f"self.logging into account {user_data['id']}...", 'INFO')
                login_result = self.login(user_data)
                if login_result["success"]:
                    self.log('login successful!', "SUCCESS")
                    game_result = self.score()
                    if not game_result:
                        self.log('Need to self.log in again, moving to the next account', 'WARNING')
                else:
                    self.log(f"login failed! {login_result['error']}", 'ERROR')

                if i < len(data) - 1:
                    self.wait(3)

            self.wait(3)

if __name__ == '__main__':
    client = ByBit()
    try:
        client.main()
    except Exception as err:
        print(str(err))
        sys.exit(1)
