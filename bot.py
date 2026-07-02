import os
import logging
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# 1. 初始化日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 2. 从环境变量安全获取配置
BOT_TOKEN = os.getenv("BOT_TOKEN")
admin_id_str = os.getenv("ADMIN_ID")

# 检查变量是否存在，如果不存在则报错并停止
if not BOT_TOKEN:
    print("错误: 环境变量 BOT_TOKEN 未设置！")
    sys.exit(1)
if not admin_id_str:
    print("错误: 环境变量 ADMIN_ID 未设置！")
    sys.exit(1)

try:
    ADMIN_ID = int(admin_id_str)
except ValueError:
    print(f"错误: ADMIN_ID 必须是纯数字，当前值为: {admin_id_str}")
    sys.exit(1)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not update.message or not update.message.text:
        return

    # --- 管理员回复逻辑 ---
    if user.id == ADMIN_ID and update.message.reply_to_message:
        original_text = update.message.reply_to_message.text
        # 从之前的转发消息末尾提取用户 ID
        if "用户ID:" in original_text:
            try:
                target_id = int(original_text.split("用户ID: ")[-1].strip())
                await context.bot.send_message(chat_id=target_id, text=update.message.text)
                await update.message.reply_text("✅ 回复已发送")
            except Exception as e:
                await update.message.reply_text(f"❌ 发送失败: {e}")
        return

    # --- 转发用户消息给管理员 ---
    text = f"来自 {user.first_name} (@{user.username}):\n\n{update.message.text}\n\n----------\n用户ID: {user.id}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=text)

if __name__ == '__main__':
    print("正在启动机器人...")
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # 过滤掉命令，只处理文本消息
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("机器人已启动，监听中...")
    application.run_polling()
