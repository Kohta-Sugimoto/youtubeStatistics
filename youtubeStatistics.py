from apiclient.discovery import build
from apiclient.errors import HttpError

"""
----------------
---個人設定変数---
----------------
"""

API_KEY = 'AIzaSyDeGw6HOyoqdCOWrWw2YFk6gHlrIXLGJ44'   #取得したAPIキーを入力(個人で違う)
CHANNEL_ID = 'UCNJb1eaB1C7oVlKfDT0LgwQ'              #ダウンロードしたいチャンネルのIDを入力
YEAR_Ceiling = 2100            #動画の投稿日時を指定
MONTH_Ceiling = 12
YEAR_Floor = 2021
MONTH_Floor = 2
"""
以下４行のように期間指定すると、2100年１2月から2019年8月までの動画の時間を計算
YEAR_Ceiling = 2100
MONTH_Ceiling = 12
YEAR_Floor = 2020
MONTH_Floor = 1
"""
#統計情報の格納に使用する変数
duration_Hour_Sum = 0
duration_Minite_Sum = 0
duration_Second_Sum = 0
like_Sum = 0
dislike_Sum = 0
viewcount_Sum = 0
comment_Sum = 0
licenced_True_Sum = 0
licenced_False_Sum = 0
licenced_Unknown_Sum = 0

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
channels = [] #チャンネル情報を格納する配列
searches = [] #videoidを格納する配列
videos = [] #各動画情報を格納する配列
nextPagetoken = None
nextpagetoken = None

youtube = build(
    YOUTUBE_API_SERVICE_NAME, 
    YOUTUBE_API_VERSION,
    developerKey=API_KEY
    )

channel_response = youtube.channels().list(
    part = 'snippet,statistics',
    id = CHANNEL_ID
    ).execute()
    
#動画時間を合計する関数
def sumDuration(duration):
    global duration_Hour_Sum, duration_Minite_Sum, duration_Second_Sum
    hour = 0
    minite = 0
    second = 0
 #   print(duration)
    idx_Hour = duration.find('H')
    idx_Minite = duration.find('M')
    idx_Second = duration.find('S')
    if idx_Hour != -1:
        hour = int(duration[2:idx_Hour])
    if idx_Minite != -1:
        if idx_Hour != -1:
            minite = int(duration[idx_Hour+1:idx_Minite])
        else:
            minite = int(duration[2:idx_Minite])
    if idx_Second != -1:
        if idx_Minite != -1:
            second = int(duration[idx_Minite+1:idx_Second])
        else:
            if idx_Hour != -1:
                second = int(duration[idx_Hour+1:idx_Second])
            else:
                second = int(duration[2:idx_Second])
    print(str(hour) + '時間' + str(minite) + '分' + str(second) + '秒')
    duration_Hour_Sum += hour
    duration_Minite_Sum += minite
    duration_Second_Sum += second

#設定した期限内にアップされた動画かを判定
def uploadDateCheck(date):
    year = int(date[0:4])
    month = int(date[5:7])
    if YEAR_Floor <= year and year <= YEAR_Ceiling:
        if MONTH_Floor <= month or year > YEAR_Floor:
            if month <= MONTH_Ceiling or year < YEAR_Ceiling:
                return True
    return False

#時間を正しい表記にする関数
def optimizeDuration():
    global duration_Hour_Sum, duration_Minite_Sum, duration_Second_Sum
    duration_Minite_Sum += duration_Second_Sum / 60
    duration_Second_Sum %= 60
    duration_Hour_Sum += duration_Minite_Sum / 60
    duration_Minite_Sum %= 60
    duration_Hour_Sum = round(duration_Hour_Sum, 0)
    duration_Minite_Sum = round(duration_Minite_Sum, 0)
    duration_Second_Sum = round(duration_Second_Sum, 0)

#グッド数、バッド数を合計する関数
def movieLikeDislikeCount(likeNum, dislikeNum):
    global like_Sum, dislike_Sum
    like_Sum += int(likeNum)
    dislike_Sum += int(dislikeNum)

#視聴回数を合計する関数
def movieViewCount(viewCount):
    global viewcount_Sum
    viewcount_Sum += int(viewCount)

#コメント数を合計する関数
def movieCommentCount(commentCount):
    global comment_Sum
    comment_Sum += int(commentCount)

#動画のライセンス状態を合計する関数
def movieLicensedCount(licenced):
    #print(licenced)
    global licenced_True_Sum, licenced_False_Sum, licenced_Unknown_Sum
    if licenced == True:
        licenced_True_Sum += 1
    elif licenced == False:
        licenced_False_Sum += 1
    else:
        licenced_Unknown_Sum += 1


for channel_result in channel_response.get("items", []):
    if channel_result["kind"] == "youtube#channel":
        channels.append([channel_result["snippet"]["title"],channel_result["statistics"]["subscriberCount"],channel_result["statistics"]["videoCount"],channel_result["snippet"]["publishedAt"]])

while True:
    if nextPagetoken != None:
        nextpagetoken = nextPagetoken

    search_response = youtube.search().list(
      part = "snippet",
      channelId = CHANNEL_ID,
      maxResults = 50,
      order = "date", #日付順にソート
      pageToken = nextpagetoken #再帰的に指定
      ).execute()

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            searches.append(search_result["id"]["videoId"])

    try:
        nextPagetoken =  search_response["nextPageToken"]
    except:
        break

for result in searches:
    video_response = youtube.videos().list(
      part = 'snippet,statistics,contentDetails',
      id = result
      ).execute()

    for video_result in video_response.get("items", []):
        if video_result["kind"] == "youtube#video":
            videos.append([video_result["snippet"]["title"],video_result["statistics"]["viewCount"],video_result["statistics"]["likeCount"],video_result["statistics"]["dislikeCount"],video_result["statistics"]["commentCount"],video_result["snippet"]["publishedAt"],video_result["contentDetails"]["licensedContent"],video_result["id"]])  
        #統計情報を処理
        if uploadDateCheck(video_result["snippet"]["publishedAt"]):
            sumDuration(video_result["contentDetails"]["duration"])
            movieLikeDislikeCount(video_result["statistics"]["likeCount"], video_result["statistics"]["dislikeCount"])
            movieViewCount(video_result["statistics"]["viewCount"])
            movieCommentCount(video_result["statistics"]["commentCount"])
            movieLicensedCount(video_result["contentDetails"]["licensedContent"])

optimizeDuration()

print('URLが　https://www.youtube.com/channel/' + CHANNEL_ID + '　のチャンネルの')
print(str(YEAR_Floor) + '年' + str(MONTH_Floor) + '月から' + str(YEAR_Ceiling) + '年' + str(MONTH_Ceiling) + '月 までの動画の統計情報')
print('合計時間： ' + str(duration_Hour_Sum) + '時間 ' + str(duration_Minite_Sum) + '分 ' + str(duration_Second_Sum) + '秒')
print('合計グッド数: ' + str(like_Sum) + '  合計バッド数: ' + str(dislike_Sum))
print('合計視聴回数: ' + str(viewcount_Sum))
print('合計コメント数: ' + str(comment_Sum))
print('使用許可のあるコンテンツ: ' + str(licenced_True_Sum) + '　使用許可のないコンテンツ: ' + str(licenced_False_Sum) + '　使用許可が不明なコンテンツ: ' + str(licenced_Unknown_Sum))