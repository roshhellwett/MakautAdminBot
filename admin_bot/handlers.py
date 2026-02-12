import os
import sys
import asyncio
import psutil
import subprocess
from telegram import Update
from telegram.ext import ContextTypes
from core.config import ADMIN_ID
from database.repository import NotificationRepo, SecurityRepo

async def update_system(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asynchronously pulls latest code from GitHub and restarts."""
    if update.effective_user.id != ADMIN_ID: return
    
    msg = await update.message.reply_text("📥 <b>Admin:</b> Pulling from GitHub...", parse_mode="HTML")
    
    # DEFINE WORKER: Runs git in a thread to prevent blocking/crashing the loop
    def run_git_pull():
        try:
            # shell=True required for Windows command parsing
            res = subprocess.run("git pull origin main", shell=True, capture_output=True, text=True)
            return res.returncode, res.stdout, res.stderr
        except Exception as e:
            return 1, "", str(e)

    # EXECUTE: Run securely in a thread
    code, stdout, stderr = await asyncio.to_thread(run_git_pull)
    
    if code == 0:
        await msg.edit_text("✅ Code updated. Restarting system...")
        # FIXED: Use sys.executable to ensure we use the same Python interpreter
        # This handles 'python', 'python3', or virtualenv paths correctly
        os.execv(sys.executable, [sys.executable] + sys.argv)
    else:
        await msg.edit_text(f"❌ Git Fail: {stderr}")

async def send_db_backup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Securely sends BOTH Academic and Security databases."""
    if update.effective_user.id != ADMIN_ID: return

    # Backup List: Academic Data + Security Logs
    targets = ["makaut.db", "security.db"]
    sent = 0

    for db_file in targets:
        if os.path.exists(db_file):
            try:
                with open(db_file, 'rb') as f:
                    await update.message.reply_document(
                        document=f, 
                        caption=f"📂 <b>Backup:</b> {db_file}",
                        parse_mode="HTML"
                    )
                sent += 1
            except Exception as e:
                await update.message.reply_text(f"❌ Failed to upload {db_file}: {e}")
        else:
            await update.message.reply_text(f"⚠️ Warning: {db_file} not found.")
            
    if sent == 0:
        await update.message.reply_text("❌ No database files found on server.")

async def health_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forensic Health Report using Decoupled Repositories."""
    if update.effective_user.id != ADMIN_ID: return
    
    # System Metrics
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    
    # Database Metrics (Via Repositories)
    total_notices = await NotificationRepo.get_stats()
    active_strikes = await SecurityRepo.get_active_strikes()

    status_msg = (
        "<b>🖥️ ZENITH SYSTEM HEALTH</b>\n\n"
        f"<b>📊 CPU:</b> {cpu}% | <b>🧠 RAM:</b> {ram}%\n"
        f"<b>📁 DB Notices:</b> {total_notices}\n"
        f"<b>🚫 Security Flags:</b> {active_strikes}\n\n"
        "✅ <b>Repositories:</b> LINKED\n"
        "✅ <b>Pipeline:</b> HEARTBEAT STABLE"
    )
    await update.message.reply_text(status_msg, parse_mode='HTML')
    #@academictelebotbyroshhellwett