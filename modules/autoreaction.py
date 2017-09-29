import discord
import asyncio
import logging
import emoji

class AutoReaction:
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config

		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(bot.logger_level)
		self.logger.addHandler(bot.ch)
		self.logger.addHandler(bot.fh)

		self.logger.debug("AutoReaction module loaded!")

	async def on_message(self, message):
		channel = message.channel
		if channel.id in self.config:
			self.logger.debug("Add reactions!")
			for reaction in self.config[channel.id]["reactions"]:
				reaction_ = await self.get_reaction(reaction, channel.server)
				self.logger.debug(reaction_)
				await self.bot.add_reaction(message, reaction_)

	async def get_reaction(self, search, server):
		if search in emoji.UNICODE_EMOJI:
			return search
		for reaction in server.emojis:
			if reaction.name == search:
				return reaction
			if reaction.id == search:
				return reaction
		return None