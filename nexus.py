import io
from PIL import Image, ImageDraw, ImageFont
import discord
from discord.ext import commands, tasks
import asyncio
import random
import json
import os
from datetime import datetime, timezone, timedelta
from difflib import SequenceMatcher

# --- CONFIG ---
OWNER_ID = 1164907857460871228
GUILD_ID = 1469324805441323099
STAFF_ROLE_ID = 1498948654344572928
STATS_CHANNEL_ID = 1499320972916953168
ALL_KNOWING_ROLE_ID = 1499366742579875910
LOUNGE_IDS = [1499296449521778748, 1499296479427428443, 1499296509961699442, 1499296554236903526, 1499296589460668496, 1499296617680080896]
DB_FILE = "nexus_database.json"

# --- ROTATION SYSTEM ---
GAME_MODES = ["math", "emoji", "lang", "nick", "flags", "colors", "type"]
game_queue = []

# --- CUSTOM EMOJIS ---
E_WIN = "<a:win_1:1499319116300030033>"
E_CLICK = "<a:click_1:1499338069944303677>"
E_INFO = "<a:info_1:1499338148893687938>"
E_STAR = "<a:star_2:1499315733442859008>"

# --- DATA POOLS ---
SENTENCE_POOL = ["The quick brown fox jumps over the lazy dog", "Nexus is the ultimate discord community", "Coding a bot is fun and rewarding", "Speed and accuracy are the keys to victory", "Welcome to the Nexus Lounge area", "Type this sentence as fast as you can"]
EMOJI_POOL = ["😀", "😄", "😁", "😆", "😅", "😂", "🤣", "☺️", "😊", "😇", "🙂", "🙃", "😉", "😌", "😍", "🥰", "😘", "😗", "😙", "😚", "😋", "😛", "😝", "😜", "🤪", "🤨", "🧐", "🤓", "😎", "🤩", "🥳", "😏", "😒", "😞", "😔", "😖", "😫", "😩", "🥺", "😢", "😭", "😤", "😠", "😡", "🤬", "🤯", "😳", "🥵", "🥶", "😱", "😨", "😰", "😥", "😓", "🤗", "🤔", "🤭", "🤫", "😶", "😑", "😬", "🙄", "😯", "🥱", "😴", "🤤", "😪", "😵", "🤐", "🥴", "🤮", "🤧", "😷", "🤒", "🤕", "🐶", "🐼", "🐨", "🐯", "🦁", "🐸", "🐵", "🐒", "🐔", "🐧", "🐦", "🐤", "🐣", "🐥", "🦆", "🦢", "🦉", "🦚", "🦜", "🐺", "🐗", "🐴", "🦄", "🐝", "🐛", "🦋", "🐢", "🐍", "🦎", "🦖", "🦕", "🐙", "🦑", "🦐", "🦞", "🦀", "🐡", "🐠", "🐟", "🐬", "🐳", "🐋", "🦈", "🐊", "🐅", "🐆", "🦓", "🦍", "🐘", "🦛", "🦏", "🐪", "🦒", "🦘", "🐑", "🐐", "🦔", "🐾", "🐉", "🐲"]
FLAG_DATA = {"ar": "argentina", "au": "australia", "at": "austria", "by": "belarus", "be": "belgium", "bo": "bolivia", "br": "brazil", "bg": "bulgaria", "ca": "canada", "cl": "chile", "cn": "china", "co": "colombia", "hr": "croatia", "cu": "cuba", "cy": "cyprus", "cz": "czech republic", "dk": "denmark", "do": "dominican republic", "ec": "ecuador", "eg": "egypt", "ee": "estonia", "et": "ethiopia", "fj": "fiji", "fi": "finland", "fr": "france", "de": "germany", "gh": "ghana", "gr": "greece", "gd": "grenada", "hu": "hungary", "is": "iceland", "in": "india", "id": "indonesia", "ir": "iran", "iq": "iraq", "ie": "ireland", "il": "israel", "it": "italy", "jm": "jamaica", "jp": "japan", "kz": "kazakhstan", "ke": "kenya", "kr": "south korea", "lt": "lithuania", "lu": "luxembourg", "my": "malaysia", "mu": "mauritius", "mx": "mexico", "mn": "mongolia", "ma": "morocco", "np": "nepal", "nl": "netherlands", "nz": "new zealand", "ng": "call nigeria", "no": "norway", "pk": "pakistan", "py": "paraguay", "pe": "peru", "ph": "philippines", "pl": "poland", "pt": "portugal", "qa": "qatar", "ro": "romania", "ru": "russia", "sa": "saudi arabia", "rs": "serbia", "sg": "singapore", "sk": "slovakia", "si": "slovenia", "za": "south africa", "es": "spain", "lk": "sri lanka", "sd": "sudan", "se": "sweden", "ch": "switzerland", "tw": "taiwan", "tz": "tanzania", "th": "thailand", "tr": "turkey", "ua": "ukraine", "ae": "uae", "gb": "uk", "us": "usa", "uy": "uruguay", "ve": "venezuela", "vn": "vietnam", "zw": "zimbabwe"}
LANG_DATA = {"salaam": "persian", "안녕하세요": "korean", "halo": "indonesian", "merhaba": "turkish", "selam": "turkish", "barev dzez": "armenian", "olá": "portuguese", "kumasta": "filipino", "guten tag": "german", "hallo": "german", "halló": "icelandic", "sveiki": "lithuanian", "sat sri akal": "punjabi", "helo": "welsh", "hola": "spanish", "hello": "english", "ahoj": "czech", "witaj": "polish", "sziaztok": "hungarian", "tere": "estonian", "moi": "finnish", "terve": "finnish", "bonjour": "french", "ciao": "italian", "مرحبا": "arabic", "สวัสดี": "thai", "përshëndetje": "albanian", "হ্যালো": "bengali", "hej": "swedish", "xin chao": "vietnamese", "sawasdee": "thai", "dia dhuit": "irish", "kia ora": "maori", "zdravo": "serbian", "jambo": "swahili", "moien": "luxembourgish", "salve": "latin", "здравейте": "bulgarian", "bună": "romanian", "sawubona": "zulu", "sain uu": "mongolian", "shalom": "hebrew", "नमस्ते": "hindi", "γειά σας": "greek", "mingalaba": "burmese", "こんにちは": "japanese", "goedemorgen": "dutch", "yá'at'ééh": "navajo", "здраво": "macedonian", "bok": "croatian", "你好": "chinese", "привет": "russian"}
COLOR_DATA = {"blue and yellow": "green", "yellow and red": "orange", "red and blue": "purple", "blue and purple": "violet", "red and purple": "magenta", "blue and violet": "indigo", "blue and white": "light blue", "green and white": "light green", "orange and white": "peach", "red and white": "pink", "red and pink": "salmon", "blue and black": "dark blue", "red and brown": "maroon", "green and brown": "olive", "green and yellow": "lime", "green and blue": "teal"}

