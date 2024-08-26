from rest_framework import serializers, status

from webapp.models.comment import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "text", "created_at", "updated_at", "author", "article"]
        read_only_fields = ["id", "created_at", "updated_at", "author", "article"]