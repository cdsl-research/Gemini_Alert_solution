from flask import Flask, request, Response
import os
import google.generativeai as genai
import re

app = Flask(__name__)
genai.configure(api_key=os.getenv("GEMINI_APIKEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_script(response_text):
    """Geminiの応答からbashスクリプトを抽出する"""
    match = re.search(r"(#!/bin/bash.*?)(```|\Z)", response_text, re.DOTALL)
    if match:
        script = match.group(1).strip()
        if "set -x" not in script:
            script = "#!/bin/bash\nset -x\n" + script.split("#!/bin/bash", 1)[-1].strip()
        return script
    return None

@app.route("/alert", methods=["POST"])
def handle_alert():
    try:
        alert = request.get_json()
        prompt = f"""
以下のアラートに対処するシェルスクリプト（fix_issue.sh）を生成してください。

[アラート内容]
{alert}

出力形式: bashスクリプトをMarkdownコードブロックで記述（```bash ...```）
""".strip()

        response = model.generate_content(prompt)
        response_text = response.text.strip() if response.text else "(Geminiの応答が空です)"
        script = extract_script(response_text)

        result_log = f"=== Gemini 応答 ===\n{response_text}\n\n"
        if script:
            with open("fix_issue.sh", "w") as f:
                f.write(script + "\n")
            os.chmod("fix_issue.sh", 0o755)
            result_log += "✅ スクリプトを fix_issue.sh に保存しました。"
        else:
            result_log += "⚠️ スクリプトが抽出できませんでした。"

        return Response(result_log, mimetype="text/plain; charset=utf-8")

    except Exception as e:
        return Response(f"❌ エラー: {str(e)}", mimetype="text/plain; charset=utf-8"), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
