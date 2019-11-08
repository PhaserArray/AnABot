import discord
import asyncio
import logging
from discord.ext import commands

class Purge(commands.Cog):
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config

		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(bot.logger_level)
		self.logger.addHandler(bot.ch)
		self.logger.addHandler(bot.fh)

		self.logger.debug("Purge module loaded!")

	@commands.command(pass_context=True)
	async def purge(self, ctx, count=None, param=None):

		self.logger.debug(
			"Purging! Channel: {0}, Count: {1}, Param: {2}".format(
				ctx.message.channel.id,
				count,
				param
			)
		)

		if not ctx.message.server.id in self.config:
			return

		await self.bot.delete_message(ctx.message)

		_count = 0
		try:
			_count = int(count)
		except ValueError:
			await self.bot.say(content="❌ **Could not parse count!**",
			delete_after=5)
			return
		except TypeError:
			await self.bot.say(content="❌ **Count not provided!**",
			delete_after=5)
			return
		if _count < 1:
			await self.bot.say(content="❌ **Count must be at least one!**",
			delete_after=5)
			return

		permitted = False
		for role in ctx.message.author.roles:
			if role.id in self.config[ctx.message.server.id]:
				permitted = True
				break
			if role.name in self.config[ctx.message.server.id]:
				permitted = True
				break
		if not permitted:
			await self.bot.say(content="❌ **You are not allowed to use this!**",
			delete_after=5)
			return

		member = None
		if param is not None:
			if param.startswith("<@") and not param.startswith("<@&"):
				user_id = param.strip("<").strip(">").strip("@").strip("!")
				member = ctx.message.server.get_member(user_id)
				if member is None:
					await self.bot.say(content="❌ **Member not found!**",
					delete_after=5)
					return

		def check_func(msg):
			if param is None:
				return True
			if member is not None:
				if msg.author == member:
					return True
			elif str(param).lower() == "preview":
				if len(msg.embeds) != 0 or len(msg.attachments) != 0:
					return True
			else:
				if str(param) in msg.content:
					return True
			return False

		await self.bot.purge_from(ctx.message.channel, 
			limit=_count, 
			check=check_func)

		await self.bot.say(content="✅ **Messages purged!**",
			delete_after=5)