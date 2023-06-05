from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination

from .models import Subscription
from .serializers import SubscriptionSerializer


User = get_user_model()

class SubscriptionsView(viewsets.ViewSet):
    """
    Набор представлений для подписки, отписки и получения подписок
    """
    pagination_class = LimitOffsetPagination
    page_size = 6

    permission_classes = [IsAuthenticated,]

    @action(methods=['GET'], detail=False, url_path='subscriptions')
    def get_subscribers(self, request):
        paginator = self.pagination_class()
        user = request.user
        authors = User.objects.filter(subscribers__in=Subscription.objects.filter(user=user))
        result_page = paginator.paginate_queryset(authors, request)
        serializer = SubscriptionSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


    @action(methods=['POST', 'DELETE'], detail=True, url_path='subscribe')
    def subscribe(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        subscription = Subscription.objects.filter(user=request.user, author=author)

        if request.method == 'POST':

            if author == request.user:
                return Response(data='Подписываться на себя нельзя', status=status.HTTP_400_BAD_REQUEST)
            
            if subscription:
                return Response(data='Уже подписан', status=status.HTTP_400_BAD_REQUEST)
            
            Subscription.objects.create(user=request.user, author=author)
            return Response(
                data=SubscriptionSerializer(author).data,
                status=status.HTTP_200_OK
            )
        
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(data='Нет в подписках', status=status.HTTP_400_BAD_REQUEST)
    
