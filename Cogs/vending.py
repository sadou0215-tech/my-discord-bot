from discord.ext import commands

class Vending(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Vending Cog Ready!")

async def setup(bot):
    await bot.add_cog(Vending(bot))
