from rest_framework import serializers

from noticeboard.models import Post


class NoticeboardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'
