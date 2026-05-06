from flask import Flask
from threading import Thread
import os
import io
from PIL import Image, ImageDraw, ImageFont
import discord
from discord.ext import commands, tasks
import asyncio
import random
import json
from datetime import datetime, timezone, timedelta
from difflib import SequenceMatcher

app = Flask('')

@app.route('/')
def home():
    return "Nexus Bot is Online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
    
# --- CONFIG ---
OWNER_ID = 1164907857460871228
GUILD_ID = 1469324805441323099
STAFF_ROLE_ID = 1498948654344572928
STATS_CHANNEL_ID = 1499320972916953168
ALL_KNOWING_ROLE_ID = 1499366742579875910
LOUNGE_IDS = [1499296449521778748, 1499296479427428443, 1499296509961699442, 1499296554236903526, 1499296589460668496, 1499296617680080896]
DB_FILE = "nexus_database.json"
LOGODEV_KEY = 'pk_C_LL72tpRECKbvE0bhJ_MA'

# --- ROTATION SYSTEM ---
# Added "logo" to the rotation
GAME_MODES = ["math", "emoji", "lang", "nick", "flags", "colors", "type", "capital", "logo"]
game_queue = []

# --- CUSTOM EMOJIS ---
E_WIN = "<a:win_1:1499319116300030033>"
E_CLICK = "<a:click_1:1499338069944303677>"
E_INFO = "<a:info_1:1499338148893687938>"
E_STAR = "<a:star_2:1499315733442859008>"

