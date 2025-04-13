import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Replace with your bot token and OMDb API key
BOT_TOKEN = "7554607356:AAFkDBYliDVwgDMZOB4x_dj5V59gdBmZs8I"
OMDB_API_KEY = "5d4d156b"

# Optional: Hardcoded movie links (you can expand or replace with real data)
movie_links = {
    "jaat": "https://t.me/+9FwJmboQ-6YwNzVl",
    "titanic": "https://t.me/+9FwJmboQ-6YwNzVl",
    "avatar": "https://t.me/+9FwJmboQ-6YwNzVl"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Welcome to MovieBot!\nType a movie name to get info and download link.")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()

    # Fetch movie info from OMDb
    omdb_url = f"http://www.omdbapi.com/?t={query}&apikey={OMDB_API_KEY}"
    response = requests.get(omdb_url).json()

    if response["Response"] == "True":
        title = response.get("Title", "N/A")
        year = response.get("Year", "N/A")
        rating = response.get("imdbRating", "N/A")
        poster = response.get("Poster", "")
        plot = response.get("Plot", "")

        # Build download link (match lowercase title)
        download_link = movie_links.get(query.lower())

        if download_link:
            button = InlineKeyboardButton("📥 Download", url=download_link)
            reply_markup = InlineKeyboardMarkup([[button]])
            caption = f"*🎬 {title} ({year})*\n⭐ IMDb: {rating}\n\n_{plot}_"

            await update.message.reply_photo(
                photo=poster,
                caption=caption,
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_photo(
                photo=poster,
                caption=f"*🎬 {title} ({year})*\n⭐ IMDb: {rating}\n\nMovie found but no download link yet.",
                parse_mode="Markdown"
            )
    else:
        await update.message.reply_text("❌ Movie not found.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
app.run_polling()


