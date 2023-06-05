from rest_framework import viewsets

from .serializers import TagSerializer
from .models import Tag


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Набор представлений для просмотра тегов
    """

    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def list(self, request, *args, **kwargs):
        self.pagination_class = None
        return super().list(request, *args, **kwargs)
