import sys
import discord
import asyncio
from simplejson import load

class Bot(discord.Client):
	def __init__(self, config):
		self.auth = config["auth"]
		self.auto_role = config["auto_role"]

		super().__init__()

		print("Running bot!")
		self.run(self.auth["token"])

	async def on_ready(self):
		print("Logged in as: " + self.user.name)

	async def on_member_join(self, member):
		server = member.server 
		print("New member: " + member.name)
		if server.id in self.auto_role:
			print("Auto role triggered for: " + server.name)
			await self.add_no_role(member, member.server)

	async def add_no_role(self, member, server):
		_auto_role = self.auto_role[server.id]

		role = _auto_role["role"]
		if not isinstance(role, discord.role.Role):
			print("Getting role!")
			role = await self.get_role(role, server)
			self.auto_role[server.id]["role"] = role
		if role is None:
			print("Role not found!")
			return

		print("Adding roles!")
		await self.add_roles(member, role)

		if "message" in _auto_role:
			message = _auto_role["message"].format(member.mention)

			print("Sending welcome message!")
			try:
				await self.send_message(member, content=message)
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