import requests
import json

# Test dsproxy endpoint
url = "http://localhost:8000/dsproxy"

payload = {
    "data": {
        "company": "softusing",
        "conversation_history": [
            {
                "role": "user",
                "content": "フロントエンド開発者の募集について教えてください"
            }
        ],
        "lang": "jp",
        "job_positions": {
            "departments": [
                {
                    "name": "開発部",
                    "positions": [
                        {
                            "title": "フロントエンド開発者",
                            "salary": "350万円〜500万円",
                            "description": "Webアプリケーションのフロントエンド開発を担当"
                        },
                        {
                            "title": "バックエンド開発者",
                            "salary": "400万円〜650万円",
                            "description": "サーバーサイドロジックとAPI開発を担当"
                        },
                        {
                            "title": "フルスタック開発者",
                            "salary": "450万円〜700万円",
                            "description": "フロントエンドからバックエンドまで幅広く開発"
                        },
                        {
                            "title": "モバイルアプリ開発者",
                            "salary": "370万円〜550万円",
                            "description": "iOS・Android向けモバイルアプリケーション開発"
                        }
                    ]
                },
                {
                    "name": "デザイン部",
                    "positions": [
                        {
                            "title": "UI/UXデザイナー",
                            "salary": "320万円〜480万円",
                            "description": "Webサービスのインターフェースデザインを担当"
                        },
                        {
                            "title": "グラフィックデザイナー",
                            "salary": "280万円〜400万円",
                            "description": "企業ブランディングとマーケティング資料のデザイン"
                        }
                    ]
                },
                {
                    "name": "マーケティング部",
                    "positions": [
                        {
                            "title": "デジタルマーケター",
                            "salary": "330万円〜500万円",
                            "description": "デジタルチャネルでのマーケティング戦略立案・実行"
                        },
                        {
                            "title": "コンテンツクリエイター",
                            "salary": "250万円〜380万円",
                            "description": "ブログ、SNS、動画コンテンツの企画・制作"
                        }
                    ]
                },
                {
                    "name": "総務部",
                    "positions": [
                        {
                            "title": "人事担当者",
                            "salary": "350万円〜480万円",
                            "description": "採用・人事制度の企画運営、労務管理"
                        },
                        {
                            "title": "経理担当者",
                            "salary": "300万円〜450万円",
                            "description": "日常経理業務、決算業務、税務申告サポート"
                        }
                    ]
                }
            ]
        }
    }
}

print("Sending request to:", url)
print("\nPayload:")
print(json.dumps(payload, ensure_ascii=False, indent=2))

try:
    response = requests.post(url, json=payload, timeout=60)
    print("\n" + "="*50)
    print(f"Status Code: {response.status_code}")
    print("="*50)

    if response.status_code == 200:
        result = response.json()
        print("\nResponse:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("\nError Response:")
        print(response.text)

except requests.exceptions.Timeout:
    print("\nRequest timeout!")
except requests.exceptions.ConnectionError:
    print("\nConnection error! Make sure the server is running on http://localhost:8000")
except Exception as e:
    print(f"\nError: {str(e)}")