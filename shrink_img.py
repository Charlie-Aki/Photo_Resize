#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Akihiro Kondo'
__copyright__ = 'North America Engineering Department, Kawasaki Heavy Industries, Ltd.'
__license__ = 'The MIT License (http://opensource.org/licenses/mit-license.php)'


#Importing external flameworks
# ===============================================
import os, sys
import tkinter, tkinter.filedialog
from PIL import Image
import piexif


#How much do you want to shrink the image?
# ===============================================
PERCENT = 50 # 元画像に対するサイズの倍率
CHAR = '_resized' # 処理後に保存する際のファイル名(元のファイル名のあとに追加する文字)


#Functions
# ===============================================
def get_filelist(path):
    '''
    指定PATH内のファイル一覧のリストを得る(フォルダ名は含まれない)
    :param: path: ファイルリストを得るためのPATH
    '''
    filelist = []
    for _f in os.listdir(path):
        if os.path.isfile(os.path.join(path, _f)):
            filelist.append(_f)
    return filelist

def shrink_pil_img(PIL_img, img_file, output_dir_path, percent=100, char='_resized'):
    '''
    画像を縮小する
    :param PIL_img: PIL形式の元画像
    :param img_file: ファイル名+拡張子(例: filename.jpg)
    :param output_dir_path: 保存先のフォルダのPATH
    :param percent :元画像に対するサイズの倍率(初期値は100%; 縮小なし)
    :param char: 処理後に保存する際のファイル名(元のファイル名のあとに追加する文字)(初期値は_resized)
    '''
    w, h = pil_img.size
    max_width = w * percent / 100
    max_height = h * percent / 100
    img_name, ext = os.path.splitext(img_file)

    try:
        exif_dict = piexif.load(pil_img.info["exif"])
        exif_dict["Exif"][piexif.ExifIFD.PixelXDimension] = int(max_width) # piexif.ExifIFD.PixelXDimensionは40962と同じ(Pixel X Dimensionのタグ番号)
        exif_dict["Exif"][piexif.ExifIFD.PixelYDimension] = int(max_height) # piexif.ExifIFD.PixelYDimensionは40963と同じ(Pixel Y Dimensionのタグ番号)
        exif_bytes = piexif.dump(exif_dict)
        pil_img.thumbnail((max_width, max_height), Image.ANTIALIAS)
        pil_img.save(os.path.join(output_dir_path, img_name + char + ext), exif=exif_bytes)
        print('\"', img_file, '\"を処理しました。')
    except KeyError:
        pil_img.thumbnail((max_width, max_height), Image.ANTIALIAS)
        pil_img.save(os.path.join(output_dir_path, img_name + char + ext))
    except Exception as error:
        print('\n', error)
        print('\"', img_file, '\"の処理中にエラーが発生しました。\n')


#main
# =============================================

# 元画像フォルダー選択
root = tkinter.Tk()
root.withdraw()
msg = '縮小したい画像のフォルダーを選択してください。'
print(msg)
img_dir_path = tkinter.filedialog.askdirectory(title=msg)
if (not img_dir_path): # [キャンセル]クリック時の処理
    print('フォルダーを選んでください。')
    sys.exit()

# 出力先フォルダー選択
msg = '出力先のフォルダーを選択してください。'
print(msg)
output_dir_path = tkinter.filedialog.askdirectory(title=msg)
if (not output_dir_path): # [キャンセル]クリック時の処理
    print('フォルダーを選んでください。')
    sys.exit()

# フォルダのファイル名を取得する
filelist = get_filelist(img_dir_path)

# 元画像フォルダー内のファイルを1つずつ処理
for img_file in filelist:
    #print('\"'img_file, '\"を処理します。')
    img_path = os.path.join(img_dir_path, img_file)

    # 元画像読み込み(PIL)
    try:
        pil_img = Image.open(img_path)
    except OSError:
        print('\"', img_file, '\"は読み取れる画像形式ファイルではないためスキップしました。')
    except Exception as error:
        print('\n', error)
        print('\"', img_file, '\"の処理中にエラーが発生しました。\n')
    else:
        shrink_pil_img(pil_img, img_file, output_dir_path, PERCENT, CHAR)
        # 元画像(PIL)を閉じる
        pil_img.close()

print('処理を終了しました。\n')






