import sys
import logging
import discord
import asyncio
import modules
import importlib
from simplejson import load
from discord.ext import commands
from logging.handlers import RotatingFileHandler 

class Bot(commands.Bot):
	def __init__(self, config):
		self.logger_level = logging.INFO
		self._make_logger()
		self.logger.info("Loading bot!")

		super().__init__(config["bot"]["prefix"])
		self._load_modules(config["modules"])

		self.logger.info("Running bot!")
		self.run(config["bot"]["auth"]["token"])

	def _make_logger(self):
		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(self.logger_level)

		self.formatter = logging.Formatter(
			"%(asctime)s - %(name)s - [%(levelname)s] - %(message)s")

		self.ch = logging.StreamHandler()
		self.ch.setLevel(self.logger_level)
		self.ch.setFormatter(self.formatter)
		self.logger.addHandler(self.ch)

		self.fh = RotatingFileHandler('bot.log', maxBytes=50000000)
		self.fh.setLevel(self.logger_level)
		self.fh.setFormatter(self.formatter)
		self.logger.addHandler(self.fh)

	def _load_modules(self, modules):
		count = 0
		for name, config in modules.items():
			module = importlib.import_module(
				"." + name.lower(), 
				package="modules")
			self.add_cog(getattr(module, name)(self, config))
			count += 1
		self.logger.info("Loaded {0} modules!".format(count))

	async def on_ready(self):
		self.logger.info("Logged in as: " + self.user.name)

def load_config(path):
	with open(path) as config_file:
		return load(config_file)

def main():
	path = "config.json"
	if len(sys.argv) > 1:
		path = sys.argv[1]
	config = load_config(path)
	bot = Bot(config)

if __name__ == '__main__':
	main()