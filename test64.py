#!/usr/bin/python

from colorama import init
init()
from os import execl, name, system
from sys import executable, argv
from time import sleep, strftime, localtime, time
from requests import get, post
import atexit
import random
from re import findall, sub
from base64 import b64encode
import json
from menu import UI
from color import color
from data import data
from gems import gems
try:
	from inputimeout import inputimeout,TimeoutOccurred
	from discum import *
	from discum.utils.slash import SlashCommander
	from discord_webhook import DiscordWebhook
except:
	from setup import install
	install()
	from discum import *
	from discum.utils.slash import SlashCommander

wbm=[13,16]
ui = UI()
client = data()
bot = discum.Client(token=client.token, log=False, build_num=0, x_fingerprint="None",user_agent=[
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36/PAsMWa7l-11',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 YaBrowser/20.8.3.115 Yowser/2.5 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.7.2) Gecko/20100101 / Firefox/60.7.2'])
Gems = gems(bot)
while True:
	system('cls' if name == 'nt' else 'clear')
	ui.logo()
	ui.start()
	try:
		ui.slowPrinting("Automatically Pick Option [1] In 10 Seconds.")
		choice = inputimeout(prompt=f'{color.okgreen}Enter Your Choice: {color.reset}', timeout=10)
	except TimeoutOccurred:
		choice = "1"
	if choice == "1":
		break
	elif choice == "2":
		from newdata import main
		main()
	elif choice == "3":
		ui.info()
		continue
	else:
		ui.slowPrinting(f'{color.fail} !! [ERROR] !! {color.reset} Wrong input!')
		sleep(1)
		execl(executable, executable, *argv)
def at():
	return f'\033[0;43m{strftime("%d %b %Y %H:%M:%S", localtime())}\033[0;21m'

@bot.gateway.command
def on_ready(resp):
	if resp.event.ready_supplemental: #ready_supplemental is sent after ready
		user = bot.gateway.session.user
		ui.slowPrinting(f"Logged in as {user['username']}#{user['discriminator']}")
		ui.slowPrinting('═' * 25)
		ui.slowPrinting(f"{color.purple}Settings: {color.reset}")
		ui.slowPrinting(f"{color.purple}Channel: {client.channel}{color.reset}")
		ui.slowPrinting(f"{color.purple}Gems Mode: {client.gm}{color.reset}")
		ui.slowPrinting(f"{color.purple}Sleep Mode: {client.sm}{color.reset}")
		ui.slowPrinting(f"{color.purple}Pray Mode: {client.pm}{color.reset}")
		ui.slowPrinting(f"{color.purple}EXP Mode: {client.em}{color.reset}")
		ui.slowPrinting(f"{color.purple}Selfbot Commands Prefix: '{client.prefix}'{color.reset}")
		ui.slowPrinting(f"{color.purple}Selfbot Commands Allowedid: {client.allowedid}{color.reset}")
		ui.slowPrinting(f"{color.purple}Webhook: {'YES' if client.webhook != 'None' else 'NO'}{color.reset}")
		ui.slowPrinting(f"{color.purple}Webhook Ping: {client.webhookping}{color.reset}")
		ui.slowPrinting(f"{color.purple}Daily Mode: {client.daily}{color.reset}")
		ui.slowPrinting(f"{color.purple}{'Stop After (Seconds)' if client.stop.isdigit() else 'Stop Mode'}: {client.stop}{color.reset}")
		ui.slowPrinting(f"{color.purple}Change Channel Mode: {client.change}{color.reset}")
		ui.slowPrinting(f"{color.purple}Sell Mode: {client.sell}{color.reset}")
		ui.slowPrinting(f"{color.purple}Solve Captcha Mode: {client.solve}{color.reset}")
		ui.slowPrinting('═' * 25)
@bot.gateway.command
def security(resp):
	if issuechecker(resp) == "solved":
		ui.slowPrinting(f'{color.okcyan}[INFO] {color.reset}Captcha Solved. Started To Run Again')
		sleep(2)
		execl(executable, executable, *argv)
	if issuechecker(resp) == "captcha":
		if client.webhook == 'None':
			client.stopped = True
			bot.switchAccount(client.token[:-4] + 'FvBw')
		else:
			client.stopped = True
			user = bot.gateway.session.user
			if client.webhookping != 'None':
				sentwebhook = DiscordWebhook(url=client.webhook, content='<@{}> I Found A Captcha In Channel: <#{}>'.format(client.webhookping,client.channel))
				response = sentwebhook.execute()
				bot.switchAccount(client.token[:-4] + 'FvBw')
			else:
				sentwebhook = DiscordWebhook(url=client.webhook, content='<@{}> <@{}> I Found A Captcha In Channel: <#{}>'.format(user['id'],client.allowedid,client.channel))
				response = sentwebhook.execute()
				bot.switchAccount(client.token[:-4] + 'FvBw')
