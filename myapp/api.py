from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from .models import SearchHistory


class CitySearchCountAPIView(APIView):

    def get(self, request):
        search_counts = SearchHistory.objects.values('query').annotate(count=Count('query')).order_by('-count')
        return Response(search_counts)
