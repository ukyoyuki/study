import re
import zipfile
import urllib.request
import os.path
import glob

URL = 'https://www.aozora.gr.jp/cards/000081/files/43737_ruby_19028.zip'

def download(URL):
    #➀re.split()：URLの文字列を/で区切り、末尾のzipファイル名「43737_ruby_19028.zip」を取得。
    #➁urllib.request.urlretrieve(URL, 保存名)：当該サイトから直接ファイルをダウンロードし、zipファイル名「43737_ruby_19028.zip」で保存。
    #➂os.path.splitext()：zipファイル名をドット「.」で分割し、拡張子なしのファイル名dirを取得。

    zip_file = re.split(r'/', URL)[-1] #➀
    urllib.request.urlretrieve(URL, zip_file) #➁
    dir = os.path.splitext(zip_file)[0] #➂

    
    #➃zipfile.ZipFile()：先に保存したzipファイルを読み込んで、zipオブジェクトを作成し、
    #➄extractall()：zipオブジェクトの中身をすべて、ディレクトリdirに展開。
    #➅os.remove()：解凍前のzipファイルを削除。
    with zipfile.ZipFile(zip_file) as zip_object: #➃
        zip_object.extractall(dir) #➄

    os.remove(zip_file) #➅

    #➆os.path.join()：dirのパス文字列を生成。
    #➇glob.glob()： ディレクトリ内のテキストファイル名をすべて出力してリスト化。
    #➈list[0]： リスト内の一番目のファイルのパスを返す。
    path = os.path.join(dir,'*.txt') #➆
    list = glob.glob(path) #➇
    return list[0] #➈

def convert(download_text):
    #①open(ファイル名, 'rb').read()：当該ファイルを'rb'（バイナリモード）で読み込む。
    #②decode('shift_jis')：shift_jisに従ってデコードし、テキストを取得。
    data = open(download_text, 'rb').read() #➀
    text = data.decode('shift_jis') #➁

    # 本文抽出
    #➂(r'\-{5,}', text)[2]：ハイフン「-」を5回以上くり返す部分を削除し、これを区切り文字として分割されたうちの3番目の要素を取り出す。
    #④(r'底本：', text)[0]：「底本：」を削除し、これを区切り文字として分割されたうちの1番目の要素を取り出す。
    #➄(r'［＃改ページ］', text)[0]：「［＃改ページ］」を削除し、これを区切り文字として分割されたうちの1番目の要素を取り出す。
    text = re.split(r'\-{5,}', text)[2] #➂  
    text = re.split(r'底本：', text)[0] #➃
    text = re.split(r'［＃改ページ］', text)[0] #➄

    # ノイズ削除
    #➅'《.+?》'：《ルビ》
    #➆'［＃.+?］'：［注記］
    #➇'｜'：ルビ付き文字列の開始位置
    #➈'\r\n'：改行コード
    #➉'\u3000'：全角スペース
    text = re.sub(r'《.+?》', '', text) #➅
    text = re.sub(r'［＃.+?］', '', text) #➆
    text = re.sub(r'｜', '', text) #➇
    text = re.sub(r'\r\n', '', text) #➈
    text = re.sub(r'\u3000', '', text) #➉   

    return text

download_file = download(URL)
text = convert(download_file)

#print(text)

# 分かち書き
import MeCab
mecab = MeCab.Tagger ('-Owakati')
#text = mecab.parse ('今日は晴れです')
#print(text)
#print(mecab.parse(text))


#dir_processed=os.path.join('../texts/',os.path.basename(dir))
with open('../texts/prcssd.txt',mode='w') as f:
    f.writelines(mecab.parse(text))
