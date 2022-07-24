from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from . import models
from .serializers import *


# Create your views her

# comment views:


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_comment(request: Request, article_id):
    """this endpoint is to add a comment"""
    print(request.user)
    # if not request.user.is_authenticated or not request.user.has_perm('consultation.add_consultation_request'):
    #     return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)

    # request.data.update(user=request.user.id)

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
    con = Comment.objects.get(id=comment_id)
    con.delete()
    return Response({"msg": "Deleted Successfully"})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def add_article(request: Request):
    if not request.user.is_authenticated:
        return Response({'msg': 'Not Allowed!'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
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
        return Response({'msg': 'Not Unauthorized User'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_article(request: Request, article_id):
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
    article = Article.objects.all()
    dataResponse = {
        'msg': 'List of All Articles',
        'Article': ArticleSerializer(instance=article, many=True).data
    }
    return Response(dataResponse)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def posted_articles_per_publisher(request: Request, publisher_id):
    article = Article.objects.filter(publisher=publisher_id)
    dataResponse = {
        'msg': 'List of All Articles',
        'Articles': ArticleSerializer(instance=article, many=True).data
    }
    return Response(dataResponse)

