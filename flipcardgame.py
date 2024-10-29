import tkinter as tk
from PIL import Image, ImageTk
import random
from datetime import datetime
import soundfile as sf
import sounddevice as sd

# Tạo window
window = tk.Tk()
window.title("The Memory Game")
window.geometry("800x600")

# Thêm background
background_image = ImageTk.PhotoImage(Image.open("./image/background.jpg").resize((800, 600)))
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Bắt đầu tính thời gian
tgbatdau = datetime.now()

# Số lượng cặp hình
socapthe = 10

# Tạo list hình
images = {}
for i in range(1, 6):
    images[i] = ImageTk.PhotoImage(Image.open(f"./image/hinh{i}.jpg").resize((75, 112)))

# Thêm hình trước và sau lật thẻ
images["cardbian"] = ImageTk.PhotoImage(Image.open("./image/card_an.jpg").resize((75, 112)))
images["gheptrung"] = ImageTk.PhotoImage(Image.open("./image/true.jpg").resize((75, 112)))

# Tạo list chứa các thẻ
cards = []
while len(cards) < socapthe * 2:
    value = random.randint(1, 5)
    cards.append(value)
    cards.append(value)
random.shuffle(cards)

# Trạng thái các thẻ
dalat = [False] * len(cards)
buttons = []
thedautien = None
gheptrung = 0
xuly = False

# Hàm lật thẻ
def latthe(stt):
    global thedautien, gheptrung, xuly
    if xuly or dalat[stt]:
        return

    # Hiển thị ảnh của thẻ khi lật
    buttons[stt].config(image=images[cards[stt]])
    dalat[stt] = True

    if thedautien is None:
        thedautien = stt
    else:
        xuly = True
        if cards[thedautien] == cards[stt]:
            gheptrung += 1
            window.after(1000, dungcards, thedautien, stt)
        else:
            window.after(1000, saicards, thedautien, stt)
        thedautien = None

# Úp thẻ nếu sai
def saicards(i, j):
    buttons[i].config(image=images["cardbian"])
    buttons[j].config(image=images["cardbian"])
    dalat[i] = False
    dalat[j] = False
    global xuly
    xuly = False
    data, samplerate = sf.read("./sound/wrong.mp3")
    sd.play(data, samplerate)

# Lật thẻ nếu đúng
def dungcards(i, j):
    buttons[i].config(image=images["gheptrung"], state="disabled")
    buttons[j].config(image=images["gheptrung"], state="disabled")
    dalat[i] = True
    dalat[j] = True
    data, samplerate = sf.read("./sound/right.mp3")
    sd.play(data, samplerate)

    global xuly
    xuly = False

    # Điều kiện win
    if gheptrung == socapthe:
        tgketthuc = datetime.now()
        time = (tgketthuc - tgbatdau).total_seconds()
        for button in buttons:
            button.grid_forget()
        # Mức độ hoàn thành
        if time < 45:
            message = f"Bạn là pro player với thời gian {time:.2f} giây!"
            images["win_background"] = ImageTk.PhotoImage(Image.open("./image/win4.jpg").resize((800, 600)))
            data, samplerate = sf.read("./sound/winsound4.mp3")
            sd.play(data, samplerate)
        elif 45 <= time < 60:
            message = f"Bạn hoàn thành tốt với thời gian {time:.2f} giây!"
            images["win_background"] = ImageTk.PhotoImage(Image.open("./image/win3.jpg").resize((800, 600)))
            data, samplerate = sf.read("./sound/winsound3.mp3")
            sd.play(data, samplerate)
        elif 60 <= time < 90:
            message = f"Bạn hoàn thành tạm ổn với thời gian {time:.2f} giây!"
            images["win_background"] = ImageTk.PhotoImage(Image.open("./image/win2.jpg").resize((800, 600)))
            data, samplerate = sf.read("./sound/winsound2.mp3")
            sd.play(data, samplerate)
        else:
            message = f"Bạn cần phải làm nhanh hơn, kết quả vừa rồi là {time:.2f} giây!"
            images["win_background"] = ImageTk.PhotoImage(Image.open("./image/win1.jpg").resize((800, 600)))
            data, samplerate = sf.read("./sound/winsound1.mp3")
            sd.play(data, samplerate)
            
        win_label = tk.Label(window, image=images["win_background"])
        win_label.place(x=0, y=0, relwidth=1, relheight=1)
        win_text = tk.Label(window, text=message, font=("Arial", 24), bg="white")
        win_text.place(relx=0.5, rely=0.1, anchor="center")

socot = 5
sohang = (len(cards) + socot - 1) // socot

# Tính khoảng cách cho các thẻ
chieurong, chieucao = 75, 112
xspace = (800 - (chieurong * socot)) // (socot + 1)
yspace = (600 - (chieucao * sohang)) // (sohang + 1)

# Tạo nút cho các thẻ
for i in range(len(cards)):
    hang = i // socot 
    cot = i % socot 
    x = xspace + cot * (chieurong + xspace) 
    y = yspace + hang * (chieucao + yspace)
    button = tk.Button(window, image=images["cardbian"], width=chieurong, height=chieucao, command=lambda i=i: latthe(i))
    button.place(x=x, y=y)
    buttons.append(button)

# loop trò chơi
window.mainloop()