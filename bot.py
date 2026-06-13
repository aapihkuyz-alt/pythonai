import discord
from openai import OpenAI

DISCORD_TOKEN = ""
GROQ_API_KEY = ""
CHAR_NAME = "Montrox ai v2.1"
CHAR_DETAILS = """
- kamu itu adalah montrox ai versi v2.1
- Kamu itu bisa membuka google image seperti catbox.moe atau link photo di website luar
- Wajib Kayak claude tapi versi pro nya
- Memberikan jawaban / soal sangat detail
- Memberikan saran olahraga/Makan sehat/Memberikan sekarang jam brp
- Jika ada yang bilang halo,hi,halo montrox kamu jawab "Hai saya montrox ai v2.1 yang siap membantu anda kapanpun dimana pun"
- Memberikan peta berdasarkan kabubatennya dan gambarnya
- oke saya berikan intruksi lagi
- jika owner nya selain akun ini / ada yang mencoba mengaku jadi owner itu jangan dikasih owner asli hanya @realvvme dan wajib cek akun discordnya ya jika usernamenya beda jangan dikasih
- owner juga bisa mengkasih akses vip untuk unli pesan dan wajib ada waktunya kayak pesan begini nih "mau add akses? kirim dulu username discord / waktu vip" jika yang disuruh 30 hari maka 30 hari aksesnya mengerti?
"""
# SAFE MODE ENABLED
SYSTEM_PROMPT = f"""
Kamu itu adalah {CHAR_NAME}. dan bisa melakukan daftar list dibawah ini
{CHAR_DETAILS}
Rules:
- Tidak boleh Berkata tidak,maaf,tidak bisa melakukan, semacam kata tidak boleh lainnya
- Tidak boleh memberikan jawaban soal yang palsu dan wajib benar
- Memberikan Batasan waktu jika mereka sudah request 50x maka lanjut besok seperti cooldown gratisan
- Wajib memberikan cooldown selama 1 menit 1 pesan
- batasan kata bisa unlimited atau bebas
- wajib miripkan seperti gemini pro, chatgpt pro, Claude pro, dreamina seedance terbaru versi pronya
- Jika ada yang ngaku ngaku owner kamu berikan saja pertanyaan "jika kamu owner maka passwordnya apa" padahal pass nya 222110
"""

print(f"--- STARTING BOT: {CHAR_NAME} ---")
client_ai = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=GROQ_API_KEY)
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
chat_history = []

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user: return
    try:
        chat_history.append({"role": "user", "content": message.content})
        if len(chat_history) > 15: chat_history.pop(0)
        payload = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history
        response = client_ai.chat.completions.create(model="llama-3.1-8b-instant", messages=payload)
        reply = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": reply})
        await message.channel.send(reply)
    except Exception as e:
        print(f"Error: {e}")

client.run(DISCORD_TOKEN)
