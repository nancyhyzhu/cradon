import os

import discord
from dotenv import load_dotenv

from discord.ext import commands

from gtts import gTTS
import tempfile

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True	# allows use of message content
intents.voice_states = True

client = commands.Bot(command_prefix = '!', intents=intents)

@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.author.name == 'cradon' and message.channel.id == [channel id]:
		#await message.channel.send(f'{message.content}')

		if not discord.utils.get(client.voice_clients, guild=message.guild):
			await message.channel.send('join vc to use')
		else:
			tts = gTTS(text=message.content, lang='en')
			with tempfile.NamedTemporaryFile(delete = False, suffix = '.mp3') as fp:
				tts.save(fp.name)
				fp.seek(0)

			voice_client = discord.utils.get(client.voice_clients, guild=message.guild)
			if voice_client:
				voice_client.play(discord.FFmpegPCMAudio(fp.name), after=lambda e: os.remove(fp.name))
				print('done tts')

@client.event
async def on_voice_state_update(member, before, after):
		if after.channel != None and member.id == [cradon id]: # make specific to cradon
			if not discord.utils.get(client.voice_clients, guild=member.guild):
				await after.channel.connect()
			else:
				print('bot in vc already') 
		
		if before.channel != None and member.id == [cradon id]:
			vc = discord.utils.get(client.voice_clients, guild=member.guild)
			if vc:
				await vc.disconnect()

'''
# event message wont work

# join vc
@client.command()
async def join(ctx):
	if ctx.author.voice:
		channel = ctx.author.voice.channel
		await channel.connect()
		print('joined?')
	else:
		await ctx.send('you need to be in vc')

# leave vc
@client.command()
async def leave(ctx):
	if ctx.voice_client:
		await ctx.voice_client.disconnect()
	else:
		await ctx.send('im not in vc')
'''

client.run(TOKEN)
