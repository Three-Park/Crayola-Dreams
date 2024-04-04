# import jwt
# from rest_framework import status, viewsets
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Follow
from .serializers import FollowSerializer

from .serializers import *
from fairy_tairy.permissions import *

class FollowViewSet(GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin):
    
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        followee = serializer.validated_data.get('following_user')
        if followee==request.user:
            return Response({"message": f"Cannot Follow yourself, {followee.username}."}, status=status.HTTP_400_BAD_REQUEST)
            
        follow_request, created = Follow.objects.get_or_create(follower=request.user, following_user=followee)

        if created:
            return Response({"message": f"Follow request sent to {followee.username}"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"Follow request already sent to {followee.username}"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Follow request deleted"}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = Follow.ACCEPTED
        instance.save()
        return Response({"message": "Follow request accepted"}, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = Follow.REJECTED
        instance.save()
        return Response({"message": "Follow request rejected"}, status=status.HTTP_200_OK)
        
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
    
    
# class ProfileAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ProfileSerializer
    
#     def get(self, request):
#         user = request.user
#         print(request.user)
#         serializer = self.serializer_class(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request):
#         user = request.user
#         serializer = self.serializer_class(user, data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)