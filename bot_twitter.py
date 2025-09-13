import os
import asyncio
import yt_dlp
from telegram import Update, InputMediaPhoto, InputMediaVideo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ▼▼▼ TOKEN DO BOT ▼▼▼
TOKEN = os.getenv("TOKEN")
# ▲▲▲ TOKEN DO BOT ▲▲▲

# Pasta para downloads temporários
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Função para baixar mídias do Twitter
def baixar_midias(url: str):
    ydl_opts = {
        "outtmpl": f"{DOWNLOAD_DIR}/%(id)s.%(ext)s",
        "quiet": True,
        "merge_output_format": "mp4",  # combina áudio + vídeo
        "noplaylist": False,
        "format": "bestvideo+bestaudio/best",  # melhor qualidade
    }

    # Cookies para NSFW
    if os.path.exists("cookies_twitter.txt"):
        ydl_opts["cookiefile"] = "cookies_twitter.txt"

    arquivos = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)

            # Carrossel / múltiplas mídias
            if "entries" in info and info["entries"]:
                for entry in info["entries"]:
                    entry_info = ydl.extract_info(entry["url"], download=True)
                    arquivos.append(ydl.prepare_filename(entry_info))
            else:
                info_download = ydl.extract_info(url, download=True)
                arquivos.append(ydl.prepare_filename(info_download))

        except Exception as e:
            print(f"Erro no download: {e}")
            return []

    return arquivos

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! 👋 Envie um link do Twitter/X que eu baixo vídeos e fotos para você.\n"
        "Posts com várias mídias também serão baixados."
    )

# Quando usuário envia link
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    media_paths = []

    processing_msg = await update.message.reply_text("⏳ Processando seu link...")

    try:
        if "twitter.com" in url or "x.com" in url:
            media_paths = await asyncio.to_thread(baixar_midias, url)

            if not media_paths:
                await processing_msg.edit_text(
                    "❌ Não foi possível baixar nenhuma mídia.\n"
                    "O post pode ser privado ou os cookies expiraram."
                )
                return

            media_group = []
            files_to_send = [open(path, "rb") for path in media_paths]

            for i, path in enumerate(media_paths):
                ext = path.lower()
                if ext.endswith((".mp4", ".mov", ".webm")):
                    media_group.append(InputMediaVideo(files_to_send[i]))
                elif ext.endswith((".jpg", ".jpeg", ".png", ".webp")):
                    media_group.append(InputMediaPhoto(files_to_send[i]))

            # Envia mídias em grupos de até 10
            for i in range(0, len(media_group), 10):
                await update.message.reply_media_group(media_group[i:i+10])

            await processing_msg.delete()

        else:
            await processing_msg.edit_text("❌ Por favor, envie um link válido do Twitter/X.")

    except Exception as e:
        await processing_msg.edit_text(f"❌ Ocorreu um erro: {e}")

    finally:
        if 'files_to_send' in locals():
            for f in files_to_send:
                f.close()
        for path in media_paths:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError as e:
                    print(f"Erro ao remover arquivo {path}: {e}")

# Rodar bot
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    print("🤖 Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