# --- UTILITIES ---
def similarity(a, b): return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def get_time_remaining():
    now = datetime.now(timezone.utc)
    monday = (now + timedelta(days=(7 - now.weekday()) % 7)).replace(hour=0, minute=0, second=0, microsecond=0)
    if monday <= now: monday += timedelta(days=7)
    diff = monday - now
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m remaining"

def create_text_image(text):
    calc_width = max(750, (len(text) * 22) + 100)
    img = Image.new('RGB', (calc_width, 160), color=(43, 45, 49))
    d = ImageDraw.Draw(img)
    try: font = ImageFont.load_default(size=40)
    except: font = ImageFont.load_default()
    d.text((50, 55), text, fill=(255, 255, 255), font=font)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

def load_data():
    defaults = {"all_time": {}, "weekly": {}, "blacklist": [], "lb_msg_id": None, "interval": 10, "start_offset": 0, "last_weekly_winner": "None"}
    if not os.path.exists(DB_FILE): return defaults
    with open(DB_FILE, "r") as f:
        try:
            data = json.load(f)
            for k, v in defaults.items():
                if k not in data: data[k] = v
            return data
        except: return defaults

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

def get_rank(uid, lb_dict):
    sorted_lb = sorted(lb_dict.items(), key=lambda x: x[1], reverse=True)
    for i, (u, _) in enumerate(sorted_lb):
        if str(u) == str(uid): return i + 1
    return len(sorted_lb) + 1

# --- BOT SETUP ---
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)
active_nick_targets = {}

