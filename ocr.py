#OCR実行する画像をアップロードします。（アップロード後、画像を確認します）
#「ocr.png」「kaisetu.png」のところを変更して使ってみてください。
# from IPython.display import Image,display_png
# display_png(Image('data/images/2022-04-07_000060_1.00.jpg')) #ここを変更

#OCRに挑戦
#「ocr.png」のところを変更して使ってみてください。
from PIL import Image
import pyocr
import pyocr.builders
import sys
import glob
import openpyxl
import pandas as pd

tools = pyocr.get_available_tools()

#OCRが使えるかチェック
if len(tools) == 0:
    print('OCRツールが使えません')
    sys.exit(1)

tool = tools[0]
print("インストールされているOCRツールは', %s" % (tool.get_name()) ,'です。\n Tesseract（テッセラクト）は光学文字認識のエンジンです。\n\n')

img_list = glob.glob('data/images/*.jpg')
img_list = sorted(img_list)
df = [['','','','',''] for x in range(len(img_list))]
j = 0 #j: 実際の問題文番号(0~12)

for i in range(len(img_list)):
    #画像の読み込み
    input_img = Image.open(img_list[i]) #ここを変更

    #画像の特定領域を指定
    img_region = input_img.crop((642, 310, 2240, 977))
    img_region_1 = input_img.crop((692, 1008, 2194, 1111))
    #画像の左上が原点。(x1, y1, x2, y2) 。ここの数字を変更してください。
                                               #x1,y1は左上の端。x2,y2は右下の端


    # OCRを実行する画像イメージや言語指定、オプション指定
    txt = tool.image_to_string(
        img_region,
        lang='eng+jpn',
        builder=pyocr.builders.TextBuilder() #オプション番号は必要に応じて変更してください。デフォルトは「3」
    )
    txt = txt.replace(' ', '')
    txt = txt.replace('\n', '')
    if i != 0 and old_txt[:5] != txt[:5]:
        j += 1

    txt_1 = tool.image_to_string(
        img_region_1,
        lang='eng+jpn',
        builder=pyocr.builders.TextBuilder() #オプション番号は必要に応じて変更してください。デフォルトは「3」
    )
    txt_1 = txt_1.replace(' ', '')
    txt_1 = txt_1.replace('\n', '')
    print('\n\nOCR（光学文字認識）の実行結果\n\n\n__________________\n\n',txt, '\n\n__________________\n\n')

    print('\n\nOCR（光学文字認識）の実行結果\n\n\n__________________\n\n', txt_1, '\n\n__________________\n\n')

    if j > 0:
        if df[j-1][0][:5] != txt[:5]: #最初の5文字を比較
            df[j][0] = txt #問題文書き込み
    else:
        df[j][0] = txt  # 問題文書き込み



    if df[j][1] == '':
        df[j][1] = txt_1 #質問文書き込み
    elif df[j][2] == '' and df[j][1] != '' and txt_1[:5] != df[j][1][:5]:
        df[j][2]= txt_1  # 質問文書き込み
    elif df[j][3] == '' and df[j][2] != '' and txt_1[:5] != df[j][2][:5]:
        df[j][3] = txt_1  # 質問文書き込み
    elif df[j][4] == '' and df[j][3] != '' and txt_1[:5] != df[j][3][:5]:
        df[j][4] = txt_1  # 質問文書き込み

    old_txt = txt
    print(df)
    print('j', j)
    print('i', i)

df = pd.DataFrame(df)
df.to_excel('excel/sample.xlsx', sheet_name='Sheet1')