# bulk-screen-capture

bulk screen capture script intended to use for Anki.

## 前準備

- Chrome Browser を自動操縦するためのドライバ [Chrome driver](http://chromedriver.chromium.org/downloads) をダウンロードして、 PATH の通ったとこ(`/usr/local/bin` とか)に置く。
Shell から `chromedriver -h` と打って、help が出たらOK

- selenium と pillow の install
```
pip install selenium pillow
```

## 使い方

### help


ヘルプを見て使えるオプションを確認。オプションを試行錯誤する場合は `--show` オプションでブラウザを表示しておくと便利

```python
$ python bulk-screen-capture.py -h
```

### 実践編

```python
python bulk-screen-capture.py -d collection.media -p "google-img--" -j before_scroll.js -w 720x720 word.txt
```

- `-d collection.media`: 保存先ディレクトリを指定
- `-p "google-img--"`: ファイル名につけるprefix。Ankiのメディアファイルはサブディレクトリに入れるとデバイス間で、同期されないので、メディアディレクトリ直下に置く必要あるので、見分けがつくように Prefix で目印をつけたい場合に使う。
- `-j before_scroll.js`: 保存前に呼ぶスクリプトのファイル名を指定。
- `-w 720x720`: スクリーンサイズ。大きくすると画像は綺麗だがサイズが大きくなる。
- `sample.tsv`: 最後に渡すのはファイル名。タブ区切りの最初のフィールドの単語を検索する。どうせ最初のフィールドしか使わないので、一行ずつ単語が書かれたファイルでも良い。

sample.tsv の中身
```
tactic	戦術、戦法、作戦
backfire	計画などが裏目に出る、エンジン・車がさか火を起こす
catastrophic	壊滅的な、大異変の、最悪の
```

<p>
<img src="./imgs/google-img--tactic.jpg" width="300">
<img src="./imgs/google-img--backfire.jpg" width="300">
<img src="./imgs/google-img--catastrophic.jpg" width="300">
</p>

### デフォルトの `before_scroll.js` は何をしているか？

画面キャプチャを撮る前に良い感じの場所までスクロールさせている。

以下の検索結果の画像で説明する。
- `A`: この部分は邪魔。`B` あるいは `C` までスクロールしてから撮りたい
- `B`: この部分はその単語がどんな文脈で使われるかを知るのに便利
- `C`: しかし、検索語によっては `B` が出ない場合もある。その場合は `C`までスクロール

<p>
<img src="./imgs/Google_Search.png" width="600">
</p>
