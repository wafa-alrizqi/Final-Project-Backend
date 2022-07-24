from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from . import models
from .serializer import *
# Create your views her

#comment views:


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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def view_comment(request: Request):
    """this endpoint is to view comments"""
    comment = Comment.objects.all()

    dataResponse = {
        "msg": "List of Comments:",
        "comment": Comment_serializer(instance=comment, many=True).data,
    }

    return Response(dataResponse)
