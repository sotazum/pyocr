import cv2
import os
import tkinter
import glob
from PIL import Image, ImageTk
import shutil
#import ocr
import sys
import pyocr
import pyocr.builders


def save_frame_range_sec(video_path, start_sec, stop_sec, step_sec,
                         dir_path, basename, ext='jpg'):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    fps = cap.get(cv2.CAP_PROP_FPS)
    fps_inv = 1 / fps

    sec = start_sec
    while sec < stop_sec:
        n = round(fps * sec)
        cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(
                '{}_{}_{:.2f}.{}'.format(
                    base_path, str(n).zfill(digit), n * fps_inv, ext
                ),
                frame
            )
        else:
            return
        print(sec)
        sec += step_sec

save_frame_range_sec('data/2022-04-09.mov', 0, 2095, 3, 'data/images_2', '2022-04-09')


'''
#以下画像処理

#範囲を指定して切り取った画像の保存場所："ocr_images"
#古い画像を削除するため、毎回フォルダ毎削除し、再度フォルダを作成
shutil.rmtree("ocr_images")
os.makedirs("ocr_images")

#OCRを行いたい、未処理の画像の保存場所："images"
jpgs = glob.glob("data/images/*.jpg")
img1 = Image.open(jpgs[0])
W,H = img1.size

#指定範囲した画像に名前をつける番号：cnt
cnt = 1

#コールバック関数：タッチパッドを押した時
def Push(event):
    global x_start,y_start
    x_start = event.x
    y_start = event.y
    canvas.create_rectangle(x_start,y_start,x_start+1,y_start+1,outline="red",tag="rect")

#コールバック関数：タッチパッドから指を離したとき
def Release(event):
    global x_end,y_end,cnt
    x_end = event.x
    y_end = event.y
    canvas.create_rectangle(x_start,y_start,x_end,y_end,outline="red")
    img = Image.open(jpgs[0])
    img.crop((x_start,y_start,x_end,y_end)).save(f"ocr_images/{cnt}.jpg")
    cnt = cnt + 1

#コールバック関数：タッチパッド上で指を動かしている時
def Motion(event):
    x_end = event.x
    y_end = event.y
    canvas.coords("rect",x_start,y_start,x_end,y_end)

#tkinterで画像の表示を行う
root = tkinter.Tk()
root.attributes("-topmost",True)
root.title("image select")

canvas = tkinter.Canvas(root,width=W,height=H,bg="black")
gazou = ImageTk.PhotoImage(file=jpgs[0])

canvas.create_image(int(W/2),int(H/2),image=gazou)
canvas.pack()

#コールバック関数の設定
root.bind("<ButtonPress-1>",Push)
root.bind("<ButtonRelease-1>",Release)
root.bind("<Button1-Motion>",Motion)
root.mainloop()

#OCR・tesseractを実行するpyファイルの呼び出し


jpgs = sorted(glob.glob("ocr_images/*.jpg"),reverse=False)

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No Ocr Tools")
    sys.exit(1)
tool = tools[0]
print("Will use tool")

langs = tool.get_available_languages()

#tkinterで切り取った画像を順々にOCRを実行していく
for i in jpgs:
    txt = tool.image_to_string(Image.open(i),lang="eng+jpn",builder=pyocr.builders.TextBuilder())
    print(txt)
'''