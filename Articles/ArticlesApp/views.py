from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import *


# comment views:

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_comment(request: Request, article_id):
    """this endpoint is to add a comment on an article"""
    if not request.user.is_authenticated:
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        comment = Comment_serializer(data=request.data)
        request.data["article"] = article_id
        request.data["user"] = request.user.id

        if comment.is_valid():
            print(request.user.username)
            comment.save()
            dataResponse = {
                "msg": "Created Successfully",
                "comment": comment.data
            }
            return Response(dataResponse)
        else:
            print(request.user.id)
            print(comment.errors)
            dataResponse = {'msg': 'Unable to Add Comment'}
            return Response(dataResponse, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_comment(request: Request, article_id):
    """this endpoint is to view comments"""
    # comment = Comment.objects.all()
    # dataResponse = {
    #     "msg": "List of Comments:",
    #     "comment": Comment_serializer(instance=comment, many=True).data,
    # }
    # return Response(dataResponse)
    comments = Comment.objects.filter(article=article_id)
    dataResponse = {
        'msg application': 'List of Comments in each Article',
        'application': Comment_serializer(instance=comments, many=True).data
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
    if comment.user.id == request.user.id:
        comment.delete()
        return Response({"msg": "Deleted Comment Successfully"})
    else:
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)




@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def add_bookmark(request: Request, article_id):
    """ This endpoint for adding articles to the user's bookmark  """
    if not request.user.is_authenticated:
        return Response("Not Allowed", status=status.HTTP_400_BAD_REQUEST)

    request.data["user"] = request.user.id
    articleId= Article.objects.get(id=article_id)

    if Bookmark.objects.filter(user=request.user.id, article=articleId).exists():
        return Response({"msg": "you already have added this article"}, status=status.HTTP_400_BAD_REQUEST)
    user_request = User.objects.get(id=request.user.id)

    create_bookmark = Bookmark.objects.create(article=articleId,user=user_request)
    new_bookmark=BookmarkSerializer.data

    if new_bookmark.is_valid():
        new_bookmark.save()
        return Response({"Bookmark": new_bookmark})
    else:
        print(new_bookmark.errors)
        return Response("Couldn't add to Bookmark", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def list_bookmark(request: Request):
    """ This endpoint for list all your Bookmark  """
    bookmark = Bookmark.objects.filter(user=request.user.id)
    print(request.user.id)
    responseData = {
        "msg": " Bookmark : ",
        "Bookmark": BookmarkArticlesSerializer(instance=bookmark, many=True).data
    }
    return Response(responseData)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_bookmark(request: Request, bookmark_id):
    """ This endpoint for delete your bookmark """
    if not request.user.is_authenticated:
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        request.data.update(user=request.user.id)
        bookmark = Bookmark.objects.get(id=bookmark_id)
        if bookmark.user.id == request.user.id:
            bookmark.delete()
            return Response({"msg": "Deleted bookmark Successfully"})
        else:
            return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({"msg": "Could not delete the bookmark not found "}, status=status.HTTP_404_NOT_FOUND)




@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def add_article(request: Request):
    """ This endpoint is for adding an article if the user is a publisher"""

    if not request.user.is_authenticated:
        return Response({'msg': 'Not Allowed!'}, status=status.HTTP_401_UNAUTHORIZED)

    else:
        article = ArticleSerializer(data=request.data)
        request.data["publisher"] = request.user.id
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


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def add_ArticleLike(request: Request, article_id):
    """ This endpoint is for adding a like for an article if the user is logged in"""

    if not request.user.is_authenticated:
        return Response({'msg': 'Not Allowed!'}, status=status.HTTP_401_UNAUTHORIZED)

    else:
        article = Article.objects.get(id=article_id)
        add_like = ArticleLikesSerializer(instance=article, data=request.data)
        if add_like.is_valid():
            add_like.save()
            dataResponse = {
                'msg': 'Article like Added Successfully',
                'article': add_like.data
            }
            return Response(dataResponse)
        else:
            print(add_like.errors)
            dataResponse = {'msg': 'Unable to add like article'}
            return Response(dataResponse, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_article(request: Request, article_id):
    """ This endpoint is for updating an article """
    if not request.user.is_authenticated:
        return Response({'msg': 'Not Allowed'}, status=status.HTTP_401_UNAUTHORIZED)

    article = Article.objects.get(id=article_id)
    if request.user.id == article.publisher.id:
        article_updated = ArticleSerializer(instance=article, data=request.data)
        request.data["publisher"] = request.user.id
        if article_updated.is_valid():
            article_updated.save()
            responseData = {'msg': 'Article Updated Successfully'}
            return Response({'msg': 'Article Updated Successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'msg': 'User Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_article(request: Request, article_id):
    """ This endpoint is for deleting an article """
    if not request.user.is_authenticated:
        return Response({'msg': 'Not Allowed'}, status=status.HTTP_401_UNAUTHORIZED)
    article = Article.objects.get(id=article_id)
    if request.user.id == article.publisher.id:
        article.delete()
        return Response({'msg': 'Article Deleted Successfully'})
    else:
        print(request.user.id)
        print(article.publisher.id)
        return Response({'msg': 'Not Unauthorized User'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def all_articles(request: Request):
    """ This endpoint is for listing/viewing all articles """
    article = Article.objects.all()
    dataResponse = {
        'msg': 'List of All Articles',
        'Article': ArticlePublisherSerializer(instance=article, many=True).data
    }
    return Response(dataResponse)


@api_view(['GET'])
def article_details(request: Request, article_id):
    """ This endpoint is for listing/viewing all articles """
    article = Article.objects.filter(id=article_id)
    dataResponse = {
        'msg': 'Article Details',
        'Article': ArticlePublisherSerializer(instance=article, many=True).data
    }
    return Response(dataResponse)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def posted_articles_per_publisher(request: Request):
    """ This endpoint is for viewing articles by a publisher """
    article = Article.objects.filter(publisher=request.user.id)
    dataResponse = {
        'msg': 'List of All Articles',
        'Articles': ArticleSerializer(instance=article, many=True).data
    }
    return Response(dataResponse)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def posted_articles_per_category(request: Request, category_id):
    """ This endpoint is for viewing articles by a category """
    article = Article.objects.filter(category=category_id)
    dataResponse = {
        'msg': 'List of All Articles in a Category',
        'Articles': ArticleSerializer(instance=article, many=True).data
    }
    return Response(dataResponse)


@api_view(['GET'])
def top5_Article(request: Request):
    """ This endpoint for list the top 5 Articles by Likes """
    top = Article.objects.order_by('-likes')[:5]
    dataResponse = {
        "msg": "List of Top 5 Articles ",
        "TOP_5": ArticleSerializer(instance=top, many=True).data
    }
    return Response(dataResponse)


@api_view(['GET'])
def search_for_article(request: Request):
    """ This endpoint for searching Article by title  """
    if request.method == 'GET':
        art = Article.objects.all()
        title = request.GET.get('title', None)
        if title is not None:
            search_s = Article.objects.filter(title__icontains=title.lower())
            search_art = {
                "Article": ArticleSerializer(instance=search_s, many=True).data
            }
            return Response(search_art)
    return Response("non")


@api_view(['GET'])
def all_categories(request: Request):
    """ This endpoint is for listing/viewing all articles """
    category = Category.objects.all()
    dataResponse = {
        'msg': 'List of All Categories',
        'Categories': CategorySerializer(instance=category, many=True).data
    }
    return Response(dataResponse)


# Favourite Category views:


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def add_favCategory(request: Request, category_id):
    """ This endpoint for adding categories to the user's Favourite Category  """


    request.data["user"] = request.user.id
    category_id = Category.objects.get(id=category_id)

    if FavouiteCatgory.objects.filter(user=request.user.id, category=category_id).exists():
        return Response({"msg": "you already have added this category"}, status=status.HTTP_400_BAD_REQUEST)

    user_request = User.objects.get(id=request.user.id)

    create_favCategory = FavouiteCatgory.objects.create(category=category_id, user=user_request)
    new_favCategory = FavouiteCatgoriesSerializer.data

    if new_favCategory.is_valid():
        new_favCategory.save()
        return Response({"Favouites": new_favCategory})
    else:
        print(new_favCategory.errors)
        return Response("Couldn't add to Bookmark", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def list_favCategory(request: Request):
    """ This endpoint for list all your Favouite Catgories  """

    favCategory = FavouiteCatgory.objects.filter(user=request.user.id)
    print(request.user.id)
    responseData = {
        "msg": " Favouites : ",
        "Favouites": FavouiteCatgoriesSerializer(instance=favCategory, many=True).data
    }
    return Response(responseData)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_favCategory(request: Request, favCategory_id):
    """ This endpoint for delete your bookmark """

    if not request.user.is_authenticated:
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        request.data.update(user=request.user.id)
        del_favCategory = FavouiteCatgory.objects.get(id=favCategory_id)
        if del_favCategory.user.id == request.user.id:
            del_favCategory.delete()
            return Response({"msg": "Deleted Favouite Catgory Successfully"})
        else:
            return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({"msg": "Could not delete the Favouite Catgory not found "}, status=status.HTTP_404_NOT_FOUND)