async def update_leaderboard_display():
    data = load_data(); channel = bot.get_channel(STATS_CHANNEL_ID)
    if not channel: return
    
    def format_lb(lb_dict):
        sorted_lb = sorted(lb_dict.items(), key=lambda x: x[1], reverse=True)[:10]
        return "\n".join([f"[{i+1}] <@{u}> - **{s}stars** {E_STAR}" for i, (u, s) in enumerate(sorted_lb)]) or "No data."

    all_time_dict = data.get("all_time", {})
    at_top = max(all_time_dict, key=all_time_dict.get) if all_time_dict else "None"
    wk_top = data.get("last_weekly_winner", "None")
    time_rem = get_time_remaining()

    at_emb = discord.Embed(title="Nexus All-Time Leaderboard", description=f"{format_lb(all_time_dict)}\n\nAll time The All-Knowing - <@{at_top}>", color=0x2ECC71)
    wk_emb = discord.Embed(title="Nexus Weekly Leaderboard", description=f"{format_lb(data.get('weekly', {}))}\n\nCurrent All-Knowing - <@{wk_top}>\n\n({time_rem})", color=0x2ECC71)
    
    try:
        if data.get("lb_msg_id"):
            msg = await channel.fetch_message(data["lb_msg_id"])
            await msg.edit(embeds=[at_emb, wk_emb])
        else: raise Exception
    except:
        new_msg = await channel.send(embeds=[at_emb, wk_emb]); data["lb_msg_id"] = new_msg.id; save_data(data)

async def award_winner(user, channel, mode, trigger_msg=None, update_lb=True):
    data = load_data(); uid = str(user.id)
    if uid in data["blacklist"]: return
    data["all_time"][uid] = data["all_time"].get(uid, 0) + 1
    data["weekly"][uid] = data["weekly"].get(uid, 0) + 1
    save_data(data)
    rank = get_rank(user.id, data["all_time"])
    desc = f"{E_WIN} Rank #{rank}\n{E_INFO} {user.mention} won a star {E_STAR}!\n{E_CLICK} Check the Rankings: <#{STATS_CHANNEL_ID}>"
    emb = discord.Embed(description=desc, color=0x2ECC71)
    if trigger_msg and mode != "nick": await trigger_msg.reply(embed=emb, mention_author=True)
    else: await channel.send(f"{user.mention}", embed=emb)
    
    if update_lb:
        await update_leaderboard_display()

# --- GAME LOGIC ---
async def run_game(channel, mode=None, skip_lb_update=False):
    global game_queue
    if not mode:
        if not game_queue:
            game_queue = GAME_MODES.copy()
            random.shuffle(game_queue)
        mode = game_queue.pop(0)

    now_str = datetime.now().strftime("Today at %I:%M %p")
    embed = discord.Embed(color=0x2ECC71); ans_list, tolerance, file = [], 0, None
    reveal_ans = "" 

    if mode == "type":
        target = random.choice(SENTENCE_POOL); ans_list = [target]
        reveal_ans = target
        embed.title = "⌨️ Typing Game!"; embed.description = "Type the sentence in the image exactly!"
        file = discord.File(create_text_image(target), filename="game.png")
        embed.set_image(url="attachment://game.png"); tolerance = 0 
    elif mode == "emoji":
        target = random.choice(EMOJI_POOL); ans_list = [target]
        reveal_ans = target
        embed.title = "✨ Emoji Game!"; embed.description = f"First to type the emoji '{target}' wins!"
    elif mode == "math":
        op = random.choice(["+", "-", "x", "/"])
        if op == "+": a, b = random.randint(10, 95), random.randint(10, 95); q, ans = f"{a} + {b}", str(a+b)
        elif op == "-": a = random.randint(50, 195); b = random.randint(5, 45); q, ans = f"{a} - {b}", str(a-b)
        elif op == "x": a, b = random.randint(2, 12), random.randint(2, 14); q, ans = f"{a} x {b}", str(a*b)
        else: b = random.randint(2, 10); res = random.randint(2, 15); a = b * res; q, ans = f"{a} / {b}", str(res)
        ans_list = [ans]; reveal_ans = ans; embed.title = "🔢 Solve the problem!!"; embed.description = f"What is **{q}**?"
    elif mode == "flags":
        code, name = random.choice(list(FLAG_DATA.items())); ans_list = [name]
        reveal_ans = name.title()
        embed.title = "🚩 Guess the flag!"; embed.set_image(url=f"https://flagcdn.com/w640/{code}.png"); tolerance = 1
    elif mode == "lang":
        phrase, lang = random.choice(list(LANG_DATA.items())); ans_list = [lang]
        reveal_ans = lang.title()
        embed.title = "🌐 Guess the Language!"; embed.description = f"📝 What language is `{phrase}`?"; tolerance = 1
    elif mode == "colors":
        mix, res = random.choice(list(COLOR_DATA.items())); ans_list = [res.lower()]
        reveal_ans = res.title()
        embed.title = "🎨 Guess the Color!"; embed.description = f"🖍️ What color does **{mix}** make?"
    elif mode == "nick":
        adjectives = ['Tipsy', 'Fluffy', 'Dizzy', 'Zesty', 'Bubbly', 'Funky', 'Rowdy', 'Jelly', 'Sassy', 'Mochi', 'Goofy', 'Sleepy', 'Hyper', 'Lazy', 'Cool', 'Epic', 'Rusty', 'Shiny', 'Tiny', 'Chilly', 'Silly', 'Grumpy', 'Lucky', 'Cranky', 'Jumpy', 'Wobbly', 'Fancy', 'Gloomy', 'Spicy', 'Nutty']
        animals = ['Tiger', 'Puff', 'Dolphin', 'Zebra', 'Bunny', 'Falcon', 'Rhino', 'Shark', 'Monkey', 'Panda', 'Koala', 'Turtle', 'Hamster', 'Lizard', 'Kitten', 'Puppy', 'Otter', 'Eagle', 'Raven', 'Fox']
        target = f"{random.choice(adjectives)}_{random.choice(animals)}"
        reveal_ans = target
        win_event = asyncio.Event()
        active_nick_targets[channel.id] = {"target": target, "event": win_event}
        embed.title = "👤 Nickname Game!"; embed.description = "Change your nickname to match the image!"
        file = discord.File(create_text_image(target), filename="game.png")
        embed.set_image(url="attachment://game.png")

    embed.set_footer(text=f"Earn a star • {now_str}")
    if file: await channel.send(file=file, embed=embed)
    else: await channel.send(embed=embed)

    if mode == "nick":
        try:
            await asyncio.wait_for(active_nick_targets[channel.id]["event"].wait(), timeout=50.0)
        except asyncio.TimeoutError:
            await channel.send(embed=discord.Embed(description=f"{E_INFO} Nobody responded in time. The answer was `{reveal_ans}`", color=0xFF0000))
        finally:
            if channel.id in active_nick_targets: del active_nick_targets[channel.id]
    else:
        def check(m):
            if m.channel != channel or m.author.bot: return False
            content = m.content.strip().lower()
            for invisible in ["\u200d", "\u200b", "\ufeff"]: content = content.replace(invisible, "")
            return any((similarity(content, a.lower()) >= 0.85 if tolerance else content == a.lower()) for a in ans_list)
        try:
            winner_msg = await bot.wait_for("message", timeout=50.0, check=check)
            await award_winner(winner_msg.author, channel, mode, trigger_msg=winner_msg, update_lb=not skip_lb_update)
        except asyncio.TimeoutError:
            await channel.send(embed=discord.Embed(description=f"{E_INFO} Nobody responded in time. The answer was `{reveal_ans}`", color=0xFF0000))