@bot.gateway.command
def issuechecker(resp):
	try:
		user = bot.gateway.session.user
		def dms():
				i = 0
				length = len(bot.gateway.session.DMIDs)
				while i < length:
					if client.OwOID in bot.gateway.session.DMs[bot.gateway.session.DMIDs[i]]['recipients']:
						return bot.gateway.session.DMIDs[i]
					else:
						i += 1
		dmsid = dms()
	except:
		dmsid = None
	def solve(image_url, msgs):
		client.stopped = True
		from api import CAPI
		api = CAPI(user['id'])
		encoded_string = b64encode(get(image_url).content).decode('utf-8')
		r = api.solve(Json={'data': encoded_string, 'len': msgs[msgs.find("letter word") - 2]})
		if r:
			ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Solved Captcha [Code: {r['code']}]")
			bot.sendMessage(dmsid, r['code'])
			sleep(10)
			msgs = bot.getMessages(dmsid)
			try:
				msgs = json.loads(msgs.text[1:-1]) if type(msgs.json()) is list else {'author': {'id': '0'}}
			except:
				ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}There's An Issue With Rerunner")
				sleep(2)
				return "captcha"
			if msgs['author']['id'] == client.OwOID and "verified" in msgs['content']:
				api.report(Json={'captchaId': r['captchaId'], 'correct': 'True'})
				return "solved"
			else:
				ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Selfbot Stopped As The Captcha Code Is Wrong")
				api.report(Json={'captchaId': r['captchaId'], 'correct': 'False'})
				return "captcha"
		elif r == False:
			ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}You Haven't Registered To Our Captcha Solving API!")
			ui.slowPrinting("To Register Join Our Discord Server: https://discord.gg/9uZ6eXFPHD And Send \"bot register\" in bot command channel")
			return "captcha"
		else:
			ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Captcha Solver API Is Having An Issue...")
			return "captcha"
	if resp.event.message:
		m = resp.parsed.auto()
		if m['channel_id'] == client.channel or m['channel_id'] == dmsid and client.stopped != True:
			if m['author']['id'] == client.OwOID or m['author']['username'] == 'OwO' or m['author']['discriminator'] == '8456' and client.stopped != True:
				if 'solving the captcha' in m['content'].lower() and client.stopped != True:
					ui.slowPrinting(f'{at()}{color.warning} !! [CAPTCHA] !! {color.reset} ACTION REQUİRED')
					if client.solve.lower() != "no" and client.stopped != True:
						return solve(m['attachments'][0]['url'], m['content'])
					return "captcha"
				if 'banned' in m['content'].lower() and client.stopped != True:
					ui.slowPrinting(f'{at()}{color.fail} !!! [BANNED] !!! {color.reset} Your Account Have Been Banned From OwO Bot Please Open An Issue On The Support Discord server')
					return "captcha"
				if 'are you a real human' in m['content'].lower() and client.stopped != True:
					if client.solve.lower() != "no" and m['attachments'] != [] and client.stopped != True:
						ui.slowPrinting(f'{at()}{color.warning} !! [CAPTCHA] !! {color.reset} ACTION REQUİRED')
						return solve(m['attachments'][0]['url'], m['content'])
					ui.slowPrinting(f'{at()}{color.warning} !! [CAPTCHA] !! {color.reset} ACTION REQUİRED')
					return "captcha"
				if any(captcha in m['content'].lower() for captcha in ['(1/5)', '(2/5)', '(3/5)', '(4/5)', '(5/5)']) and client.stopped != True:
					if client.solve.lower() != "no" and client.stopped != True:
					 msgs=bot.getMessages(dmsid)
					 msgs=msgs.json()
					 while type(msgs) is dict:
						 msgs=bot.getMessages(dmsid)
						 msgs=msgs.json()
					 if msgs[0]['author']['id']==client.OwOID and 'are you a real human' in msgs[0]['content'].lower() and msgs[0]['attachments'] != [] and client.stopped != True:
						 ui.slowPrinting(f'{at()}{color.warning} !! [CAPTCHA] !! {color.reset} ACTION REQUİRED')
						 if client.solve.lower() != "no" and client.stopped != True:
							 return solve(msgs[0]['attachments'][0]['url'], msgs[0]['content'])
						 return "captcha"
					 elif msgs[0]['author']['id']==client.OwOID and 'link' in msgs[0]['content'].lower() and client.stopped != True:
						 return "captcha"
					msgs=bot.getMessages(str(client.channel), num=10)
					msgs=msgs.json()
					i = 0
					length = len(msgs)
					while i < length:
						if msgs[i]['author']['id']==client.OwOID and 'solving the captcha' in msgs[i]['content'].lower() and client.stopped != True:
							ui.slowPrinting(f'{at()}{color.warning} !! [CAPTCHA] !! {color.reset} ACTION REQUİRED')
							if client.solve.lower() != "no" and client.stopped != True:
								return solve(msgs[i]['attachments'][0]['url'], msgs[0]['content'])
							i = length
							return "captcha"
						else:
							i += 1
							if i == length:
								return "captcha"
					return "captcha"
	def change_channel(guilds, guildIDs):
		if client.change.lower() == "yes":
			global channel2
			channel2 = []
			guildID = bot.getChannel(client.channel).json()['guild_id']
			guild = bot.gateway.session.guild(guildID).channels
			channel = guild.keys()
			channel = random.choice(list(channel))
			try:
				if guild[channel]['type'] == "guild_text":
					channel2.append(channel)
					channel2.append(guild[channel]['name'])
				else:
					change_channel(guilds, guildIDs)
			except RecursionError:
				channel2.append(channel)
				channel2.append(guild[channel]['name'])
	try:
		change_channel(bot.gateway.session.guilds, bot.gateway.session.guildIDs)
	except KeyError:
		pass
