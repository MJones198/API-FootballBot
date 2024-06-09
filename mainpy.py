import discord
from discord.ext import commands
import requests

# Define intents
intents = discord.Intents.default()
intents.message_content = True  # Enable the intent for reading message content

# Initialize bot with a command prefix and intents
bot = commands.Bot(command_prefix='^', intents=intents)

# RapidAPI credentials
RAPIDAPI_KEY = "xXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx"
RAPIDAPI_HOST = "api-football-v1.p.rapidapi.com"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')

@bot.command()
async def NF(ctx, *, team_name: str):
    # Step 1: Find Team ID
    team_id_url = "https://api-football-v1.p.rapidapi.com/v3/teams"
    team_querystring = {"search": team_name}
    team_headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    try:
        team_response = requests.get(team_id_url, headers=team_headers, params=team_querystring)
        team_response.raise_for_status()  # Raise an HTTPError for bad responses
        teams = team_response.json()['response']
        if teams:
            team_id = teams[0]['team']['id']  # Assuming the first team in the response is the desired one
        else:
            await ctx.send(f"No team found with the name: {team_name}")
            return
    except requests.exceptions.RequestException as e:
        await ctx.send(f"Failed to retrieve team data: {str(e)}")
        return

    # Step 2: Use Team ID to Find Next Fixture
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"team": team_id, "next": "1"}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        fixtures = response.json()['response']
        if fixtures:
            next_fixture = fixtures[0] 
            fixture_info = (
                f"Fixture Date: {next_fixture['fixture']['date']}\n"
                f"Fixture Status: {next_fixture['fixture']['status']['long']}\n"
                f"Home Team: {next_fixture['teams']['home']['name']}\n"
                f"Away Team: {next_fixture['teams']['away']['name']}"
            )
            await ctx.send(fixture_info)
        else:
            await ctx.send(f"No upcoming fixtures found for the team {team_name}.")
    except requests.exceptions.RequestException as e:
        await ctx.send(f"Failed to retrieve fixture data: {str(e)}")

# SWAP THIS WITH YOUR BOT TOKEN FROM DISCORD
bot.run('xXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx')
