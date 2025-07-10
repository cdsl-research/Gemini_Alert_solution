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

## 使用例


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

