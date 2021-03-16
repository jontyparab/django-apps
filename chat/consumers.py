import json
import html
import urllib.parse
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from chat.models import Friend


class ChatRoomConsumer(AsyncWebsocketConsumer):
    # username is specific for every user who makes it. Kinda like the admin of a discord server.
    # user_group_name is collection of two users or two usernames to be precise (since private chats).
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']  # username is passed from routing.py :)
        params = urllib.parse.parse_qs(self.scope['query_string'].decode('utf8'))
        recipient = params['recipient'][0]
        print(type(recipient), type(self.username))
        if recipient != "" or self.username != recipient:
            friend_id = await self.get_friendship_helper(recipient)
            if not friend_id: await self.close()  # Friend or/and Friendship Does NOT exist
            self.user_group_name = 'chat_%s' % friend_id
            print("User Channel: {}\nUser Group Name: {}".format(self.username, self.user_group_name))

            await self.channel_layer.group_add(
                self.user_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        print("AAAAAAAAAA")
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )

    # text_data is predefined I guess
    async def receive(self, text_data):
        params = urllib.parse.parse_qs(self.scope['query_string'].decode('utf8'))
        # recipient = params['recipient']
        text_data_json = json.loads(text_data)
        message = html.escape(text_data_json['message'])
        sender = html.escape(text_data_json['sender'])
        recipient = html.escape(text_data_json['recipient'])

        await self.channel_layer.group_send(
            self.user_group_name,
            {
                'type': 'user_group_message',
                'message': message,
                'sender': sender,
                'recipient': recipient
            }
        )

    async def user_group_message(self, event):
        message = event['message']
        sender = event['sender']
        recipient = event['recipient']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'recipient': recipient
        }))

    # Gives The id of the friendship Relation
    @database_sync_to_async
    def get_friendship_helper(self, recipient):
        sender_user = self.scope['user']
        try:
            recipient_user = User.objects.get(username=recipient)
        except ObjectDoesNotExist:
            return False
        try:
            if sender_user.id < recipient_user.id:
                friendship = Friend.objects.get(userone=sender_user.id, usertwo=recipient_user.id)
            else:
                friendship = Friend.objects.get(userone=recipient_user.id, usertwo=sender_user.id)
        except ObjectDoesNotExist:
            return False
        print("FRIENDSHIP HELPER RAN: {}\n".format(friendship.id))
        return str(friendship.id)

    pass

    # @database_sync_to_async
    # def get_user_info(self, recipient):
    #     sender, recipient = str(self.scope['user']) or '', str(recipient) or ''
    #     chats = []
    #     if recipient:
    #         sender_chats = requests.get('http://localhost:3000/' + str(self.scope['user']) + '/').json()
    #         recipient_chats = requests.get('http://localhost:3000/' + str(recipient) + '/').json()
    #         pass
    #         # mixed_chats = sender_chats | recipient_chats
    #         # chats = [chat for chat in mixed_chats if
    #         #          (chat['sender'] == sender and chat['recipient'] == recipient) or (
    #         #                  chat['recipient'] == sender and chat['sender'] == recipient)]
    #     print("Sender: {}\nReceiver: {}\nAll: {}".format(chats, sender_chats, recipient_chats))
    #     return chats
    #
    # @database_sync_to_async
    # def post_new_messages(self, recipient):
    #     new = {}
    #     all_chats = requests.post('http://localhost:3000/' + str(self.scope['user']) + '/').json()
    #     sender, recipient = str(self.scope['user']) or '', str(recipient) or ''
    #     chats = []
    #     if recipient:
    #         sender_chats = all_chats[sender]
    #         recipient_chats = all_chats[recipient]
    #         mixed_chats = sender_chats + recipient_chats
    #         chats = [chat for chat in mixed_chats if
    #                  (chat['sender'] == sender and chat['recipient'] == recipient) or (
    #                          chat['recipient'] == sender and chat['sender'] == recipient)]
    #     print("All: {}".format(chats))
    #     return chats
