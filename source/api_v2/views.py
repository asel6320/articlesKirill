from django.http import HttpResponse, HttpResponseNotAllowed

from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v2.serializers import ArticleSerializer, CommentSerializer
from webapp.models import Article, Comment


# Create your views here.
@ensure_csrf_cookie
def get_csrf_token(request):
    if request.method == 'GET':
        return HttpResponse()
    else:
        return HttpResponseNotAllowed(permitted_methods=["GET"])


class ArticleView(APIView):
    def get(self, request, *args, pk=None, **kwargs):
        if pk:
            article = get_object_or_404(Article, pk=pk)
            serializer = ArticleSerializer(article)
            return Response(serializer.data, status=status.HTTP_200_OK)
        articles = Article.objects.order_by('-created_at')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        request_data = request.data.copy()
        request_data["test_id"] = 1
        serializer = ArticleSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        article = serializer.save()
        article_data = ArticleSerializer(article).data
        return Response(article_data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, pk=None, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(data=request.data, instance=article)
        serializer.is_valid(raise_exception=True)
        article = serializer.save()
        article_data = ArticleSerializer(article).data
        return Response(article_data, status=status.HTTP_200_OK)

    def delete(self, request, *args, pk=None, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response({"id": pk}, status=status.HTTP_204_NO_CONTENT)

class CommentView(APIView):
    def get(self, request, *args, article_id=None, pk=None, **kwargs):
        if pk:
            comment = get_object_or_404(Comment, pk=pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif article_id:
            comments = Comment.objects.filter(article_id=article_id)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, article_id=None, **kwargs):
        article = get_object_or_404(Article, pk=article_id)
        request_data = request.data.copy()
        request_data["article"] = article.id
        request_data["author"] = request.user.id
        serializer = CommentSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        comment_data = CommentSerializer(comment).data
        return Response(comment_data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, pk=None, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        comment_data = CommentSerializer(comment).data
        return Response(comment_data, status=status.HTTP_200_OK)

    def delete(self, request, *args, pk=None, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response({"id": pk}, status=status.HTTP_204_NO_CONTENT)