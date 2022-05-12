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

img_list = glob.glob('data/images_2/*.jpg')
img_list = sorted(img_list)
df = [['','','','','','',''] for x in range(len(img_list))]
j = 0 #j: 実際の問題文番号(0~12)

nums = [0]

for i in range(len(img_list)):
    #画像の読み込み
    input_img = Image.open(img_list[i]) #ここを変更

    #画像の特定領域を指定
    img_region = input_img.crop((642, 357, 1500, 393))
    #縮小
    # width, height = img_img.size
    # w_shrink = 2
    #h_shrink = 2
    # img_img_resize = img_img.resize((int(width / w_shrink), int(height / h_shrink)))
    img_region_1 = input_img.crop((767, 1008, 2120, 1128))
    # 以下選択肢
    img_region_2 = input_img.crop((692, 1143, 2250, 1171))
    img_region_3 = input_img.crop((692, 1183, 2250, 1220))
    img_region_4 = input_img.crop((692, 1222, 2250, 1265))
    img_region_5 = input_img.crop((692, 1265, 2250, 1300))
    img_region_6 = input_img.crop((692, 1300, 2250, 1344))
    #画像の左上が原点。(x1, y1, x2, y2) 。ここの数字を変更してください。
                                               #x1,y1は左上の端。x2,y2は右下の端
                                               #玉手箱言語問題文(642, 310, 2240, 977)
                                               #玉手箱言語質問文(692, 1008, 2194, 1111)

    # OCRを実行する画像イメージや言語指定、オプション指定
    txt = tool.image_to_string(
        img_region,
        lang='eng+jpn',
        builder=pyocr.builders.TextBuilder() #オプション番号は必要に応じて変更してください。デフォルトは「3」
    )
    txt = txt.replace(' ', '')
    txt = txt.replace('\n', '')

    txt_1 = tool.image_to_string(
        img_region_1,
        lang='eng+jpn',
        builder=pyocr.builders.TextBuilder() #オプション番号は必要に応じて変更してください。デフォルトは「3」
    )
    txt_1 = txt_1.replace(' ', '')
    txt_1 = txt_1.replace('\n', '')



    txt_2 = tool.image_to_string(
        img_region_2,
        lang='eng+jpn',
        builder=pyocr.builders.TextBuilder()  # オプション番号は必要に応じて変更してください。デフォルトは「3」
    )
    txt_2 = txt_2.replace(' ', '')

    if i != 0 and old_txt[:5] != txt_2[:5]:
        j += 1
        nums.append(i)

    txt_3 = tool.image_to_string(
        img_region_3,
        lang='eng+jpn',
        builder=pyocr.builders.TextBuilder()  # オプション番号は必要に応じて変更してください。デフォルトは「3」
    )
    txt_3 = txt_3.replace(' ', '')

    txt_4 = tool.image_to_string(
        img_region_4,
        lang='eng+jpn',
        builder=pyocr.builders.TextBuilder()  # オプション番号は必要に応じて変更してください。デフォルトは「3」
    )
    txt_4 = txt_4.replace(' ', '')

    txt_5 = tool.image_to_string(
        img_region_5,
        lang='eng+jpn',
        builder=pyocr.builders.TextBuilder()  # オプション番号は必要に応じて変更してください。デフォルトは「3」
    )
    txt_5 = txt_5.replace(' ', '')

    txt_6 = tool.image_to_string(
        img_region_6,
        lang='eng+jpn',
        builder=pyocr.builders.TextBuilder()  # オプション番号は必要に応じて変更してください。デフォルトは「3」
    )
    txt_6 = txt_6.replace(' ', '')
    print('\nOCR（光学文字認識）の実行結果\n__________________\n',txt, '\n__________________\n')
    print('\nOCR（光学文字認識）の実行結果\n__________________\n', txt_1, '\n__________________\n')
    print('\nOCR（光学文字認識）の実行結果\n__________________\n', txt_2, '\n__________________\n')
    print('\nOCR（光学文字認識）の実行結果\n__________________\n', txt_3, '\n__________________\n')
    print('\nOCR（光学文字認識）の実行結果\n__________________\n', txt_4, '\n__________________\n')
    print('\nOCR（光学文字認識）の実行結果\n__________________\n', txt_5, '\n__________________\n')
    print('\nOCR（光学文字認識）の実行結果\n__________________\n', txt_6, '\n__________________\n')
    if j > 0:
        if df[j-1][0][:5] != txt[:5]: #最初の5文字を比較
            df[j][0] = txt #問題文書き込み
    else:
        df[j][0] = txt  # 問題文書き込み




    df[j][1] = txt_1 #質問文書き込み
    df[j][2] = txt_2 # 質問文書き込み
    df[j][3] = txt_3 # 質問文書き込み
    df[j][4] = txt_4 # 質問文書き込み
    df[j][5] = txt_5 # 質問文書き込み
    df[j][6] = txt_6 # 質問文書き込み
    # df[j][7] = img_img

    old_txt = txt_2
    print(df)
    print('j', j)
    print('i', i)

df = pd.DataFrame(df)
df.to_excel('excel/sample_2.xlsx', sheet_name='Sheet1')
wb = openpyxl.load_workbook('excel/sample_2.xlsx')
ws = wb["Sheet1"]

for i in range(len(nums)):
    x = nums[i]
    img = openpyxl.drawing.image.Image(img_list[x])
    pos = 'J' + str(i+2)
    ws.add_image(img, pos)
wb.save('excel/sample_2.xlsx')