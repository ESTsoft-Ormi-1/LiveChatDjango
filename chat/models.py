from django.db import models
from django.conf import settings
from mysite.json_extended import ExtendedJSONEncoder, ExtendedJSONDecoder
from post.models import Post

class OnlineUserMixin(models.Model):

    class Meta:
        abstract = True

    online_user_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="RoomMember",
        blank=True,
        related_name="joined_room_set",
    )

    def get_online_users(self):
        return self.online_user_set.all()
    
    def get_online_usernames(self):
        qs = self.get_online_users().values_list("username", flat=True)
        return list(qs)
    
    def is_joined_user(self, user):
        return self.get_online_users().filter(pk=user.pk).exists()
    
    def user_join(self, channel_name, user):
        try:
            room_member = RoomMember.objects.get(room=self, user=user)
        except RoomMember.DoesNotExist:
            room_member = RoomMember(room=self, user=user)

        is_new_join = len(room_member.channel_names) == 0
        room_member.channel_names.add(channel_name)

        if room_member.pk is None:
            room_member.save()
        else:
            room_member.save(update_fields=["channel_names"])
        
        return is_new_join
    
    def user_leave(self, channel_name, user):
        try:
            room_member = RoomMember.objects.get(room=self, user=user)
        except RoomMember.DoesNotExist:
            return True
        
        room_member.channel_names.remove(channel_name)
        if not room_member.channel_names:
            room_member.delete()
            return True
        else:
            room_member.save(update_fields=["channel_names"])
            return False


class Room(OnlineUserMixin, models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

    @property
    def chat_group_name(self):
        return self.make_chat_group_name(room=self)

    @staticmethod
    def make_chat_group_name(room=None, room_pk=None):
        return "chat-%s" % (room_pk or room.pk)


class Chat(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    parent_chat = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message_type = models.CharField(max_length=45, null=True)
    
    def __str__(self):
        return self.message


class RoomMember(models.Model):
    room = models.ForeignKey("Room", on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    channel_names = models.JSONField(
        default=set,
        encoder=ExtendedJSONEncoder,
        decoder=ExtendedJSONDecoder,
    )