# --- DATA POOLS ---
SENTENCE_POOL = ["The quick brown fox jumps over the lazy dog", "Nexus is the ultimate discord community", "Coding a bot is fun and rewarding", "Speed and accuracy are the keys to victory", "Welcome to the Nexus Lounge area", "Type this sentence as fast as you can", "Zeri is the most emo person here", "Zeri likes femboys the most"]
EMOJI_POOL = ["😀", "😄", "😁", "😆", "😅", "😂", "🤣", "☺️", "😊", "😇", "🙂", "🙃", "😉", "😌", "😍", "🥰", "😘", "😗", "😙", "😚", "😋", "😛", "😝", "😜", "🤪", "🤨", "🧐", "🤓", "😎", "🤩", "🥳", "😏", "😒", "😞", "😔", "😖", "😫", "😩", "🥺", "😢", "😭", "😤", "😠", "😡", "🤬", "🤯", "😳", "🥵", "🥶", "😱", "😨", "😰", "😥", "😓", "🤗", "🤔", "🤭", "🤫", "😶", "😑", "😬", "🙄", "😯", "🥱", "😴", "🤤", "😪", "😵", "🤐", "🥴", "🤮", "🤧", "😷", "🤒", "🤕", "🐶", "🐼", "🐨", "🐯", "🦁", "🐸", "🐵", "🐒", "🐔", "🐧", "🐦", "🐤", "🐣", "🐥", "🦆", "🦢", "🦉", "🦚", "🦜", "🐺", "🐗", "🐴", "🦄", "🐝", "🐛", "🦋", "🐢", "🐍", "🦎", "🦖", "🦕", "🐙", "🦑", "🦐", "🦞", "🦀", "🐡", "🐠", "🐟", "🐬", "🐳", "🐋", "🦈", "🐊", "🐅", "🐆", "🦓", "🦍", "🐘", "🦛", "🦏", "🐪", "🦒", "🦘", "🐑", "🐐", "🦔", "🐾", "🐉", "🐲"]
FLAG_DATA = {"ar": "argentina", "au": "australia", "at": "austria", "by": "belarus", "be": "belgium", "bo": "bolivia", "br": "brazil", "bg": "bulgaria", "ca": "canada", "cl": "chile", "cn": "china", "co": "colombia", "hr": "croatia", "cu": "cuba", "cy": "cyprus", "cz": "czech republic", "dk": "denmark", "do": "dominican republic", "ec": "ecuador", "eg": "egypt", "ee": "estonia", "et": "ethiopia", "fj": "fiji", "fi": "finland", "fr": "france", "de": "germany", "gh": "ghana", "gr": "greece", "gd": "grenada", "hu": "hungary", "is": "iceland", "in": "india", "id": "indonesia", "ir": "iran", "iq": "iraq", "ie": "ireland", "il": "israel", "it": "italy", "jm": "jamaica", "jp": "japan", "kz": "kazakhstan", "ke": "kenya", "kr": "south korea", "lt": "lithuania", "lu": "luxembourg", "my": "malaysia", "mu": "mauritius", "mx": "mexico", "mn": "mongolia", "ma": "morocco", "np": "nepal", "nl": "netherlands", "nz": "new zealand", "ng": "nigeria", "no": "norway", "pk": "pakistan", "py": "paraguay", "pe": "peru", "ph": "philippines", "pl": "poland", "pt": "portugal", "qa": "qatar", "ro": "romania", "ru": "russia", "sa": "saudi arabia", "rs": "serbia", "sg": "singapore", "sk": "slovakia", "si": "slovenia", "za": "south africa", "es": "spain", "lk": "sri lanka", "sd": "sudan", "se": "sweden", "ch": "switzerland", "tw": "taiwan", "tz": "tanzania", "th": "thailand", "tr": "turkey", "ua": "ukraine", "ae": "uae", "gb": "uk", "us": "usa", "uy": "uruguay", "ve": "venezuela", "vn": "vietnam", "zw": "zimbabwe"}
LANG_DATA = {"salaam": "persian", "안녕하세요": "korean", "halo": "indonesian", "merhaba": "turkish", "selam": "turkish", "barev dzez": "armenian", "olá": "portuguese", "kumasta": "filipino", "guten tag": "german", "hallo": "german", "halló": "icelandic", "sveiki": "lithuanian", "sat sri akal": "punjabi", "helo": "welsh", "hola": "spanish", "hello": "english", "ahoj": "czech", "witaj": "polish", "sziaztok": "hungarian", "tere": "estonian", "moi": "finnish", "terve": "finnish", "bonjour": "french", "ciao": "italian", "مرحبا": "arabic", "สวัสดี": "thai", "përshëndetje": "albanian", "হ্যালো": "bengali", "hej": "swedish", "xin chao": "vietnamese", "sawasdee": "thai", "dia dhuit": "irish", "kia ora": "maori", "zdravo": "serbian", "jambo": "swahili", "moien": "luxembourgish", "salve": "latin", "здравейте": "bulgarian", "bună": "romanian", "sawubona": "zulu", "sain uu": "mongolian", "shalom": "hebrew", "नमस्ते": "hindi", "γειά σας": "greek", "mingalaba": "burmese", "こんにちは": "japanese", "goedemorgen": "dutch", "yá'at'ééh": "navajo", "здраво": "macedonian", "bok": "croatian", "你好": "chinese", "привет": "russian"}
COLOR_DATA = {"blue and yellow": "green", "yellow and red": "orange", "red and blue": "purple", "blue and purple": "violet", "red and purple": "magenta", "blue and violet": "indigo", "blue and white": "light blue", "green and white": "light green", "orange and white": "peach", "red and white": "pink", "red and pink": "salmon", "blue and black": "dark blue", "red and brown": "maroon", "green and brown": "olive", "green and yellow": "lime", "green and blue": "teal"}

