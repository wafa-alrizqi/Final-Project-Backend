from django.shortcuts import render

# Create your views here



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_Bookmark(request: Request):
    """ This endpoint for adding comics for yor favorite  """
    if not request.user.is_authenticated or not request.user.has_perm('ArticlesApp.add_Bookmark'):
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
def list_Bookmark(request: Request):
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
def delete_Bookmark(request: Request, bookmark_id):
    """ This endpoint for delete bookmark """
    bookmark = Bookmark.objects.get(id=bookmark_id)
    bookmark.delete()
    return Response({"msg": "Deleted Successfully"})

@api_view(['GET'])
def search_for_article(request: Request):
    """ This endpoint for searching article by title  """
    if request.method == 'GET':
        artical = Article.objects.all()
        title = request.GET.get('title', None)
        if title is not None:
            search_s = Article.objects.filter(title=title)
            search_article = {
                "Article": ArticleSerializerView(instance=search_s, many=True).data
            }
            return Response(search_article)
    return Response("non")


@api_view(['GET'])
def top5_Artical(request: Request):
    """ This endpoint for list the top 5 Articals by Likes """
    top = Artical.objects.order_by('-likes')[:5]

    dataResponse = {
        "msg": "List of Top 5 Articals ",
        "TOP_5": ArticalSerializer(instance=top, many=True).data
    }
    return Response(dataResponse)