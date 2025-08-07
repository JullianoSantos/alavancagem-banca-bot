
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === CONFIGURAÇÕES ===
TELEGRAM_TOKEN = "8208832771:AAHCu3N2Vl0Yk2GpJ2E9f3PuZQPfXoU6z0A"
GOOGLE_SHEET_ID = "1aKyKzVl-5Ia3G-wMERiHz-H5r8WzLXN-DGI7d1lHnGQ"
ABA_ATIVA = "meta"

# === CONECTAR COM GOOGLE SHEETS ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credenciais = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
cliente = gspread.authorize(credenciais)
planilha = cliente.open_by_key(GOOGLE_SHEET_ID)
aba = planilha.worksheet(ABA_ATIVA)

# === FUNÇÕES AUXILIARES ===
def pegar_stake():
    try:
        stake_celula = aba.acell("D7").value
        return float(stake_celula)
    except:
        return 0.0

def gerar_sugestao():
    stake = pegar_stake()
    odd = 1.40
    lucro = round(stake * (odd - 1), 2)
    return f"🎯 Meta: R${lucro:.2f}\n💰 Stake: R${stake:.2f}\n📊 Odd mínima: {odd}\n\n✅ Sugestão:\nJogo: Vasco x CSA\nMercado: Vasco – empate anula aposta\nOdd: 1.42\nChance estimada: 78%"

# === HANDLERS ===
async def sugestao_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(gerar_sugestao())

async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stake = pegar_stake()
    await update.message.reply_text(f"💼 Status do dia:\nStake: R${stake:.2f}")

async def lucrohoje_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        valor = float(context.args[0])
        aba.update_acell("E7", str(valor))  # Exemplo de célula
        await update.message.reply_text(f"✅ Lucro de R${valor:.2f} registrado.")
    except:
        await update.message.reply_text("❌ Use: /lucrohoje VALOR")

async def perdahoje_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        valor = float(context.args[0])
        aba.update_acell("F7", str(valor))  # Exemplo de célula
        await update.message.reply_text(f"❌ Perda de R${valor:.2f} registrada.")
    except:
        await update.message.reply_text("❌ Use: /perdahoje VALOR")

# === MAIN ===
async def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("sugestao", sugestao_handler))
    app.add_handler(CommandHandler("status", status_handler))
    app.add_handler(CommandHandler("lucrohoje", lucrohoje_handler))
    app.add_handler(CommandHandler("perdahoje", perdahoje_handler))
    print("🤖 Bot iniciado!")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    import asyncio
    asyncio.get_event_loop().run_until_complete(main())


