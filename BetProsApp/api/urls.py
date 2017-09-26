from django.conf.urls import url
from BetProsApp.models import *
from BetProsApp.api.views import *

urlpatterns = [
    url(r'^json_matchlist', MatchListAPIView.as_view(), name='json_matchlist'),
]