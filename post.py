import anthropic
import requests
import os
import json

def get_access_token():
    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": os.environ["GOOGLE_CLIENT_ID"],
            "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
            "refresh_token": os.environ["GOOGLE_REFRESH_TOKEN"],
            "grant_type": "refresh_token",
        }
    )
    return response.json()["access_token"]

def generate_article():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    
    topics = [
        "韓国語の挨拶表現10選（朝・昼・夜）",
        "韓国語の数字の読み方（固有数詞と漢数詞）",
        "韓国語でよく使う助詞まとめ（は・が・を・に）",
        "韓国語の敬語と丁寧語の使い分け",
        "韓国語の動詞活用の基本パターン",
        "韓国語でよく使うフレーズ20選",
        "ハングルの母音と子音の覚え方",
        "韓国語の発音ルール（連音・激音・濃音）",
        "韓国語で自己紹介をしてみよう",
        "韓国語の時制（過去・現在・未来）の作り方",
    ]
    
    import random
    topic = random.choice(topics)
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": f"""あなたはトマト先生という韓国語講師です。
日本人の韓国語初中級学習者向けに、以下のトピックについてブログ記事を書いてください。

トピック：{topic}

条件：
- 日本語で書く
- わかりやすく親しみやすい文体
- 具体的な韓国語の例文を含める（ハングル・読み方・意味）
- 初中級者でも理解できる内容
- HTML形式で書く（h2, h3, p, tableタグを使用）
- 文字数は800〜1200字程度

タイトルも含めてHTML形式で出力してください。
最初の行に「TITLE:」で始まるタイトルを書いてください。"""
            }
        ]
    )
    
    content = message.content[0].text
    lines = content.split('\n')
    title = topic
    body = content
    
    for i, line in enumerate(lines):
        if line.startswith('TITLE:'):
            title = line.replace('TITLE:', '').strip()
            body = '\n'.join(lines[i+1:])
            break
    
    return title, body

def post_to_blogger(title, content, access_token):
    blog_id = os.environ["BLOGGER_BLOG_ID"]
    
    url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "kind": "blogger#post",
        "title": title,
        "content": content
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        print(f"✅ 投稿成功: {title}")
    else:
        print(f"❌ 投稿失敗: {response.text}")

if __name__ == "__main__":
    print("🍅 トマト先生のブログ自動投稿開始")
    access_token = get_access_token()
    title, content = generate_article()
    post_to_blogger(title, content, access_token)
