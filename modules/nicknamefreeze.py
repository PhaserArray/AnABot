import discord
import asyncio
import logging

class NicknameFreeze:
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config

		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(bot.logger_level)
		self.logger.addHandler(bot.ch)
		self.logger.addHandler(bot.fh)

		# TODO: Make this server specific.
		self.ignore = []

		self.logger.debug("NicknameFreeze module loaded!")

	async def on_member_update(self, before, after):
		if before.nick == after.nick:
			return
		if after.server.id in self.config:
			if self.has_role(after, self.config[after.server.id]):
				if before.id in self.ignore:
					self.ignore.remove(before.id)
					return None
				try:
					self.ignore.append(after.id)
					await self.bot.change_nickname(after, before.nick)
				except (discord.errors.Forbidden):
					self.ignore.remove(after.id)
					self.logger.warning("Could not revert "
										+ str(str(after))
										+ "'s nickname to "
										+ str(before.nick)
										+ " in "
										+ str(after.server)
										+ "!")
				else:
					self.logger.info("Reverted "
									+ str(str(after))
									+ "'s nickname to "
									+ str(before.nick)
									+ " on "
									+ str(after.server)
									+ "!")


	def has_role(self, member, search):
		for role in member.roles:
			if role.id == search:
				return True
			if role.name == search:
				return True
		return False