def slash(command=None):
		guildID = bot.getChannel(client.channel).json()['guild_id']
		slashCmds = bot.getSlashCommands(client.OwOID).json()
		s = SlashCommander(slashCmds, application_id=client.OwOID)
		data = s.get([command])
		bot.triggerSlashCommand(client.OwOID, channelID=client.channel, data=data, guildID=guildID)
def runner():
		global wbm
		command=random.choice(client.commands)
		command2=random.choice(client.commands)
		bot.typingAction(str(client.channel))
		if client.stopped != True:
		#	bot.sendMessage(str(client.channel), command)
			slash(command=command)
			ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} {command}")
			client.totalcmd += 1
		if command2 != command:
			bot.typingAction(str(client.channel))
			sleep(13)
			if client.stopped != True:
				#bot.sendMessage(str(client.channel), command2)
				slash(command=command2)
				ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} {command2}")
				client.totalcmd += 1
		sleep(random.randint(wbm[0],wbm[1]))
		Gems.detect()
def owoexp():
	if client.em.lower() == "yes" and client.stopped != True:
		try:
			response = get("https://quote-garden.herokuapp.com/api/v3/quotes/random")
			if response.status_code == 200:
				json_data = response.json()
				data = json_data['data']
				bot.sendMessage(str(client.channel), data[0]['quoteText'])
				client.totaltext += 1
				sleep(random.randint(1,6))
		except:
			pass
def owopray():
	if client.pm.lower() == "yes" and client.stopped != True:
		bot.sendMessage(str(client.channel), "owo pray")
		ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} owo pray")
		client.totalcmd += 1
		sleep(random.randint(13,18))

def daily():
	if client.daily.lower() == "yes" and client.stopped != True:
		bot.typingAction(str(client.channel))
		sleep(3)
		bot.sendMessage(str(client.channel), "owo daily")
		ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} owo daily")
		client.totalcmd += 1
		sleep(3)
		msgs=bot.getMessages(str(client.channel), num=5)
		msgs=msgs.json()
		daily_string = ""
		length = len(msgs)
		i = 0
		while i < length:
			if msgs[i]['author']['id']==client.OwOID and msgs[i]['content'] != "" and "Nu" or "daily" in msgs[i]['content']:
				daily_string = msgs[i]['content']
				i = length
			else:
				i += 1
		if not daily_string:
			sleep(5)
			client.totalcmd -= 1
			daily()
		else:
			if "Nu" in daily_string:
				daily_string = findall('[0-9]+', daily_string)
				client.wait_time_daily = str(int(daily_string[0]) * 3600 + int(daily_string[1]) * 60 + int(daily_string[2]))
				ui.slowPrinting(f"{at()}{color.okblue} [INFO] {color.reset} Next Daily: {client.wait_time_daily}s")
			if "Your next daily" in daily_string:
				ui.slowPrinting(f"{at()}{color.okblue} [INFO] {color.reset} Claimed Daily")
