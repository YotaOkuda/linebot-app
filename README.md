# Flesh or Stale ??

<br>

## 説明
こちらは「Flesh or Stale ??」という、食品が腐っているかどうかを教えてくれるアプリケーションです。
私は自炊をするとき、購入してから日にちがたっている食材は「腐ってないかな？使って大丈夫かな？」と不安になることがよくあります。そんな時に僕は「にんじん 腐る」などとググって腐っていないか検索結果と照らし合わせて確認します笑。しかし毎回検索 → 記事を探してというのはめんどくさい ...    
そこでその食材の画像をとるだけで、腐っているか判定してくれる便利なアプリがあればいいなと思ったことが制作のきっかけです。（AWS の勉強もしたかった）

具体的にはLINE上で食材の画像を送ると、機械学習で腐っているかを判断し、その結果をメッセージで教えてくれます。
こちらが実際に動いているものになります。  

<div style="display: flex; justify-content: space-between;">
  <img src="/img/Flesh-or-Stale-reaction.png" width="300">
  <img src="/img/Videotogif.gif" width="300">
</div>

<br>

## アーキテクチャ
<img src="/img/architecture.png">

フロントエンドは、LINE を使用しています。LINE Message API を介して AWS 上のシステムと連携します。
まずLINE 上で画像を送信すると、Webhook で指定した AWS API Gateway へリクエストを送信します。これをトリガーとして AWS Lambda が起動し送られてきた画像を取得します。
その後取得した画像を AWS Rekognition で解析し、結果を AWS Lambda に返します。受け取った結果を LINE Message API を介して LINE 上に表示する流れとなっています。

リポジトリは GitHub を使用しており、GitHub Actions によって、CI/CD パイプラインを構築しています。

意識した点としては、「現時点で費用を最小にする構成」と「今後の拡張に対応しやすく」の2点になります。  
1．現時点で費用を最小にする構成  
チャットBotなので常時サーバーを起動しておく必要がないことから、サーバーレス構成を採用することで、費用を抑えています。  

2．今後の拡張に対応しやすく  
フレームワークに SAM（Serverless Application Model）を採用しており、テンプレートファイルでインフラ構成を管理できるので AWS Lambda の追加が容易にできます。  
Step Function なども使用することで、それぞれの Lambda を順番に起動し任意の処理を行うことができます。

<br>

## スキル
<img src="https://skillicons.dev/icons?i=aws,python,github" />

<br>

## 今後の展望
- 現状だと腐っているか微妙、わかりずらい食材については、精度が落ちるところがあるので精度の改善
- たくさんの同食材の中で、どれが一番新鮮か判断する機能の作成