LOGO_DATA = [
    {"name": "Google", "domain": "google.com"}, {"name": "Discord", "domain": "discord.com"},
    {"name": "Microsoft", "domain": "microsoft.com"}, {"name": "Apple", "domain": "apple.com"},
    {"name": "Amazon", "domain": "amazon.com"}, {"name": "Meta", "domain": "facebook.com"},
    {"name": "Instagram", "domain": "instagram.com"}, {"name": "YouTube", "domain": "youtube.com"},
    {"name": "Netflix", "domain": "netflix.com"}, {"name": "Spotify", "domain": "spotify.com"},
    {"name": "TikTok", "domain": "tiktok.com"}, {"name": "Twitter", "domain": "twitter.com"},
    {"name": "WhatsApp", "domain": "whatsapp.com"}, {"name": "GitHub", "domain": "github.com"},
    {"name": "Samsung", "domain": "samsung.com"}, {"name": "Xiaomi", "domain": "mi.com"},
    {"name": "OnePlus", "domain": "oneplus.com"}, {"name": "Nvidia", "domain": "nvidia.com"},
    {"name": "Intel", "domain": "intel.com"}, {"name": "Razer", "domain": "razer.com"},
    {"name": "Logitech", "domain": "logitech.com"}, {"name": "AMD", "domain": "amd.com"},
    {"name": "Steam", "domain": "steampowered.com"}, {"name": "Android", "domain": "android.com"},
    {"name": "McLaren", "domain": "mclaren.com"}, {"name": "Ferrari", "domain": "ferrari.com"},
    {"name": "Lamborghini", "domain": "lamborghini.com"}, {"name": "Porsche", "domain": "porsche.com"},
    {"name": "Tesla", "domain": "tesla.com"}, {"name": "BMW", "domain": "bmw.com"},
    {"name": "Mercedes-Benz", "domain": "mercedes-benz.com"}, {"name": "Audi", "domain": "audi.com"},
    {"name": "Toyota", "domain": "toyota.com"}, {"name": "Honda", "domain": "honda.com"},
    {"name": "Ford", "domain": "ford.com"}, {"name": "Hyundai", "domain": "hyundai.com"},
    {"name": "Volkswagen", "domain": "vw.com"}, {"name": "Bentley", "domain": "bentleymotors.com"},
    {"name": "Jaguar", "domain": "jaguar.com"}, {"name": "Volvo", "domain": "volvocars.com"},
    {"name": "McDonald's", "domain": "mcdonalds.com"}, {"name": "Starbucks", "domain": "starbucks.com"},
    {"name": "KFC", "domain": "kfc.com"}, {"name": "Burger King", "domain": "burgerking.com"},
    {"name": "Coca-Cola", "domain": "cocacola.com"}, {"name": "Pepsi", "domain": "pepsi.com"},
    {"name": "Red Bull", "domain": "redbull.com"}, {"name": "Monster Energy", "domain": "monsterenergy.com"},
    {"name": "Oreo", "domain": "oreo.com"}, {"name": "Pringles", "domain": "pringles.com"},
    {"name": "Nike", "domain": "nike.com"}, {"name": "Adidas", "domain": "adidas.com"},
    {"name": "Puma", "domain": "puma.com"}, {"name": "Rolex", "domain": "rolex.com"},
    {"name": "Gucci", "domain": "gucci.com"}, {"name": "Louis Vuitton", "domain": "louisvuitton.com"},
    {"name": "Chanel", "domain": "chanel.com"}, {"name": "Prada", "domain": "prada.com"},
    {"name": "Versace", "domain": "versace.com"}, {"name": "Cartier", "domain": "cartier.com"},
    {"name": "Supreme", "domain": "supreme.com"}, {"name": "Patagonia", "domain": "patagonia.com"},
    {"name": "Harvard", "domain": "harvard.edu"}, {"name": "Stanford", "domain": "stanford.edu"},
    {"name": "MIT", "domain": "mit.edu"}, {"name": "National Geographic", "domain": "nationalgeographic.com"},
    {"name": "Bluetooth", "domain": "bluetooth.com"}, {"name": "Yamaha", "domain": "yamaha.com"},
    {"name": "Cisco", "domain": "cisco.com"}, {"name": "Unilever", "domain": "unilever.com"},
    {"name": "Shell", "domain": "shell.com"}, {"name": "BP", "domain": "bp.com"},
    {"name": "Visa", "domain": "visa.com"}, {"name": "PayPal", "domain": "paypal.com"},
    {"name": "Mastercard", "domain": "mastercard.com"}, {"name": "Slack", "domain": "slack.com"},
    {"name": "Twitch", "domain": "twitch.tv"}, {"name": "Linux", "domain": "kernel.org"}
]

