from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from . import models
from .serializers import *


# comment views:

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_comment(request: Request, article_id):
    """this endpoint is to add a comment on an article"""

    print(request.user)
    if not request.user.is_authenticated or not request.user.has_perm('articles.add_comment'):
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)

    request.data.update(user=request.user.id)

    comment = Comment_serializer(data=request.data)
    if comment.is_valid():
        comment.save()
        dataResponse = {
            "msg": "Created Successfully",
            "comment": comment.data
        }
        return Response(dataResponse)
    else:
        print(comment.errors)
        dataResponse = {"msg": "couldn't create a comment"}
        return Response(dataResponse, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_comment(request: Request):
    """this endpoint is to view comments"""
    comment = Comment.objects.all()

    dataResponse = {
        "msg": "List of Comments:",
        "comment": Comment_serializer(instance=comment, many=True).data,
    }

    return Response(dataResponse)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_comment(request: Request, comment_id):
    """this endpoint is for deleting a comment"""
    if not request.user.is_authenticated:
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)

    comment = Comment.objects.get(id=comment_id)
    # Check if the comment by the same user who wrote it
    if comment.users.id == request.user.id:
        comment.delete()
        return Response({"msg": "Deleted Comment Successfully"})
    else:
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_bookmark(request: Request):
    """ This endpoint for adding articles to the user's bookmark  """
    if not request.user.is_authenticated:
        return Response("Not Allowed", status=status.HTTP_400_BAD_REQUEST)

    request.data["user"] = request.user.id
    new_bookmark = BookmarkSerializer(data=request.data)
    if new_bookmark.is_valid():
        new_bookmark.save()
        return Response({"Bookmark": new_bookmark.data})
    else:
        print(new_bookmark.errors)
        return Response("Couldn't add", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def list_bookmark(request: Request):
    """ This endpoint for list all your Bookmark  """
    bookmark = Bookmark.objects.all()

    responseData = {
        "msg": " Bookmark : ",
        "Bookmark": BookmarkSerializer(instance=bookmark, many=True).data
    }
    return Response(responseData)


@permission_classes([IsAuthenticated])
def delete_bookmark(request: Request, bookmark_id):
    """ This endpoint for delete your bookmark """
    bookmark = Bookmark.objects.get(id=bookmark_id)
    bookmark.delete()
    return Response({"msg": "Deleted Successfully"})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def add_article(request: Request):
    ''' This endpoint is for adding an article if the user is a publisher'''

    if not request.user.is_authenticated:
        return Response({'msg': 'Not Allowed!'}, status=status.HTTP_401_UNAUTHORIZED)
    # request.data["publisher"]=request.user.id
    else:
        request.data["publisher"] = request.user.id
        article = ArticleSerializer(data=request.data)
        if article.is_valid():
            article.save()
            dataResponse = {
                'msg': 'article Added Successfully',
                'article': article.data
            }
            return Response(dataResponse)
        else:
            print(article.errors)
            dataResponse = {'msg': 'Unable to add article'}
            return Response(dataResponse, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_article(request: Request, article_id):
    ''' This endpoint is for updating an article '''
    if not request.user.is_authenticated:
        return Response({'msg': 'Not Allowed'}, status=status.HTTP_401_UNAUTHORIZED)

    article = Article.objects.get(id=article_id)
    if request.user.id == article.publisher:
        article_updated = ArticleSerializer(instance=article, data=request.data)
        if article_updated.is_valid():
            article_updated.save()
            responseData = {'msg': 'Article Updated Successfully'}
            return Response(responseData)
    else:
        return Response({'msg': 'User Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_article(request: Request, article_id):
    ''' This endpoint is for deleting an article '''
    if not request.user.is_authenticated:
        return Response({'msg': 'Not Allowed'}, status=status.HTTP_401_UNAUTHORIZED)
    article = Article.objects.get(id=article_id)
    if request.user.id == article.publisher:
        article.delete()
        return Response({'msg': 'Article Deleted Successfully'})
    else:
        return Response({'msg': 'Not Unauthorized User'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def all_articles(request: Request):
    ''' This endpoint is for listing/viewing all articles '''
    article = Article.objects.all()
    dataResponse = {
        'msg': 'List of All Articles',
        'Article': ArticleSerializer(instance=article, many=True).data
    }
    return Response(dataResponse)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def posted_articles_per_publisher(request: Request, publisher_id):
    ''' This endpoint is for viewing articles by a publisher '''
    article = Article.objects.filter(publisher=publisher_id)
    dataResponse = {
        'msg': 'List of All Articles',
        'Articles': ArticleSerializer(instance=article, many=True).data
    }
    return Response(dataResponse)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def posted_articles_per_category(request: Request, category_id):
    ''' This endpoint is for viewing articles by a category '''
    article = Article.objects.filter(category=category_id)
    dataResponse = {
        'msg': 'List of All Articles in a Category',
        'Articles': ArticleSerializer(instance=article, many=True).data
    }
    return Response(dataResponse)

@api_view(['GET'])
def search_for_article (request: Request, article_title):
    """ This endpoint for searching article by title  """

    search_article = Article.objects.filter(title__contains=article_title.lower())

    article_info = ArticleSerializer(instance=search_article, many=True).data
    if article_info:
        dataResponse = {
            "Article": article_info
        }
        return Response(dataResponse)
    else:
        print(article_info.errors)
        return Response({"msg": "couldn't find the article"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def top5_Article(request: Request):
    """ This endpoint for list the top 5 Articles by Likes """
    top = Article.objects.order_by('-likes')[:5]
    dataResponse = {
        "msg": "List of Top 5 Articles ",
        "TOP_5": ArticleSerializer(instance=top, many=True).data
    }
    return Response(dataResponse)
