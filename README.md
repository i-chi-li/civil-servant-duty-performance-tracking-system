# 公務員職務遂行追跡システム

Civil Servant Duty Performance Tracking System

## Elastic Stack

- [Elastic StackとDocker Composeを使いはじめる：パート1](https://www.elastic.co/jp/blog/getting-started-with-the-elastic-stack-and-docker-compose)
- [Elastic StackとDocker Composeを使いはじめる：パート2](https://www.elastic.co/jp/blog/getting-started-with-the-elastic-stack-and-docker-compose-part-2)


# 国会会議録検索システム

(1) 会議単位簡易出力
https://kokkai.ndl.go.jp/api/meeting_list?any=%E7%A7%91%E5%AD%A6%E6%8A%80%E8%A1%93
(2) 会議単位出力
https://kokkai.ndl.go.jp/api/meeting?any=%E7%A7%91%E5%AD%A6%E6%8A%80%E8%A1%93
(3) 発言単位出力
https://kokkai.ndl.go.jp/api/speech?any=%E7%A7%91%E5%AD%A6%E6%8A%80%E8%A1%93

(1) 会議単位簡易出力
https://kokkai.ndl.go.jp/api/meeting_list?from=1980-01-01&until=1980-12-31&speaker=%E7%94%B0%E4%B8%AD%20%E9%88%B4%E6%9C%A8
(2) 会議単位出力
https://kokkai.ndl.go.jp/api/meeting?from=1980-01-01&until=1980-12-31&speaker=%E7%94%B0%E4%B8%AD%20%E9%88%B4%E6%9C%A8
(3) 発言単位出力
https://kokkai.ndl.go.jp/api/speech?from=1980-01-01&until=1980-12-31&speaker=%E7%94%B0%E4%B8%AD%20%E9%88%B4%E6%9C%A8


https://kokkai.ndl.go.jp/api/meeting_list?from=2024-01-29&until=2024-01-29
https://kokkai.ndl.go.jp/api/meeting?maximumRecords=10&recordPacking=json&from=2024-01-29&until=2024-01-29


# NPO 法人
[内閣府 NPO ホームページ](https://www.npo-homepage.go.jp/)
NPO 基礎情報 → NPO 法人情報 → 全国 NPO 法人の検索 → 全国特定非営利活動法人の検索 → データをダウンロードする → NPO 法人情報の一括ダウンロード
全所轄庁 の行政入力情報データ(ZIP形式： 9,880 KB)と法人入力情報データ(ZIP形式： 1,860 KB)を利用する。

# 法人等
[国税庁 法人番号公表サイト](https://www.houjin-bangou.nta.go.jp/)
基本3情報データをダウンロード可能だが、代表者名などは、API で取得する必要がありそう。
API を利用するには、トークンの発行手続が必要。恐らくオンラインでできそう。

