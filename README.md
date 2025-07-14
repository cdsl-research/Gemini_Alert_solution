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

### app.py
'/alert' エンドポイントを持つ Webhook サーバー
主な機能は，Alertmanagerなどから送信されるアラートの情報（JSON形式）を受信し，その内容をもとにGoogle Gemini APIに対処方法の提案を依頼を行う．
受信したアラートの情報はプロンプトとして整形され，Geminiに送信される．Geminiからの応答の中からBashスクリプトを自動的に抽出し，fix_issue.shのファイル名で保存される．

### requirements.txt
'app.py'の実行に必要なPythonパッケージが記述されている．

## 注意点
- 本ツールはあくまで支援ツールであるため，生成されるスクリプトの内容は，必ず確認してから実行してください．
- Gemini APIの応答結果により，意図しない内容や不完全なスクリプトが生成される場合があります．複数回の修正や確認をしてください．
- Gemini APIの利用にはAPIキーが必要である，APIの利用料金や制限が発生する可能性があります．使用前に必ず確認してください．

## 使用例
今回は以下のコマンドを実行して仮想環境で説明します．
```
$ python3 -m venv gemini
c0a22169@redmine-test:~$
```
```
$ source gemini/bin/activate
(gemini) c0a22169@redmine-test:~$
```

仮想環境の準備が出来たら，Gemini APIキーの設定をします．
```
$ export GEMINI_APIKEY="your-api-key"
(gemini) c0a22169@redmine-test:~$
```
app.pyを実行します．

```
(gemini) c0a22169@redmine-test:~/gemini_alert$ python app.py 
 * Serving Flask app 'app'
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

今回はテストとしてcurlで確認すると，以下のようにGeminiからの回答が返されます．
```
$ curl -X POST http://localhost:5000/alert \
  -H "Content-Type: application/json" \
  -d '{
    "alertname": "HighMemoryUsage",
    "instance": "web01.example.local",
    "severity": "critical"
}'
=== Gemini 応答 ===
このアラートは、`web01.example.local` サーバーの高メモリ使用率を示しています。このスクリプトは、状況を調査し、いくつかの対処を試みま すが、根本的な原因の解決は行いません。  より適切な対処法は、システムの構成やアプリケーションの最適化など、アラートの原因を特定し根本 的に解決することです。

このスクリプトは、`free` コマンドを使ってメモリ使用状況を確認し 、`/var/log/syslog` を確認し、メモリ使用率が高いプロセスを特定しよう と試みます。  そして、結果をログファイルに記録し、問題が解決したかどうかは確認しません。  より高度な監視や自動化が必要な場合は、この スクリプトを拡張する必要があります。


```bash
#!/bin/bash

# アラート情報
HOST="web01.example.local"
ALERT="HighMemoryUsage"

# ログファイル
LOGFILE="/var/log/fix_issue.log"

# 現在時刻
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# ログに記録
echo "${TIMESTAMP} - Alert: ${ALERT} on ${HOST}" >> ${LOGFILE}

# メモリ使用状況を確認
echo "${TIMESTAMP} - Checking memory usage on ${HOST}" >> ${LOGFILE}
ssh ${HOST} "free -h" >> ${LOGFILE} 2>&1

# 高メモリ使用率のプロセスを特定しようと試みる
echo "${TIMESTAMP} - Identifying high memory usage processes on ${HOST}" >> ${LOGFILE}
ssh ${HOST} "ps aux --sort=-%mem | head -n 10" >> ${LOGFILE} 2>&1

# syslogを確認 (エラーメッセージを探す)
echo "${TIMESTAMP} - Checking syslog on ${HOST}" >> ${LOGFILE}
ssh ${HOST} "tail -n 100 /var/log/syslog" >> ${LOGFILE} 2>&1


# ここでは、メモリを解放する具体的なアクションを追加できます。例えば：
# * 特定のプロセスを停止する (killコマンドを使用する際は慎重に！)
# * キャッシュをクリアする
# * 不要なサービスを停止する

# 例：特定のプロセスIDをkillする (非常に危険なので、慎重に使用する！)
# PID=$(ssh ${HOST} "ps aux | grep [プロセス名] | awk '{print $2}'")
# if [ -n "$PID" ]; then
#   echo "${TIMESTAMP} - Killing process with PID ${PID} on ${HOST}" >> ${LOGFILE}
#   ssh ${HOST} "kill ${PID}" >> ${LOGFILE} 2>&1
# fi

echo "${TIMESTAMP} - Check the log file ${LOGFILE} for details." >> ${LOGFILE}

echo "Check log file: ${LOGFILE}"
```　


**重要な注意:**  このスクリプトは、`ssh` を使用してリモートサー バーに接続します。  `ssh` によるパスワードレスログインを設定するか、 スクリプト実行時にパスワードを要求するようにしてください。  また、`kill` コマンドの使用は非常に危険であり、誤って重要なプロ セスを停 止してしまう可能性があります。  十分に注意して使用し、必要に応じてプロセスを停止する前にバックアップを取ってください。  このスクリプ トはあくまで例であり、実際の環境に合わせて修正する必要があります。  さらに、より堅牢なソリューションとしては、監視ツールと自動化ツー ルを組み合わせたアプローチが推奨されます。

c0a22169@redmine-test:~$
```
上記の出力内容の

\```bashから

\```
までのコマンドがfix_issue.shとして保存されます．


そうすると作業しているディレクトリにfix_issue.shとして保存されていればOKです．
```
(gemini) c0a22169@redmine-test:~/git$ ls
app.py  fix_issue.sh  requirements.txt
(gemini) c0a22169@redmine-test:~/git$
```

## おわりに
今回はGeminiを使ってアラートが通知された時の対処をサポートするソフトウェアを作成しました．生成AIに依存してる部分もあるのでまだまだ改善が必要です．
