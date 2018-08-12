from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import BookmarkCollection
from ..serializers.collection import BookmarkCollectionSerializer

from utils.exceptions.get_object_or_404 import get_object_or_404_customed

User = get_user_model()


class BookmarkCollectionListCreateAPIView(APIView):

    def post(self, request, pk):
        pass

    def get(self, request, pk):
        user = get_object_or_404_customed(User, pk=pk)
        bookmarkcollections = BookmarkCollection.objects.all().filter(user=user)
        serailizer = BookmarkCollectionSerializer(bookmarkcollections, many=True)
        return Response(serailizer.data)
