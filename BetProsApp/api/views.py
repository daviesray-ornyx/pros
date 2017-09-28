from __future__ import unicode_literals
from django.db.models import Q
from rest_framework import status

from rest_framework.response import Response

from rest_framework.generics import (ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.views import APIView

from BetProsApp.api.serializers import *

from datetime import datetime, time, timedelta
from dateutil import parser as DateUtilParser, tz
from django.utils import timezone


class MatchListAPIView(ListAPIView):
    serializer_class = MatchSerializer

    def sync_required(self, last_create_datetime, last_update_datetime, last_sync_datetime):
        if last_sync_datetime is None:
            """No sync datetime value passed"""
            return True
        """Sync datetime value passed"""
        if last_sync_datetime > last_create_datetime and last_sync_datetime > last_update_datetime:
            """Update not required"""
            return False
        else:
            return True

    def get_queryset(self, *args, **kwargs):
        # queryset = Match.objects.none();
        # raw_sync_datetime = self.request.GET.get('last_sync_datetime', None)  # Please remember to deserialize date
        # local_timezone = tz.tzlocal()
        # last_sync_datetime = None if raw_sync_datetime is None else datetime.strptime(raw_sync_datetime, '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=local_timezone)
        # last_created_match = Match.objects.latest('created_at')
        # last_updated_match = Match.objects.latest('updated_at')
        """Sync process"""
        start_date = datetime.now() - timedelta(days=1)
        end_date = datetime.now() + timedelta(days=2)
        queryset = Match.objects.filter(match_date__range=(start_date, end_date), complete=False)
        return queryset


class BettingTipListAPIView(ListAPIView):
    serializer_class = BettingTipSerializer
    """
        Retrieves the latest Betting Tip
    """

    def get_queryset(self, *args, **kwargs):
        latest_betting_tip = BettingTip.objects.latest('created_at')
        queryset = BettingTip.objects.filter(pk=latest_betting_tip.pk)
        return queryset

