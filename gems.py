from data import data
from time import sleep, strftime, localtime
from color import color
from colorama import init
from menu import UI
from re import findall, sub
client = data()
ui= UI()
init()
class gems:
	def __init__(self, bot):
		self.bot = bot
		self.available = [1, 3, 4]
		self.gemtypes = [1, 3, 4]
		self.regex = "gem(\d):\d+>`\[(\d+)"
	def at(self):
		return f'\033[0;43m{strftime("%d %b %Y %H:%M:%S", localtime())}\033[0;21m'
	def useGems(self, gemslist=[1,3,4]):
		def switchCode(code):
			for i in code:
				if i == 1:
					code[code.index(i)] = 0
				elif i == 3:
					code[code.index(i)] = 1
				elif i == 4:
					code[code.index(i)] = 2
		print(f"Input Code: {gemslist}")
		switchCode(gemslist)
		self.bot.typingAction(str(client.channel))
		sleep(3)
		self.bot.sendMessage(str(client.channel), "owo inv")
		ui.slowPrinting(f"{self.at()}{color.okgreen} [SENT] {color.reset} owo inv")
		client.totalcmd += 1
		sleep(5)
		msgs=self.bot.getMessages(str(client.channel), num=5)
		msgs=msgs.json()
		inv = ""
		for i in range(len(msgs)):
			if msgs[i]['author']['id'] == client.OwOID and 'Inventory' in msgs[i]['content']:
				inv=findall(r'`(.*?)`', msgs[i]['content'])
		if not inv:
			sleep(5)
			client.totalcmd -= 1
			self.useGems()
		else:
			if '050' in inv:
				self.bot.sendMessage(str(client.channel), "owo lb all")
				ui.slowPrinting(f"{self.at()}{color.okgreen} [SENT] {color.reset} owo lb all")
				sleep(13)
				self.useGems()
			if '100' in inv:
				self.bot.sendMessage(str(client.channel), "owo crate all")
				ui.slowPrinting(f"{self.at()}{color.okgreen} [SENT] {color.reset} owo crate all")
				self.available = list(self.gemtypes)
				sleep(2)
			for item in inv:
				try:
					if int(item) >= 100 or int(item) <= 50:
						inv.pop(inv.index(item)) #weapons
				except: #backgounds etc
					inv.pop(inv.index(item))
			tier = [[],[],[]]
			ui.slowPrinting(f"{self.at()}{color.okblue} [INFO] {color.reset} Found {len(inv)} Gems Inventory")
			self.available = []
			for gem in inv:
				gem = sub(r"[^a-zA-Z0-9]", "", gem)
				gem = int(gem)
				if 50 < gem < 58:
					tier[0].append(gem)
					self.available.append(1)
				elif 64 < gem < 72:
					tier[1].append(gem)
					self.available.append(3)
				elif 71 < gem <  79:
					tier[2].append(gem)
					self.available.append(4)
			print(f"Output Code: {gemslist}")
			for level in gemslist:
					if not len(tier[level]) == 0:
						sleep(5)
						self.bot.sendMessage(str(client.channel), "owo use "+ str(max(tier[level])))
						ui.slowPrinting(f"{self.at()}{color.okgreen} [SENT] {color.reset} owo use {str(max(tier[level]))}")
	def detect(self):
		def isAvailable(gem):
			if gem in self.available:
				return True
			return False
		m = self.bot.getMessages(client.channel, num = 10).json()
		while type(m) is dict:
			m = self.bot.getMessages(client.channel, num = 10).json()
		i = 0
		length = len(m)
		while i < length:
			if m[i]['author']['id'] == client.OwOID and "**🌱" in m[i]['content']:
				m = m[i]
				i = length
			i += 1
			if i > length:
				self.detect()
		print(m['content'])
		gems = findall(self.regex, m['content'])
		print(f"Output Regex: {gems}")
		usegems = list(self.gemtypes)
		usegems2 = []
		if len(gems) < 3:
			for i in gems:
				if int(i[0]) in usegems:
					usegems.pop(usegems.index(int(i[0])))
			for i in usegems:
				if isAvailable(i):
					usegems2.append(i)
			self.useGems(usegems2)