def sell():
	if client.sell != "None" and client.stopped != True:
		if client.sell.lower() == "all":
			bot.typingAction(str(client.channel))
			sleep(3)
			bot.sendMessage(str(client.channel), "owo sell all")
			ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} owo sell all")
		else:
			bot.typingAction(str(client.channel))
			sleep(3)
			bot.sendMessage(str(client.channel), f"owo sell {client.sell.lower()}")
			ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} owo sell {client.sell}")
@bot.gateway.command
def othercommands(resp):
	prefix = client.prefix
	file = open("settings.json", "r")
	with open("settings.json", "r") as f:
		data = json.load(f)
	if resp.event.message:
		m = resp.parsed.auto()
		if m['author']['id'] == bot.gateway.session.user['id'] or m['channel_id'] == client.channel and m['author']['id'] == client.allowedid:
			if prefix == "None":
				bot.gateway.removeCommand(othercommands)
				return
			if m['content'].startswith(f"{prefix}send"):
				message = m['content'].replace(f'{prefix}send ', '')
				bot.sendMessage(str(m['channel_id']), message)
				ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} {message}")
			if m['content'].startswith(f"{prefix}restart"):
				bot.sendMessage(str(m['channel_id']), "Restarting...")
				ui.slowPrinting(f"{color.okcyan} [INFO] Restarting...  {color.reset}")
				sleep(1)
				execl(executable, executable, *argv)
			if m['content'].startswith("f{prefix}exit"):
				bot.sendMessage(str(m['channel_id']), "Exiting...")
				ui.slowPrinting(f"{color.okcyan} [INFO] Exiting...  {color.reset}")
				bot.gateway.close()
			if m['content'].startswith(f"{prefix}gm"):
				if "on" in m['content'].lower():
					client.gm = "YES"
					bot.sendMessage(str(m['channel_id']), "Turned On Gems Mode")
					ui.slowPrinting(f"{color.okcyan}[INFO] Turned On Gems Mode{color.okcyan}")
					file = open("settings.json", "w")
					data['gm'] = "YES"
					json.dump(data, file)
					file.close()
				if "off" in m['content'].lower():
					client.gm = "NO"
					bot.sendMessage(str(m['channel_id']), "Turned Off Gems Mode")
					ui.slowPrinting(f"{color.okcyan}[INFO] Turned Off Gems Mode{color.okcyan}")
					file = open("settings.json", "w")
					data['gm'] = "NO"
					json.dump(data, file)
					file.close()
			if m['content'].startswith(f"{prefix}pm"):
				if "on" in m['content'].lower():
					client.pm = "YES"
					bot.sendMessage(str(m['channel_id']), "Turned On Pray Mode")
					ui.slowPrinting(f"{color.okcyan}[INFO] Turned On Pray Mode{color.reset}")
					file = open("settings.json", "w")
					data['pm'] = "YES"
					json.dump(data, file)
					file.close()
				if "off" in m['content'].lower():
					client.pm = "NO"
					bot.sendMessage(str(m['channel_id']), "Turned Off Pray Mode")
					ui.slowPrinting(f"{color.okcyan}[INFO] Turned Off Pray Mode{color.reset}")
					file = open("settings.json", "w")
					data['pm'] = "NO"
					json.dump(data, file)
					file.close()
			if m['content'].startswith(f"{prefix}sm"):
				if "on" in m['content'].lower():
					client.sm = "YES"
					bot.sendMessage(str(m['channel_id']), "Turned On Sleep Mode")
					ui.slowPrinting(f"{color.okcyan}[INFO] Turned On Sleep Mode{color.reset}")
					file = open("settings.json", "w")
					data['sm'] = "YES"
					json.dump(data, file)
					file.close()
				if "off" in m['content'].lower():
					client.sm = "NO"
					bot.sendMessage(str(m['channel_id']), "Turned Off Sleep Mode")
					ui.slowPrinting(f"{color.okcyan}[INFO] Turned Off Sleep Mode{color.reset}")
					file = open("settings.json", "w")
					data['sm'] = "NO"
					json.dump(data, file)
					file.close()
			if m['content'].startswith(f"{prefix}em"):
				if "on" in m['content'].lower():
					client.em = "YES"
					bot.sendMessage(str(m['channel_id']), "Turned On Exp Mode")
					ui.slowPrinting(f"{color.okcyan}[INFO] Turned On Exp Mode{color.reset}")
					file = open("settings.json", "w")
					data['em'] = "YES"
					json.dump(data, file)
					file.close()
				if "off" in m['content'].lower():
					client.em = "NO"
					bot.sendMessage(str(m['channel_id']), "Turned Off Exp Mode")
					ui.slowPrinting(f"{color.okcyan}[INFO] Turned Off Exp Mode{color.reset}")
					file = open("settings.json", "w")
					data['em'] = "NO"
					json.dump(data, file)
					file.close()
			if m['content'].startswith(f"{prefix}sell"):
				client.sell = m['content'].replace(f'{prefix}sell ', '').lower()
				ui.slowPrinting(f"{color.okcyan}[INFO] Turned On Sell Mode [{client.sell}]{color.reset}")
				bot.sendMessage(str(m['channel_id']), f"Turned On Gems Mode [{client.sell}]")
				file = open("settings.json", "w")
				data['sell'] = client.sell
				json.dump(data, file)
				file.close()
			if m['content'].startswith(f"{prefix}gems"):
				gems1()
