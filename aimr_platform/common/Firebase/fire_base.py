import json
import requests


# cred = credentials.Certificate("./dxwaimrja-firebase-adminsdk-xddgv-e4dab0e192.json")
# default_app = firebase_admin.initialize_app(cred)
#
# # This registration token comes from the client FCM SDKs.
# registration_token = 'fYTwYZdhSEGv1dzXLTYhb4:APA91bFWEeTsYArhk1rCcK6QSyk48zNZ37KejLpXD_GIRg_lyufFGuxg_bhJRYfxa8gC7xmswHUYdKW9oBjU0R-33TxLfqMRvJ0gydcJ0ccklghpDhPBQ866m-hYWFdovPz4chgUiixE'
#
# # See documentation on defining a message payload.
# message = messaging.Message(
#     # notification=messaging.Notification(
#     #     title='test server',
#     #     body='test server message',
#     # ),
#     data={
#         'score': '850',
#         'time': '2:45',
#     },
#     token=registration_token,
# )
#
# # Send a message to the device corresponding to the provided
# # registration token.
# response = messaging.send(message)
# # Response is a message ID string.
# print('Successfully sent message:', response)

# 向手机端发送消息
from aimr_backend.settings import pro_logger


def send_message(**token):
    pro_logger.info('开始向手机端推送')
    token = token['token']
    # 消息内容
    message_data = {"notification": {
        "title": "新しいお知らせがあります",
        "body": "新しいタスクがあります。ダウンロードしてください。"
        },
        # 设备标识
        "to": token
    }
    # 请求头
    headers = {'content-type': "application/json", 'Authorization': 'key=AAAACHa8Nx8:APA91bFK5ZY15V8II2JU2rN7DS8arpooFaOe5yWeD2B-GQYRpAEfxww8oz5M2rqCpqhaYwkkP4o5v6C5qS1dAiWiQZx7mokWggsHad19NMl5dbj9SOq2aQZFopZA11am3a4ys6Amt_7z'}
    # url
    url = "https://fcm.googleapis.com/fcm/send"
    # 发送请求并接收响应
    response = requests.post(url, data=json.dumps(message_data), headers=headers)
    # 返回响应编码
    pro_logger.info('推送结束 status_code:' + str(response.status_code))
    return response.status_code

