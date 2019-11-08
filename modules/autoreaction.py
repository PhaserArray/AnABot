import discord
import asyncio
import logging
import emoji
from discord.ext import commands

class AutoReaction(commands.Cog):
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
			for reaction in self.config[channel.id]["reactions"]:
				reaction_ = await self.get_reaction(reaction, channel.server)
				if reaction_ is None:
					self.logger.warning("Could not load reaction: " + reaction)
				else:
					self.logger.debug("Adding reaction: " + reaction)
				await self.bot.add_reaction(message, reaction_)

	async def get_reaction(self, search, server):
		for reaction in server.emojis:
			if reaction.name == search:
				return reaction
			if reaction.id == search:
				return reaction
		emojized = emoji.emojize(search, use_aliases=True)
		if emojized is not None:
			return "".join(emojized.split())
		return None