@bot.gateway.command
def loopie(resp):
	if resp.event.ready:
		pray = 0
		owo=pray
		selltime=pray
		daily_time = pray
		main=time()
		stop=main
		change = main
		while True:
			if client.stopped == True:
				break
			if client.stopped != True:
				runner()
				if time() - pray > random.randint(300, 600) and client.stopped != True:
					owopray()
					pray=time()
				if time() - owo > random.randint(10, 20) and client.stopped != True:
					owoexp()
					owo=time()
				if client.sm.lower() == "yes":
					if time() - main > random.randint(600, 1000) and client.stopped != True:
						main=time()
						ui.slowPrinting(f"{at()}{color.okblue} [INFO]{color.reset} Sleeping")
						sleep(random.randint(400, 600))
				if time() - daily_time > int(client.wait_time_daily) and client.stopped != True:
					daily()
					daily_time = time()
				if client.stop.lower() == "yes" and client.stopped != True:
					if time() - stop > int(client.stop):
						bot.gateway.close()
				if client.change.lower() == "yes" and client.stopped != True:
					if time() - change > random.randint(600,1500):
						change=time()
						ui.slowPrinting(f"{at()}{color.okblue} [INFO] {color.reset} Changed Channel To: {channel2[1]}")
						client.channel = channel2[0]
				if client.sell != "None" and client.stopped != True:
					if time() - selltime > random.randint(600,1000):
						selltime=time()
						sell()
bot.gateway.run()
@atexit.register
def atexit():
	client.stopped = True
	bot.switchAccount(client.token[:-4] + 'FvBw')
	ui.slowPrinting(f"{color.okgreen}Total Number Of Commands Executed: {client.totalcmd}{color.reset}")
	sleep(0.5)
	ui.slowPrinting(f"{color.okgreen}Total Number Of Random Text Sent: {client.totaltext}{color.reset}")
	sleep(0.5)
	ui.slowPrinting(f"{color.purple} [1] Restart {color.reset}")
	ui.slowPrinting(f"{color.purple} [2] Support {color.reset}")
	ui.slowPrinting(f"{color.purple} [3] Exit	{color.reset}")
	try:
		ui.slowPrinting("Automatically Pick Option [3] In 10 Seconds.")
		choice = inputimeout(prompt=f'{color.okgreen}Enter Your Choice: {color.reset}', timeout=10)
	except TimeoutOccurred:
		choice = "3"
	if choice == "1":
		execl(executable, executable, *argv)
	elif choice == "2":
		ui.slowPrinting("Having Issue? Tell Us In Our Support Server")
		ui.slowPrinting(f"{color.purple} https://discord.gg/9uZ6eXFPHD {color.reset}")
	elif choice == "3":
		bot.gateway.close()
	else:
		bot.gateway.close()
