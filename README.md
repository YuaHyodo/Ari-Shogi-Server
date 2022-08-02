# Ari-Shogi-Server

# 概要
- Ari-Shogi-Serverは、「ローカルで動く自分専用のミニfloodgate」である。(未完成)
- 開発者が「ローカルで動く自分専用のミニfloodgate」が欲しいと思ったので開発した。
- ちゃんとしたサーバーのプログラムが欲しい人は別のところを当たる事。
- USIプロトコルじゃなくてCSAプロトコルを使う理由: 私(兵頭)のAIはCSAプロトコルには対応しているけどUSIプロトコルには対応していないから
- ファイル・クラス・関数・変数名、出力されるメッセージ、実装方法、設計思想などに関する意見は受け付けておりません。 (不満があるなら自分で作ってください)

# すでにある機能・想定している使い方
## すでにある機能
- CSAプロトコルを使って将棋の対局を行う機能
- 複数のプレーヤーがログインしている時にランダムに対局を組む機能
- 棋譜をCSA形式で出力する機能
- ログをとる機能
- プレーヤの情報を保存・管理する機能
- レートをつける機能(深刻なバグがある可能性高)

## 想定している使い方
- 「ローカルで動く自分専用のミニfloodgate」を作る事で、開発を効率化する。

# 追加予定の機能など
- 簡易的なUI

# ちゃんと実装できていないところ・不具合
- CSAプロトコルの「自分の手番以外で行動しようとすると即反則になる」という規定に関する部分
- 手番を持った対局者が行動しないと永久に対局が終わらない
- ログアウト関連の部分
- その他多数

# 「ローカルで動く自分専用のfloodgate」のメリット
- 1: floodgateと違って、絶対に勝てないAIとマッチングさせられたり、バグのせいで対局開始に間に合わなかったりする事がない。
- 2: 好きな時に対局を開始できる。好きな時にストップできる。
- 3: 「どの改造がどの程度強さに影響を及ぼしたか？」の計測がしやすくなる。なので開発の方針を決めやすくなる。
- 4: 「長期的に見て自分のAIがどれくらい強くなったか？」も分かりやすくなる。すると、「今月はレートを10上げる」という風に目標が立てれるようになる。
- 6: 強化学習nサイクルでどれくらいレートが上がるかも見やすくなる。
- 7: 自分が「欲しい」と思った機能をつけることができるので、その他いろんな事ができる。
