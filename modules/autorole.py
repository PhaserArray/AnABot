import discord
import asyncio
import logging
from discord.ext import commands

class AutoRole(commands.Cog):
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config

		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(bot.logger_level)
		self.logger.addHandler(bot.ch)
		self.logger.addHandler(bot.fh)

		self.logger.debug("AutoRole module loaded!")

	async def on_member_join(self, member):
		server = member.server 
		self.logger.info("{0} has joined {1}!".format(member, member.server))
		if server.id in self.config:
			self.logger.debug("Auto role triggered!") 
			await self.add_no_role(member, member.server)

	async def add_no_role(self, member, server):
		_auto_role = self.config[server.id]

		if "role" not in _auto_role:
			return
		role = _auto_role["role"]

		if not isinstance(role, discord.role.Role):
			self.logger.debug("Getting role!")
			role = await self.get_role(role, server)
			self.config[server.id]["role"] = role
		if role is None:
			self.logger.debug("Role not found!")
			return

		self.logger.debug("Adding roles!")
		await self.bot.add_roles(member, role)

		if "message" in _auto_role:
			message = _auto_role["message"].format(member.mention)

			self.logger.debug("Sending welcome message!")
			try:
				await self.bot.send_message(member, content=message)
			except discord.errors.Forbidden:
				pass

	async def get_role(self, search, server):
		roles = server.role_hierarchy
		best_match = None
		for role in roles:
			if search == role.id:
				return role
			elif search == role.name:
				best_match = role
		return best_match