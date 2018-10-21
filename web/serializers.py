from rest_framework import serializers
from web.models import Content


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id','title','content', 'author', 'email','menu','imageDir','imageFileName','countLike','countDisLike',,'approved','create_date','release_date','updated_by')


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id','title', 'author', 'email','menu','imageDir','photoList','countLike','countDisLike','approved','create_date','release_date','updated_by')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id','comment','create_date','approved','updated_by'.'content')
