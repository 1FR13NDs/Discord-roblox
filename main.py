import discord
from discord.ext import commands
import asyncio
from config import TOKEN, CHANNEL_ID, AUTHORIZED_USERS, MAX_ACCOUNTS_TO_SEND, ACCOUNTS_FILE, VIP_USERS, VIP_ACCOUNTS_FILE

# Intents ayarlarını belirleyin
intents = discord.Intents.all()
intents.members = True  # Kullanıcıların sunucu üyeleri hakkında bilgiye erişebilmesi için

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} ismiyle giriş yapıldı.")
    await bot.change_presence(activity=discord.Game(name=f"{count_accounts()} Hesap"))

@bot.command()
async def olustur(ctx, count: int = 1):
    if ctx.channel.id != CHANNEL_ID or ctx.author.id not in AUTHORIZED_USERS:
        await ctx.send("Bu komutu kullanma izniniz yok.")
        return

    if count <= 0:
        await ctx.send("Geçerli bir hesap sayısı belirtmelisiniz.")
        return

    accounts = load_accounts(count)
    
    if not accounts:
        await ctx.send("Hesap bulunamadı.")  # Hesaplar yoksa hata mesajı ver
        return
    
    for account in accounts:
        await ctx.author.send(account)
        await asyncio.sleep(1)  # Gönderilen hesaplar arasında bir saniye bekleyin

    await ctx.send(f"{count} hesap gönderildi.")


def load_accounts(count):
    try:
        with open(ACCOUNTS_FILE, "r") as file:
            lines = file.readlines()
            accounts = [line.strip() for line in lines[:count]]
            lines = lines[count:]
        
        with open(ACCOUNTS_FILE, "w") as file:
            file.writelines(lines)

        return accounts
    except Exception as e:
        print(f"Hesaplar yüklenirken bir hata oluştu: {str(e)}")
        return []

def count_accounts():
    try:
        with open(ACCOUNTS_FILE, "r") as file:
            return len(file.readlines())
    except Exception as e:
        print(f"Hesaplar sayılırken bir hata oluştu: {str(e)}")
        return 0

@bot.command()
async def vip(ctx):
    if ctx.author.id not in VIP_USERS:
        await ctx.send("Bu komutu kullanma izniniz yok.")
        return
    
    vip_accounts = load_vip_accounts(1)  # 1 VIP hesap gönderilir
    if vip_accounts:
        account_message = f"```\n{vip_accounts[0]}\n```"
        await ctx.author.send(account_message)
        await asyncio.sleep(1)
        await ctx.send("VIP hesap gönderildi.")
    else:
        await ctx.send("VIP hesap bulunamadı.")

def load_vip_accounts(count):
    try:
        with open(VIP_ACCOUNTS_FILE, "r") as file:
            lines = file.readlines()
            accounts = [line.strip() for line in lines[:count]]
            lines = lines[count:]
        
        with open(VIP_ACCOUNTS_FILE, "w") as file:
            file.writelines(lines)

        return accounts
    except Exception as e:
        print(f"VIP hesaplar yüklenirken bir hata oluştu: {str(e)}")
        return []


bot.run(TOKEN)