# --- COMMANDS ---
def is_staff():
    async def pred(ctx): return ctx.author.id == OWNER_ID or any(r.id == STAFF_ROLE_ID for r in ctx.author.roles)
    return commands.check(pred)

def is_owner():
    async def pred(ctx): return ctx.author.id == OWNER_ID
    return commands.check(pred)

@bot.command()
async def leaderboard(ctx):
    data = load_data()
    def format_lb(lb_dict):
        sorted_lb = sorted(lb_dict.items(), key=lambda x: x[1], reverse=True)[:10]
        return "\n".join([f"[{i+1}] <@{u}> - **{s}stars** {E_STAR}" for i, (u, s) in enumerate(sorted_lb)]) or "No data."
    at_top = max(data["all_time"], key=data["all_time"].get) if data["all_time"] else "None"
    wk_top = data.get("last_weekly_winner", "None")
    time_rem = get_time_remaining()
    at_emb = discord.Embed(title="Nexus All-Time Leaderboard", description=f"{format_lb(data['all_time'])}\n\nAll time The All-Knowing - <@{at_top}>", color=0x2ECC71)
    wk_emb = discord.Embed(title="Nexus Weekly Leaderboard", description=f"{format_lb(data['weekly'])}\n\nCurrent All-Knowing - <@{wk_top}>\n\n({time_rem})", color=0x2ECC71)
    await ctx.send(embeds=[at_emb, wk_emb])

@bot.command()
@is_staff()
async def game(ctx):
    for cid in LOUNGE_IDS:
        chan = bot.get_channel(cid)
        if chan:
            try:
                await run_game(chan, skip_lb_update=True)
                await asyncio.sleep(1) 
            except Exception as e:
                print(f"Error in channel {cid}: {e}")
    await update_leaderboard_display()

@bot.command()
@is_staff()
async def emoji(ctx): await run_game(ctx.channel, "emoji")

@bot.command()
@is_staff()
async def math(ctx): await run_game(ctx.channel, "math")

@bot.command()
@is_staff()
async def flag(ctx): await run_game(ctx.channel, "flags")