CAPITAL_POOL = [
    {"name": "Argentina", "capital": "Buenos Aires", "code": "ar"}, {"name": "Australia", "capital": "Canberra", "code": "au"},
    {"name": "Austria", "capital": "Vienna", "code": "at"}, {"name": "Belarus", "capital": "Minsk", "code": "by"},
    {"name": "Belgium", "capital": "Brussels", "code": "be"}, {"name": "Bolivia", "capital": "Sucre", "code": "bo"},
    {"name": "Brazil", "capital": "Brasilia", "code": "br"}, {"name": "Bulgaria", "capital": "Sofia", "code": "bg"},
    {"name": "Canada", "capital": "Ottawa", "code": "ca"}, {"name": "Chile", "capital": "Santiago", "code": "cl"},
    {"name": "China", "capital": "Beijing", "code": "cn"}, {"name": "Colombia", "capital": "Bogotá", "code": "co"},
    {"name": "Croatia", "capital": "Zagreb", "code": "hr"}, {"name": "Cuba", "capital": "Havana", "code": "cu"},
    {"name": "Cyprus", "capital": "Nicosia", "code": "cy"}, {"name": "Czechia", "capital": "Prague", "code": "cz"},
    {"name": "Denmark", "capital": "Copenhagen", "code": "dk"}, {"name": "Dominican Republic", "capital": "Santo Domingo", "code": "do"},
    {"name": "Ecuador", "capital": "Quito", "code": "ec"}, {"name": "Egypt", "capital": "Cairo", "code": "eg"},
    {"name": "Estonia", "capital": "Tallinn", "code": "ee"}, {"name": "Ethiopia", "capital": "Addis Ababa", "code": "et"},
    {"name": "Fiji", "capital": "Suva", "code": "fj"}, {"name": "Finland", "capital": "Helsinki", "code": "fi"},
    {"name": "France", "capital": "Paris", "code": "fr"}, {"name": "Germany", "capital": "Berlin", "code": "de"},
    {"name": "Ghana", "capital": "Accra", "code": "gh"}, {"name": "Greece", "capital": "Athens", "code": "gr"},
    {"name": "Grenada", "capital": "St. George's", "code": "gd"}, {"name": "Hungary", "capital": "Budapest", "code": "hu"},
    {"name": "Iceland", "capital": "Reykjavík", "code": "is"}, {"name": "India", "capital": "New Delhi", "code": "in"},
    {"name": "Indonesia", "capital": "Jakarta", "code": "id"}, {"name": "Iran", "capital": "Tehran", "code": "ir"},
    {"name": "Iraq", "capital": "Baghdad", "code": "iq"}, {"name": "Ireland", "capital": "Dublin", "code": "ie"},
    {"name": "Israel", "capital": "Jerusalem", "code": "il"}, {"name": "Italy", "capital": "Rome", "code": "it"},
    {"name": "Jamaica", "capital": "Kingston", "code": "jm"}, {"name": "Japan", "capital": "Tokyo", "code": "jp"},
    {"name": "Kazakhstan", "capital": "Astana", "code": "kz"}, {"name": "Kenya", "capital": "Nairobi", "code": "ke"},
    {"name": "South Korea", "capital": "Seoul", "code": "kr"}, {"name": "Lithuania", "capital": "Vilnius", "code": "lt"},
    {"name": "Luxembourg", "capital": "Luxembourg City", "code": "lu"}, {"name": "Malaysia", "capital": "Kuala Lumpur", "code": "my"},
    {"name": "Mauritius", "capital": "Port Louis", "code": "mu"}, {"name": "Mexico", "capital": "Mexico City", "code": "mx"},
    {"name": "Mongolia", "capital": "Ulaanbaatar", "code": "mn"}, {"name": "Morocco", "capital": "Rabat", "code": "ma"},
    {"name": "Nepal", "capital": "Kathmandu", "code": "np"}, {"name": "Netherlands", "capital": "Amsterdam", "code": "nl"},
    {"name": "New Zealand", "capital": "Wellington", "code": "nz"}, {"name": "Nigeria", "capital": "Abuja", "code": "ng"},
    {"name": "Norway", "capital": "Oslo", "code": "no"}, {"name": "Pakistan", "capital": "Islamabad", "code": "pk"},
    {"name": "Paraguay", "capital": "Asunción", "code": "py"}, {"name": "Peru", "capital": "Lima", "code": "pe"},
    {"name": "Philippines", "capital": "Manila", "code": "ph"}, {"name": "Poland", "capital": "Warsaw", "code": "pl"},
    {"name": "Portugal", "capital": "Lisbon", "code": "pt"}, {"name": "Qatar", "capital": "Doha", "code": "qa"},
    {"name": "Romania", "capital": "Bucharest", "code": "ro"}, {"name": "Russia", "capital": "Moscow", "code": "ru"},
    {"name": "Saudi Arabia", "capital": "Riyadh", "code": "sa"}, {"name": "Serbia", "capital": "Belgrade", "code": "rs"},
    {"name": "Singapore", "capital": "Singapore", "code": "sg"}, {"name": "Slovakia", "capital": "Bratislava", "code": "sk"},
    {"name": "Slovenia", "capital": "Ljubljana", "code": "si"}, {"name": "South Africa", "capital": "Pretoria", "code": "za"},
    {"name": "Spain", "capital": "Madrid", "code": "es"}, {"name": "Sri Lanka", "capital": "Kotte", "code": "lk"},
    {"name": "Sudan", "capital": "Khartoum", "code": "sd"}, {"name": "Sweden", "capital": "Stockholm", "code": "se"},
    {"name": "Switzerland", "capital": "Bern", "code": "ch"}, {"name": "Taiwan", "capital": "Taipei", "code": "tw"},
    {"name": "Tanzania", "capital": "Dodoma", "code": "tz"}, {"name": "Thailand", "capital": "Bangkok", "code": "th"},
    {"name": "Turkey", "capital": "Ankara", "code": "tr"}, {"name": "Ukraine", "capital": "Kyiv", "code": "ua"},
    {"name": "UAE", "capital": "Abu Dhabi", "code": "ae"}, {"name": "United Kingdom", "capital": "London", "code": "gb"},
    {"name": "USA", "capital": "Washington D.C.", "code": "us"}, {"name": "Uruguay", "capital": "Montevideo", "code": "uy"},
    {"name": "Venezuela", "capital": "Caracas", "code": "ve"}, {"name": "Vietnam", "capital": "Hanoi", "code": "vn"},
    {"name": "Zimbabwe", "capital": "Harare", "code": "zw"}
]

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
    
    if trigger_msg and mode not in ["nick", "capital"]:
        await trigger_msg.reply(embed=emb, mention_author=True)
    elif mode == "capital":
        await channel.send(embed=emb, reference=trigger_msg)
    else:
        await channel.send(f"{user.mention}", embed=emb)
    
    if update_lb:
        await update_leaderboard_display()

