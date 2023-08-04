import requests

YOUR_API_KEY = 'YOUR-DEEPL-API-KEY'


def translate_to_english():
    text = input('翻訳したい日本語を入力してください。> ')
    params = {
                "auth_key": YOUR_API_KEY,
                "text": text,
                "source_lang": 'JA',
                "target_lang": 'EN' 
            }
    # パラメータと一緒にPOSTする
    request = requests.post("https://api-free.deepl.com/v2/translate", data=params)

    result = request.json()
    print(result["translations"][0]["text"])


translate_to_english()