import os
import boto3

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage
)

handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))

client = boto3.client('rekognition')


def lambda_handler(event, context):
    headers = event["headers"]
    body = event["body"]

    # get X-Line-Signature header value
    signature = headers['x-line-signature']

    # handle webhook body
    handler.handle(body, signature)

    return {"statusCode": 200, "body": "OK"}

# メッセージが送られてきたときの処理
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """ TextMessage handler """
    # input_text = event.message.text
    input_text = "食材の画像（青果）をアップロードしてください！！"

    line_bot_api.reply_message(
        event.reply_token,
         TextSendMessage(text=input_text)
    )

# 画像が送られてきたときの処理
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    # 送られてきた画像を file_pathに保存
    message_content = line_bot_api.get_message_content(event.message.id)
    file_path = "/tmp/sent-image.jpg"
    with open(file_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    
    # 追加 1
    min_confidence = 40
    model = "arn:aws:rekognition:ap-northeast-1:746669236371:project/linebot-Flesh-or-Stale/version/linebot-Flesh-or-Stale.2024-10-18T14.59.31/1729231170857"
    
    # Rekognition で感情分析
    with open(file_path, 'rb')as fd:
        sent_image_binary = fd.read()
        '''response = client.detect_faces(Image={"Bytes": sent_image_binary},
                                  Attributes=["ALL"])'''
        
        # 追加 2
        response = client.detect_custom_labels(
            Image={"Bytes": sent_image_binary},
            MinConfidence=min_confidence,
            ProjectVersionArn=model
        )
        
        print(response)
    
    # 表情によってメッセージを変更
    '''if all_happy(response):
        message = "素晴らしい笑顔ですね！！"
    else:
        message = "もう少し笑顔を意識してみましょう！！"
    '''
    
    message = response[:100]
    
    # 返答を送信する
    line_bot_api.reply_message(
        event.reply_token,
         TextSendMessage(text=message)
    )
    
    # file_path の画像を削除
    os.remove(file_path)

# 追加    
def find_heighest_confidence(result):
    max_conf = 0
    high_label = "判断できません"
    for customLabel in result['CustomLabels']:
        if max_conf < customLabel['Confidence']:
            max_conf = customLabel['Confidence']
            high_label = f"Label: {customLabel['Name']}, Confidence: {max_conf:.2f}%"
            
    return high_label
        

def all_happy(result):
    for detail in result["FaceDetails"]:
        if most_confident_emotion(detail["Emotions"]) != "HAPPY":
            return False
    return True

def most_confident_emotion(emotions):
    max_conf = 0
    result = ""
    for e in emotions:
        if max_conf < e["Confidence"]:
            max_conf = e["Confidence"]
            result = e["Type"]
    
    return result