@bot.command()
@is_staff()
async def language(ctx): await run_game(ctx.channel, "lang")

@bot.command()
@is_staff()
async def color(ctx): await run_game(ctx.channel, "colors")

@bot.command()
@is_staff()
async def nick(ctx): await run_game(ctx.channel, "nick")

@bot.command()
@is_staff()
async def type(ctx): await run_game(ctx.channel, "type")

@bot.command()
@is_staff()
async def frequency(ctx, minutes: int):
    data = load_data(); data["interval"] = max(1, minutes); save_data(data)
    await ctx.send(f"✅ Frequency set to **{minutes} minutes**.")

@bot.command()
@is_staff()
async def start_offset(ctx, minute: int):
    data = load_data(); data["start_offset"] = minute % 60; save_data(data)
    await ctx.send(f"✅ Loop offset set to **:{minute:02d}** mark.")

@bot.command()
@is_staff()
async def resetweekly(ctx):
    data = load_data(); data["weekly"] = {}; save_data(data)
    await update_leaderboard_display(); await ctx.send("✅ Weekly leaderboard reset.")

@bot.command()
@is_owner()
async def resetalltime(ctx):
    data = load_data(); data["all_time"] = {}; data["weekly"] = {}
    save_data(data); await update_leaderboard_display(); await ctx.send("🚨 **All-Time and Weekly leaderboards wiped.**")

@bot.command()
@is_staff()
async def setstars(ctx, member: discord.Member, amount: int):
    data = load_data(); data["all_time"][str(member.id)] = amount; save_data(data)
    await update_leaderboard_display(); await ctx.send(f"✅ {member.mention} stars set to {amount}.")

@bot.command()
@is_staff()
async def blacklist(ctx, member: discord.Member):
    data = load_data(); uid = str(member.id)
    if uid in data["blacklist"]: data["blacklist"].remove(uid); msg = "un-blacklisted"
    else: data["blacklist"].append(uid); msg = "blacklisted"
    save_data(data); await ctx.send(f"✅ {member.mention} is now {msg}.")

@bot.command()
async def stars(ctx, member: discord.Member = None):
    data = load_data(); target = member or ctx.author; uid = str(target.id)
    count = data["all_time"].get(uid, 0); rank = get_rank(uid, data["all_time"])
    emb = discord.Embed(title=f"{target.display_name}'s Stars", description=f"{target.mention} have \n {count} stars {E_STAR}", color=0x2ECC71)
    emb.set_thumbnail(url=target.display_avatar.url)
    emb.set_footer(text=f"Rank #{rank} | {datetime.now().strftime('%I:%M %p')}")
    await ctx.send(embed=emb)

# --- TASKS ---
@tasks.loop(minutes=1)
async def automation_loop():
    data = load_data(); now = datetime.now(timezone.utc)
    if now.weekday() == 0 and now.hour == 0 and now.minute == 0:
        if data["weekly"]:
            try:
                winner_id = str(max(data["weekly"], key=data["weekly"].get))
                guild = bot.get_guild(GUILD_ID)
                role = guild.get_role(ALL_KNOWING_ROLE_ID) if guild else None
                if role:
                    for m in role.members: await m.remove_roles(role)
                    win_mem = guild.get_member(int(winner_id))
                    if win_mem: await win_mem.add_roles(role)
                chan = bot.get_channel(STATS_CHANNEL_ID)
                if chan: await chan.send(embed=discord.Embed(title="🏆 Weekly Champion!", description=f"<@{winner_id}> won the week!", color=0x2ECC71))
                data["last_weekly_winner"] = winner_id
            except: pass
            data["weekly"] = {}; save_data(data)
    await update_leaderboard_display()
    if (now.minute - data.get("start_offset", 0)) % data.get("interval", 10) == 0:
        for cid in LOUNGE_IDS:
            chan = bot.get_channel(cid)
            if chan:
                try:
                    await run_game(chan, skip_lb_update=True)
                    await asyncio.sleep(1) 
                except: continue
        await update_leaderboard_display()

@bot.event
async def on_ready():
    if not automation_loop.is_running(): automation_loop.start()
    print(f"Logged in as {bot.user}")

@bot.event
async def on_member_update(before, after):
    for cid, info in list(active_nick_targets.items()):
        if after.display_name == info["target"]:
            chan = bot.get_channel(cid)
            if chan:
                await award_winner(after, chan, "nick")
                info["event"].set()
                if cid in active_nick_targets: del active_nick_targets[cid]

bot.run(os.getenv('DISCORD_TOKEN'))


