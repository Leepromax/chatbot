import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# 从 Render 环境变量中获取配置
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID")) # 你的 Telegram 数字 ID

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # 如果是你（管理员）发来的消息
    if user.id == ADMIN_ID:
        # 检查是否是回复别人的消息
        if update.message.reply_to_message:
            # 获取原消息的备注信息（之前转发时存下来的对方ID）
            original_sender_id = update.message.reply_to_message.forward_from_chat.id if update.message.reply_to_message.forward_from_chat else None
            # 实际上更稳妥的方法是利用 message.text 或者 database 匹配
            # 简化版：这里演示如何直接回复
            await context.bot.send_message(chat_id=original_sender_id, text=update.message.text)
        return

    # 如果是别人发来的消息，转发给你
    text = f"来自 {user.first_name} (@{user.username}):\n\n{update.message.text}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=text)

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # 处理所有文本消息
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    application.run_polling()
