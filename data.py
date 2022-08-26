from version import Version
from requests import get
from color import color
from menu import UI
from time import sleep
from re import findall
from inputimeout import TimeoutOccurred, inputimeout
import json
ui = UI()
class data:
	def __init__(self):
		self.commands=[
			"hunt",
			"hunt",
			"battle"
			]
		self.wbm = [13,18]
		self.OwOID = '408785106942164992'
		self.totalcmd = 0
		self.totaltext = 0
		self.stopped = False
		self.version = int(''.join(map(str, Version)))
		self.wait_time_daily = 60
		with open('settings.json', "r") as file:
			data = json.load(file)
			self.token = data["token"]
			self.channel = data["channel"]
			self.gm = data["gm"]
			self.sm = data["sm"]
			self.pm = data["pm"]
			self.em = data["em"]
			self.prefix = data["prefix"]
			self.allowedid = data["allowedid"]
			self.webhook = data["webhook"]
			self.webhookping = data["webhookping"]
			self.daily = data["daily"]
			self.stop = data["stop"]
			self.change = data['change']
			self.sell = data['sell']
			self.solve = data['solve']
	def Version(self):
		response = get("https://raw.githubusercontent.com/ahihiyou20/discord-selfbot-owo-bot/development/source/src/version.py")
		version = response.text
		version = findall(r'\b\d+\b', version)
		return int(''.join(version))
	def check(self):
		version = self.Version()
		if self.token and self.channel == 'nothing':
			ui.slowPrinting(f"{color.fail} !!! [ERROR] !!! {color.reset} Please Enter Information To Continue")
			sleep(2)
			from newdata import main
			main()
		else:
			response = get('https://discord.com/api/v9/users/@me',headers={"Authorization": self.token})
			if response.status_code != 200:
				ui.slowPrinting(f"{color.fail} !!! [ERROR] !!! {color.reset} Invalid Token")
				sleep(2)
		ui.slowPrinting(f"{color.warning}Checking Update... {color.reset}")
		sleep(0.5)
		if self.version >= version:
			ui.slowPrinting(f"{color.okgreen}No Update Available {color.reset}")
		elif self.version < version:
			sleep(0.5)
			ui.slowPrinting(f"{color.warning}Update Available {color.reset}")
			ui.slowPrinting("Automatically Pick Option [NO] In 10 Seconds.")
		try:
			choice = inputimeout(prompt=f"{color.warning}Do You Want To Update (YES/NO): {color.reset}", timeout=10)
		except TimeoutOccurred:
			choice = "NO"
		if choice.lower() == "yes":
			import update
a = data()
a.check()
