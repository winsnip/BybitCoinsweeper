import os, json, time, requests, crayons, sys, re, hmac, hashlib, random, pytz, math
from datetime import datetime
import urllib.parse


def calc(i, s, a, o, d, g):
    st = (10 * i + max(0, 1200 - 10 * s) + 2000) * (1 + o / a) / 10
    return math.floor(st) + value(g)

def generate_hash(key, message):
    hmac_obj = hmac.new(key.encode(), message.encode(), hashlib.sha256)
    return hmac_obj.hexdigest()

def url_decode(encoded_url):
    return urllib.parse.unquote(encoded_url)

def value(input_str):
    return sum(ord(char) for char in input_str) / 1e5

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
            "tl-init-data": None,
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

    def login(self, init_data):
        try:
            self.headers = { "tl-init-data": init_data}
            response = self.session.post("https://api.bybitcoinsweeper.com/api/auth/login", json={"initData": init_data}, headers=self.headers)
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
        
    def userinfo(self):
        try:
            user = self.session.get("https://api.bybitcoinsweeper.com/api/users/me", headers=self.headers).json()
            return user
        except requests.RequestException as error:
            return {"success": False, "error": str(error)}        


    def score_win(self):
            try:
                min_game_time = 70
                max_game_time = 120
                game_time = random.randint(min_game_time, max_game_time)
                playgame = self.session.post("https://api.bybitcoinsweeper.com/api/games/start", json={}, headers=self.headers).json()
                if "message" in playgame:
                    if("expired" in playgame["message"]):
                        self.log("Query Expired Sir", "ERROR")
                        sys.exit(0)
                gameid = playgame["id"]
                rewarddata = playgame["rewards"]
                started_at = playgame["createdAt"]
                userdata = self.userinfo()
                self.log(f"Total Score: {userdata['score']+userdata['scoreFromReferrals']}","SUCCESS")
                unix_time_started = datetime.strptime(started_at, '%Y-%m-%dT%H:%M:%S.%fZ')
                unix_time_started = unix_time_started.replace(tzinfo=pytz.UTC)
                starttime = int(unix_time_started.timestamp() * 1000)
                self.log(f"Starting game {gameid}. Play time: {game_time} seconds", 'INFO')
                self.wait(game_time)
                i = f"{userdata['id']}v$2f1"
                first = f"{i}-{gameid}-{starttime}"
                last = f"{game_time}-{gameid}"
                score = calc(45, game_time, 54, 9, True, gameid)
                game_data = {
                    "bagCoins": rewarddata["bagCoins"],
                    "bits": rewarddata["bits"],
                    "gifts": rewarddata["gifts"],
                    "gameId": gameid,
                    'gameTime': game_time,
                    "h": generate_hash(first ,last),
                    'score': float(score)
                }
                res = self.session.post('https://api.bybitcoinsweeper.com/api/games/win', json=game_data, headers=self.headers)
                if res.status_code == 201:
                    self.info["score"] += score
                    self.log(f"Game Status: WIN","SUCCESS")
                elif res.status_code == 401:
                    self.log('Token expired, need to self.log in again', "ERROR")
                    return False
                else:
                    self.log(f"An Error Occurred With Code {res.status_code}", 'ERROR')
                self.wait(5)
            except requests.RequestException:
                self.log('Too Many Requests, Please Wait', 'WARNING')
                self.wait(60)
    

    def score_lose(self):
            try:
                min_game_time = 70
                max_game_time = 120
                game_time = random.randint(min_game_time, max_game_time)
                playgame = self.session.post("https://api.bybitcoinsweeper.com/api/games/start", json={}, headers=self.headers).json()
                if "message" in playgame:
                    if("expired" in playgame["message"]):
                        self.log("Query Expired Sir", "ERROR")
                        sys.exit(0)
                gameid = playgame["id"]
                rewarddata = playgame["rewards"]
                started_at = playgame["createdAt"]
                userdata = self.userinfo()
                self.log(f"Total Score: {userdata['score']}","SUCCESS")
                unix_time_started = datetime.strptime(started_at, '%Y-%m-%dT%H:%M:%S.%fZ')
                unix_time_started = unix_time_started.replace(tzinfo=pytz.UTC)
                self.log(f"Starting game {gameid}. Play time: {game_time} seconds", 'INFO')
                self.wait(game_time)
                game_data = {
                    "bagCoins": rewarddata["bagCoins"],
                    "bits": rewarddata["bits"],
                    "gifts": rewarddata["gifts"],
                    "gameId": gameid
                }
                res = self.session.post('https://api.bybitcoinsweeper.com/api/games/lose', json=game_data, headers=self.headers)
                if res.status_code == 201:
                    self.log(f"Game Status: LOSEEEEEEEE","ERROR")
                elif res.status_code == 401:
                    self.log('Token expired, need to self.log in again', "ERROR")
                    return False
                else:
                    self.log(f"An Error Occurred With Code {res.status_code}", 'ERROR')
                self.wait(5)
            except requests.RequestException:
                self.log('Too Many Requests, Please Wait', 'WARNING')
                self.wait(60)
    
    def score(self):
        for i in range(3):
            try:
                is_win = random.random() < float(0.8)
                if(is_win):
                    self.score_win()
                else:
                    self.score_lose()
            except Exception as e:
                print(e)
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
                login_result = self.login(init_data)
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