# --- CAPITAL QUIZ VIEW ---
class FlagQuizView(discord.ui.View):
    def __init__(self, correct_capital, options, channel):
        super().__init__(timeout=50.0)
        self.correct_capital = correct_capital
        self.options = options
        self.channel = channel
        self.winner = None
        self.attempted_users = set()

        for option in options:
            btn = discord.ui.Button(label=option, style=discord.ButtonStyle.secondary)
            btn.callback = self.make_callback(option)
            self.add_item(btn)

    def make_callback(self, option):
        async def callback(interaction: discord.Interaction):
            if self.winner: return
            if interaction.user.id in self.attempted_users:
                await interaction.response.send_message("Only one try allowed!", ephemeral=True)
                return
            self.attempted_users.add(interaction.user.id)
            if option == self.correct_capital:
                self.winner = interaction.user
                for child in self.children:
                    child.disabled = True
                    if child.label == self.correct_capital: child.style = discord.ButtonStyle.success
                await interaction.response.edit_message(view=self)
                await award_winner(interaction.user, self.channel, "capital", trigger_msg=interaction.message)
                self.stop()
            else:
                await interaction.response.send_message("❌ Wrong!", ephemeral=True)
        return callback

    async def on_timeout(self):
        for child in self.children: child.disabled = True

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
    elif mode == "logo":
        brand_name, brand_domain = random.choice(list(LOGO_DATA.items()))
        ans_list = [brand_name]
        reveal_ans = brand_name
        embed.title = " Guess the Logo!"
        embed.set_image(url=f"https://img.logo.dev/{brand_domain}?token={LOGODEV_KEY}")
        
        # ADD THIS LINE HERE
        tolerance = 1 
        
    elif mode == "capital":
        target = random.choice(CAPITAL_POOL)
        correct_cap = target['capital']
        wrong_options = random.sample([c['capital'] for c in CAPITAL_POOL if c['capital'] != correct_cap], 3)
        options = wrong_options + [correct_cap]
        random.shuffle(options)
        embed.title = "What is the capital of this country?"
        embed.set_image(url=f"https://flagcdn.com/w320/{target['code']}.png")
        view = FlagQuizView(correct_cap, options, channel)
        msg = await channel.send(embed=embed, view=view)
        async def handle_timeout():
            await asyncio.sleep(50.0)
            if not view.winner:
                for child in view.children: child.disabled = True
                try: await msg.edit(view=view)
                except: pass
        asyncio.create_task(handle_timeout()); await asyncio.sleep(4.0); return 
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

     # Handle the game listening/timing in a background task
