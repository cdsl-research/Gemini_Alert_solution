# Gemini_Alert_solution

## 環境
- Ubuntu 24.04.2 LTS
- Python 3.12.3
- gemini-1.5-flash

## Pythonライブラリ
- flask
- os
- google.generativeai
- re

## 概要
このFlaskアプリは，Alertmanagerなどから送られてきたアラート情報をGemini APIに渡し，対処スクリプト（bash）を自動生成するWebhookエンドポイントです．

app.py
'/alert' エンドポイントを持つ Webhook サーバー
主な機能は，Alertmanagerなどから送信されるアラートの情報（JSON形式）を受信し，その内容をもとにGoogle Gemini APIに対処方法の提案を依頼を行う．
受信したアラートの情報はプロンプトとして整形され，Geminiに送信される．Geminiからの応答の中からBashスクリプトを自動的に抽出し，fix_issue.shのファイル名で保存される．

requirements.txt
'app.py'の実行に必要なPythonパッケージが記述されている．

## 注意点
- 本ツールはあくまで支援ツールであるため，生成されるスクリプトの内容は，必ず確認してから実行してください．
- Gemini APIの応答結果により，意図しない内容や不完全なスクリプトが生成される場合があります．その都度修正や確認をしてください．
- Gemini APIの利用にはAPIキーが必要である，APIの利用料金や制限が発生する可能性があります．使用前に必ず確認してください．

## 使用例
まずはGemini APIキーの設定をします．
export GEMINI_APIKEY="your-api-key"

```
(gemini) c0a22169@redmine-test:~/gemini_alert$ python app5.py 
 * Serving Flask app 'app5'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.100.80:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 148-530-754
```

