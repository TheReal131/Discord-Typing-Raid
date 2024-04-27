import aiohttp,asyncio,discord,random,time,string,json

R = '\033[1;31m'
B = '\033[1;34m'
C = '\033[1;37m'
G = '\033[1;32m'
Y = '\033[1;33m'
Q = '\033[1;36m'

TokenList = "토큰.txt"

def Config():
    with open('설정.json', 'r', encoding="utf-8") as config_file:
        config_data = json.load(config_file)
    서버아이디 = config_data.get("서버아이디", "")
    채널아이디 = config_data.get("채널아이디", "")
    타이핑딜레이 = int(config_data.get("타이핑딜레이", 7))
    닉변딜레이 = int(config_data.get("닉변딜레이", 20))
    랜덤닉네임최소길이 = int(config_data.get("랜덤닉네임최소길이", 4))
    랜덤닉네임최대길이 = int(config_data.get("랜덤닉네임최대길이", 10))

    return 서버아이디, 채널아이디, 랜덤닉네임최소길이, 랜덤닉네임최대길이, 타이핑딜레이, 닉변딜레이

async def sendTyping(session, userToken):
    headers = {
        "Authorization": userToken,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9023 Chrome/108.0.5359.215 Electron/22.3.26 Safari/537.36",
        "Accept": "*/*",
        "Origin": "https://discord.com",
        "Referer": f"https://discord.com/channels/@me/{채널아이디}",
        "Content-Length": "0"
    }

    async with session.post(f"https://discord.com/api/v9/channels/{채널아이디}/typing", headers=headers) as response:
        if response.status == 204:
            print('[%s%s%s] Typing 요청에 성공했습니다!' % (G, response.status, C))
        elif response.status == 401:
            print('[%s%s%s] Typing 요청에 실패했습니다... 토큰이 유효한지 확인해주세요' % (R, response.status, C))
        elif response.status == 403:
            print('[%s%s%s] Typing 요청이 거부되었습니다... 채널을 다시 확인해주세요' % (R, response.status, C))
        else:
            print('[%s%s%s] Typing 요청 중 알 수 없는 오류가 발생했습니다' % (R, response.status, C))
            print('기술 지원이 필요하시다면 다음 연락처로 연락해주시기 바랍니다 %sDiscord%s: %schundoohwan%s' % (B, C, Q, C))
            exit()

def GenNick():
    length = random.randint(int(닉네임최소길이), int(닉네임최대길이))
    first_char = random.choice(string.ascii_lowercase)
    rest_chars = [random.choice(string.ascii_letters + string.digits) for _ in range(length - 1)]
    return first_char + ''.join(rest_chars)

async def ChNick(session, userToken):
    headers = {
        "Authorization": userToken,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9023 Chrome/108.0.5359.215 Electron/22.3.26 Safari/537.36",
        "Accept": "*/*",
        "Origin": "https://discord.com",
        "Content-Type": "application/json"
    }
    
    random_nickname = GenNick()
    data = {
        "nick": random_nickname
    }
    async with session.patch(f"https://discord.com/api/v9/guilds/{서버아이디}/members/@me/nick", headers=headers, json=data) as response:
        if response.status == 200:
            print(f'[%s%s%s] 닉네임이 성공적으로 변경되었습니다: {random_nickname}' % (G, response.status, C))
        elif response.status == 400:
            print(f'[%s%s%s] 닉네임 변경에 실패했습니다: 잘못된 요청' % (R, response.status, C))
        elif response.status == 401:
            print(f'[%s%s%s] 닉네임 변경에 실패했습니다: 토큰이 유효한지 확인해주세요' % (R, response.status, C))
        elif response.status == 403:
            print(f'[%s%s%s] 닉네임 변경에 실패했습니다: 권한이 없습니다' % (R, response.status, C))
        else:
            print(f'[%s%s%s] 닉네임 변경 중 알 수 없는 오류가 발생했습니다' % (R, response.status, C))
            print('기술 지원이 필요하시다면 다음 연락처로 연락해주시기 바랍니다 %sDiscord%s: %schundoohwan%s' % (B, C, Q, C))
            exit()

async def main1():
    async with aiohttp.ClientSession() as session:
        with open(TokenList, "r") as file:
            userTokens = [line.strip() for line in file.readlines()]
        
        while True:
            typing_tasks = [asyncio.create_task(sendTyping(session, userToken)) for userToken in userTokens]
            await asyncio.gather(*typing_tasks)
            await asyncio.sleep(int(타이핑딜레이))

async def main2():
    async with aiohttp.ClientSession() as session:
        with open(TokenList, "r") as file:
            userTokens = [line.strip() for line in file.readlines()]
        
        while True:
            nickname_tasks = [asyncio.create_task(ChNick(session, userToken)) for userToken in userTokens]
            await asyncio.gather(*nickname_tasks)
            await asyncio.sleep(int(닉변딜레이))

if __name__ == '__main__':
    print('\n%sCTRL%s + %sC%s 를 입력하여 스크립트를 중지할 수 있습니다.\n' % (C, Y, C, Y,))

    서버아이디, 채널아이디, 닉네임최소길이, 닉네임최대길이, 타이핑딜레이, 닉변딜레이 = Config()

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(main1(), main2()))
    except KeyboardInterrupt:
        print('\n스크립트가 중지되었습니다. 이용해 주셔서 감사합니다! :D\n')