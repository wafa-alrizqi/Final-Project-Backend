from django.shortcuts import render
<<<<<<< HEAD

# Create your views here

=======
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

def delete_comment(request: Request, comment_id):
    """this endpoint is for deleting a comment"""
    con = Comment.objects.get(id=comment_id)
    con.delete()
    return Response({"msg": "Deleted Successfully"})



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_bookmark(request: Request):
    """ This endpoint for adding comics for yor favorite  """
    if not request.user.is_authenticated or not request.user.has_perm('ArticlesApp.add_bookmark'):
        return Response("Not Allowed", status=status.HTTP_400_BAD_REQUEST)

    request.data["user"] = request.user.id
    new_bookmark = BookmarkSerializer(data=request.data)
    if new_bookmark.is_valid():
        new_bookmark.save()
        return Response({"Bookmark": new_bookmark.data})
    else:
        print(new_bookmark.errors)
        return Response("no", status=status.HTTP_400_BAD_REQUEST)



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


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_bookmark(request: Request, bookmark_id):
    """ This endpoint for delete bookmark """
    bookmark = Bookmark.objects.get(id=bookmark_id)
    bookmark.delete()
    return Response({"msg": "Deleted Successfully"})


@api_view(['GET'])
def search_for_article(request: Request):
    """ This endpoint for searching article by title  """
    if request.method == 'GET':
        article = Article.objects.all()
        title = request.GET.get('title', None)
        if title is not None:
            search_s = Article.objects.filter(title=title)
            search_article = {
                "Article": ArticleSerializer(instance=search_s, many=True).data
            }
            return Response(search_article)
    return Response("non")


@api_view(['GET'])
def top5_Article(request: Request):
    """ This endpoint for list the top 5 Articles by Likes """
    top = Article.objects.order_by('-likes')[:5]
    dataResponse = {
        "msg": "List of Top 5 Articles ",
        "TOP_5": ArticleSerializer(instance=top, many=True).data
    }
    return Response(dataResponse)


