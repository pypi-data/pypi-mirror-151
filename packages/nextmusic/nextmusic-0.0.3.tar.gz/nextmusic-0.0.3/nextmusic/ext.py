import discord
from discord.ext import commands
import psutil, pstats


class Intents:
    intents = discord.Intents.default()
    intents.members = True

class Commands(commands.Cog):
    """Music commands"""

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.bot.remove_command('help')
    def invite_link(self):
            invite_link = ''
            try:
                invite_link = self.bot.invite_link
            except:
                invite_link = 'https://araki.social'

            return invite_link
    def support_server(self):
        support_server = ''
        try:
            support_server = self.bot.support_server
        except:
            support_server = 'https://araki.social/support'

        return support_server

    def embed_colour(self):
        clr = None
        try:
           clr = self.bot.embed_colour
        except:
           clr = 0x303236

        return clr


    @commands.command(name='help')
    async def _help(self, ctx: commands.Context):
        embed = discord.Embed(
            description=self.bot.description,
            colour=self.embed_colour()
        )
        embed.set_author(name='Help Panel')
        embed.add_field(name='Music Command', value='```join```, ```play```, ```play spotify```, ```play youtube```, ```play soundcloud```, ```volume```, ```stop```, ```pause```, ```resume```, ```skip```, ```seek```, ```loop```, ```queue```', inline=False)
        embed.add_field(name='Utility Command', value='```ping```, ```stats```, ```info```, ```invite```, ```support```',inline=False)
        embed.add_field(name='Links', value=f'[Invite]({self.invite_link()}) • [Support server]({self.support_server()}) • [Nextmusic](https://araki.social/support)', inline=False)
        embed.set_footer(text='Powered by Nextmusic')
        await ctx.send(embed=embed)

    @commands.command(name='ping')
    async def _ping(self, ctx: commands.Context):
        ping = round(self.bot.latency * 1000)
        embed = discord.Embed(
            description=f'My ping - {ping}',
            colour=self.embed_colour()
        )
        embed.set_author(name='Bot ping')
        await ctx.send(embed=embed)
    @commands.command(name='stats')
    async def _stats(self, ctx:commands.Context):
        embed = discord.Embed(colour=self.embed_colour())
        embed.add_field(name="Total server", value=f"{len(self.bot.guilds)}", inline=False)
        embed.add_field(name="Total users", value=f"{len(self.bot.users)}", inline=False)
        embed.add_field(name="Memory usages", value=f"{psutil.virtual_memory().percent}mb", inline=False)
        embed.add_field(name="Cpu usages", value=f"{psutil.cpu_percent()}%", inline=False)
        embed.set_author(name='Bot Stats')
        embed.set_footer(text='Powered by nextmusic')
        await ctx.send(embed=embed)

    @commands.command(aliases=['inv', 'support', 'invite'])
    async def _invite(self, ctx: commands.Context):
        embed = discord.Embed(description=f'[Click here to invite me]({self.invite_link()})\n[Click here to join support serer]({self.invite_link()})', colour=self.embed_colour())
        embed.set_author(name='Links')
        await ctx.send(embed=embed)