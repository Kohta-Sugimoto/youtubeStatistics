# youtubeStatistics

# 概要
Youtubeのチャンネルの統計情報を取得するプログラムです。  
情報取得する動画は、アップロード期間の指定ができます。  
下画像のように、画像指定した期間内の動画の合計時間、合計グッド数、合計バッド数、合計視聴回数、合計コメント数、使用許可のあるコンテンツなどが取得できます。

![結果](https://github.com/Kohta-Sugimoto/github-newreppsitory/blob/main/youtubeStatisticsResult.png)

この情報を基に、チャンネルの人気度などが算出できそうです。(どういう計算式にするかは悩み中)

※Youtube APIには1日に送れるリクエストに制限があるため、連続して実行したり、動画数の多いチャンネル(1000個以上くらい)には実行しないことをお勧めします。どうしても大量に処理したい場合は、APIキーを何個か取得するといいと思います。

[参考サイト](https://qiita.com/g-k/items/7c98efe21257afac70e9)を参考にしました。

## 使用言語
言語はPythonです。



## Description
以下のコマンドでプログラム(youtubeStatistics.py)を実行して、動画をダウンロードします。
```bash
sudo python3 youtubeStatistics.py
```

## Setting
以下のコマンドでYouTube APIを使えるようにします。
```bash
sudo pip3 install google-api-python-client
```

## プログラムの編集箇所
### 10行目
Youtube Data APIの登録に関しては[参考サイト](https://qiita.com/g-k/items/7c98efe21257afac70e9)を参考にしてください。
取得したAPIキーをプログラムにコピペしてください。  
### 11行目
ChannelIDは統計情報を取得したいチャンネルのものを入力してください。  
ブラウザでチャンネルのページまで飛んで、URLにChannelIDが載っています。
![URL](https://github.com/Kohta-Sugimoto/github-newreppsitory/blob/main/youtubeURL.PNG)
### 12~15行目
情報取得する動画のアップロード年月日を指定します。
