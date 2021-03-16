from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework.exceptions import NotFound, ParseError

from chat.models import Friend


class Chat(LoginRequiredMixin, View):
    def get(self, request, username=None):
        if request.user.username == username and request.GET.get('recipient') != request.user.username:
            sender = request.user.username
            recipient = request.GET.get('recipient')
            sender_user = request.user
            friendsSet = Friend.objects.filter(Q(userone=sender_user, statususerone=True, statususertwo=True)
                                               | Q(usertwo=sender_user, statususerone=True, statususertwo=True)).distinct()
            friends = []
            for friend in friendsSet:
                if friend.userone.username == sender:
                    friends.append(friend.usertwo.username)
                else:
                    friends.append(friend.userone.username)
            print(friends)
            return render(request, 'chat/chat.html',
                          {'sender': sender, 'recipient': recipient, 'friends': friends})
        return HttpResponseRedirect(self.request.path_info + request.user.username)

    def post(self, request, username):
        friend = request.POST['friend']
        sender_user = request.user

        if sender_user.username != friend:
            try:
                recipient_user = User.objects.get(username=friend)
            except ObjectDoesNotExist:
                messages.error(request, 'User Not Found :(')
                return HttpResponseRedirect(self.request.path_info)

            try:
                if sender_user.id < recipient_user.id:
                    friendship = self.helperFunction(sender_user, recipient_user)
                    friendship.statususerone = True
                    friendship.save()
                else:
                    friendship = self.helperFunction(recipient_user, sender_user)
                    friendship.statususertwo = True
                    friendship.save()
            except AttributeError:
                return HttpResponseRedirect(self.request.path_info)
            messages.success(request, 'Friendship Request Sent!')

        else:
            messages.warning(request, 'You can\'t send friend request to yourself!! (OwO)')

        return HttpResponseRedirect(self.request.path_info)

    def helperFunction(self, sender_user, recipient_user):
        newFriendship = Friend(userone=sender_user, usertwo=recipient_user, statususerone=False, statususertwo=False)
        try:
            friendship = Friend.objects.get(userone=sender_user.id, usertwo=recipient_user.id)
            if friendship.statususerone and friendship.statususertwo:
                messages.info(self.request, 'You are already friends with the person.')
                return None
        except ObjectDoesNotExist:
            return newFriendship
        return friendship

    # def post(self, request, username):
    #     friend = request.POST['friend']
    #     sender_user = request.user
    #
    #     # Horrific Attempt to not repeat entries in Friendship tables, you might be able to do it in a better way
    #     # Logic: userone.id will always be less than usertwo.id
    #     try:
    #         recipient_user = get_object_or_404(User, username=friend)
    #         if sender_user.id < recipient_user.id:
    #             print("IF RAN")
    #             try:
    #                 friendship = Friend.objects.get(userone=sender_user.id, usertwo=recipient_user.id)
    #             except:
    #                 Friend(userone=sender_user, usertwo=recipient_user, statususerone=False, statususertwo=False).save()
    #
    #             friendship.statususerone = True
    #             friendship.save()
    #         elif sender_user.id > recipient_user.id:
    #             print("ELIF RAN")
    #             try: friendship = Friend.objects.get(userone=recipient_user.id, usertwo=sender_user.id)
    #             except: Friend(userone=recipient_user, usertwo=sender_user, statususerone=False, statususertwo=False).save()
    #
    #             friendship.statususertwo = True
    #             friendship.save()
    #
    #     except:
    #         messages.error(request, 'User Not Found :(')
    #         return HttpResponseRedirect(self.request.path_info)
