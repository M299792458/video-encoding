import os
from bot import data, download_dir
from pyrogram.types import Message
from .ffmpeg_utils import encode, get_thumbnail, get_duration, get_width_height

def on_task_complete():
    del data[0]
    if len(data) > 0:
      add_task(data[0])

def add_task(message: Message):
    try:
      msg = message.reply_text("جارٍ تنزيل المقطع...", quote=True)
      filepath = message.download(file_name=download_dir)
      msg.edit("جاريةٌ الآن إعادة ترميز المقطع، قد تأخذ عدة ساعات...")
      new_file = encode(filepath)
      if new_file:
        msg.edit("تمت إعادة ترميز المقطع! جارٍ الحصول على بعض المعلومات فقط...")
        duration = get_duration(new_file)
        thumb = get_thumbnail(new_file, download_dir, duration / 4)
        width, height = get_width_height(new_file)
        msg.edit("جارٍ رفع المقطع إليك...")
        message.reply_video(new_file, quote=True, supports_streaming=True, thumb=thumb, duration=duration, width=width, height=height)
        os.remove(new_file)
        os.remove(thumb)
        msg.edit("تمت إعادة الترميز بنجاح!")
      else:
        msg.edit("فشلت عملية إعادة الترميز! تأكد من أن المقطع ليس أصلاً بترميز h.265")
        os.remove(filepath)
    except Exception as e:
      msg.edit(f"```{e}```")
    on_task_complete()