async def game_handler():
        # This allows the background task to see the variables defined above
        nonlocal ans_list, tolerance, reveal_ans 

        if mode == "nick":
            try:
                await asyncio.wait_for(active_nick_targets[channel.id]["event"].wait(), timeout=50.0)
            except asyncio.TimeoutError:
                await channel.send(embed=discord.Embed(description=f"{E_INFO} Nobody responded in time. The answer was `{reveal_ans}`", color=0xFF0000))
            finally:
                if channel.id in active_nick_targets: del active_nick_targets[channel.id]
        else:
            def check(m):
                if m.channel.id != channel.id or m.author.bot: return False
                content = m.content.strip().lower()
                for inv in ["\u200d", "\u200b", "\ufeff"]: content = content.replace(inv, "")
                
                # Verify that ans_list isn't empty before checking
                if not ans_list: return False
                return any((similarity(content, a.lower()) >= 0.85 if tolerance else content == a.lower()) for a in ans_list)

            try:
                winner_msg = await bot.wait_for("message", timeout=50.0, check=check)
                await award_winner(winner_msg.author, channel, mode, trigger_msg=winner_msg, update_lb=not skip_lb_update)
            except asyncio.TimeoutError:
                if reveal_ans:
                    await channel.send(embed=discord.Embed(description=f"{E_INFO} Nobody responded in time. The answer was `{reveal_ans}`", color=0xFF0000))

    # Trigger the background listener
    asyncio.create_task(game_handler())
    
    # The 4s Universal Cascade
    await asyncio.sleep(4.0)
    return
    
    
    
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
            try: await run_game(chan, skip_lb_update=True); await asyncio.sleep(1) 
            except: continue
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
async def capital(ctx): await run_game(ctx.channel, "capital")
@bot.command()
@is_staff()
async def logo(ctx): await run_game(ctx.channel, "logo")

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
                try: await run_game(chan, skip_lb_update=True); await asyncio.sleep(1) 
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

keep_alive()
bot.run(os.getenv('DISCORD_TOKEN'))
