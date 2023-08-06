# Google Drive 関連の処理
from google.colab import drive
def mount():
  drive.mount('/drive', force_remount=True)

from pathlib import Path
DATADIR = Path('/drive/MyDrive/research/2022/nlp100/data')

import os

# download: URL先のデータをダウンロードしたファイルのパスを返す。まだダウンロードしてなければダウンロードする。
def download(url):
    path = DATADIR.joinpath(url.split('/')[-1])
    if not path.exists():
        os.system(f'curl -o {path} {url}')
    return path
