import asyncio, json
from asyncio.windows_events import SelectorEventLoop
from discord.ext import commands
from serverclass import MinecraftServer

# Copyright(C) 2021 Bogdan Ungureanu
# This script makes playing minecraft with your friends easier.
# You can command the minecraft server from the discord server, but only the allowed commands you configured in config.json
# The names in allowed-names must be lowercase in order to work
# The roles in allowed-roles are case-sensitive


with open("config.json", "r") as f:
    config_dic = json.load(f)

bot = commands.Bot(command_prefix=".")
server = MinecraftServer(
    config_dic["server-path"],
    config_dic["ram"]["min-ram"],
    config_dic["ram"]["max-ram"],
)


@bot.event
async def on_ready():
    print(20 * "=" + "\n#Bot is ready\n" + 20 * "=")


def isallowed():
    # check if a user is allowed to execute the command, else send a message
    # check allowed-names in config.json (it can contain the display name or the accout name of the user but it must be all LOWER CASE)
    async def predicate(ctx):

        if ctx.author.display_name.lower() in [
            e.lower() for e in config_dic["allowed-names"]
        ] or ctx.author.name.lower() in [
            e.lower() for e in config_dic["allowed-names"]
        ]:
            return True

        for role in config_dic["allowed-roles"]:
            if role in ctx.author.roles:
                return True
        else:
            await ctx.channel.send("`You do not have permission to do that.`")
            return False

    return commands.check(predicate)


@isallowed()
@commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
@bot.command(name="play-minecraft", aliases=config_dic["command-aliases"])
async def mainMinecraft(ctx):
    chan = ctx.message.channel
    msg = ctx.message.content.split()
    comanda = msg[1]
    args = " ".join(msg[2:])

    if comanda == "start":
        print(40 * "=" + "\n#Starting Minecraft Server...\n" + 40 * "=")
        return await chan.send(f"```{server.start()}```")

    elif comanda == "stop":
        print(40 * "=" + "\n#Stopping Minecraft Server...\n" + 40 * "=")
        return await chan.send(f"```{server.command(comanda)}```")

    elif comanda == "status":
        print(40 * "=" + "\n#Printing Minecraft Server Status...\n" + 40 * "=")
        return await chan.send(f"```{server.status()}```")

    elif comanda == "ip":
        print(40 * "=" + "\n#Printing the IP of Minecraft server...\n" + 40 * "=")
        return await chan.send(
            f"```This is the Minecraft Server IP : {server.ip()}:25565```"
        )

    elif comanda in config_dic["valid-commands"]:
        resp = server.command(comanda, args)
        await chan.send(f"`Result of command: `")

        if len(resp) > 1:
            for i in range(0, len(resp), 10):  # print 10 lines max in a single message
                msg = "".join(resp[i : i + 10])
                await chan.send(f"```{msg}```")
        else:
            await chan.send(f"```{resp[0]}```")

        return
    else:
        al = ", ".join(config_dic["command-aliases"])
        cds = ", ".join(config_dic["valid-commands"])
        return await chan.send(
            f"`Invalid syntax. Usage: \nex: (BotCommand) (MinecraftServerCommand) (Args) ({al})  +  ({cds}) + (args)`"
        )


bot.run(config_dic["bot-token"])
