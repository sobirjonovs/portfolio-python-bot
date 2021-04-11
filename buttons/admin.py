from aiogram.types import ReplyKeyboardMarkup as keyboard, KeyboardButton as keyboard_button

keyboard = keyboard()
keyboard.row_width = 2
keyboard.add(
    keyboard_button(text='📊 Statistika'),
    keyboard_button(text="📤 Ommaviy xabar"),
    keyboard_button(text="✅ Status"),
    keyboard_button(text="😎 About me"),
    keyboard_button(text="🎯 Ko'nikmalar"),
    keyboard_button(text="🏫 Daraja"),
    keyboard_button(text="🇺🇿 Tillar"),
    keyboard_button(text="💻 Proyekt"),
)
keyboard.resize_keyboard = True
