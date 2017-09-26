
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.generic import View
from django.core import serializers

from datetime import datetime, time, timedelta
from dateutil import parser as DateUtilParser, tz
from django.utils import timezone

from BetProsApp.models import *

import json


class LoginView(View):

    def get(self, request):
        """Get request for the login page"""
        # Check if user is logged in... If logged in show the dashboard
        return render(request, 'login.html', {})    # Blank context for the meantime

    def post(self, request):
        """User is trying to login"""
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        success = True
        message = 'Login successful!'

        if email is None or password is None:
            """Login credentials missing. Return json with error message"""
            message = 'Missing login credentials.'
            success = False
        else:
            user = authenticate(username=email, password=password)
            if user is None:
                """Authentication failed"""
                message = 'Incorrect username or password.'
                success = False
            else:
                """Authentication success, check if user is active"""
                if not user.is_active:
                    """User is inactive. Return activation message """
                    message = 'Activate your account. Follow instructions sent to ' + email + ' to activate your account.'
                    success = False
                else:
                    """User is active. Proceed to login"""
                    login(request, user)

        context = {'message': message}
        """Return json data"""
        if success:
            return JsonResponse(json.dumps(context), safe=False, status=200)
        else:
            return JsonResponse(json.dumps(context), safe=False, status=500)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('login')


class RegistrationView(View):

    def post(self, request):
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirm_password', None)
        success = True
        message = 'Login successful!'
        if email is None or password is None or confirm_password is None:
            message = 'Missing credentials.'
            success = False
        elif password != confirm_password:
            message = 'Passwords do not match.'
            success = False
        if User.objects.filter(email__exact=email).count() > 0:
            message = 'The email {} is already taken. Try a different email address.'.format(email)
            success = False
        else:
            user = User.objects.create_superuser(email, email, password)
            user.is_active = True
            request.user = user
        context = {'message': message}
        """Return json data"""
        if success:
            return JsonResponse(json.dumps(context), safe=False, status=200)
        else:
            return JsonResponse(json.dumps(context), safe=False, status=500)


class DashboardView(View):
    """What you see when you first log into the application"""

    def get(self, request):
        if not request.user.is_authenticated():
            """User not authenticated... Redirect to login page"""
            print request.user
            return redirect('login')
        leagues = League.objects.all()
        matches = Match.objects.filter(complete=False)
        sports = Sport.objects.all()
        context = {
            'user': request.user,
            'sports': sports,
            'leagues': leagues,
            'matches': matches,
            'popular_view': True
        }
        return render(request, 'plain_page.html', context)  # Empty context for the meantime


def gentella_html(request):
    context = {}
    # The template to be loaded as per BetPros.
    # All resource paths for BetPros end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template(load_template)
    return HttpResponse(template.render(context, request))


class MatchListJSONView(View):

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

    def get(self, request):
        synced = True
        message = ''
        match_count = 0
        match_list = Match.objects.none().values('league', 'home_team', 'home_team_odds', 'away_team_odds',
                                                 'match_date', 'match_time', 'prediction', 'result', 'complete')

        raw_sync_datetime  = request.GET.get('last_sync_datetime', None)  # Please remember to deserialize date
        local_timezone = tz.tzlocal()
        last_sync_datetime = None if raw_sync_datetime is None else datetime.strptime(raw_sync_datetime, '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=local_timezone)
        last_created_match = Match.objects.latest('created_at')
        last_updated_match = Match.objects.latest('updated_at')
        if self.sync_required(last_created_match.created_at, last_updated_match.updated_at, last_sync_datetime):
            """Sync is required"""
            start_date = datetime.now()-timedelta(days=1)
            end_date = datetime.now() + timedelta(days=2)
            match_list = Match.objects.filter(match_date__range=(start_date, end_date), complete=False).values('league', 'home_team', 'home_team_odds', 'away_team', 'away_team_odds',
                                       'match_date', 'match_time', 'prediction', 'result', 'complete')
            match_count = match_list.count()
            message = 'Match list synced'
            pass
        else:
            """Sync is not required"""
            synced = False
            message = 'Match list up to date'
            pass

        json_match_list = []
        for match in match_list:
            json_match_list.append(match)

        context = {
            'synced': synced,
            'message': message,
            'match_count': match_count,
            'json_match_list': serializers.serialize('json', json_match_list),
            'last_sync_datetime': datetime.now(tz=local_timezone).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        }

        return JsonResponse(json.dumps(context), safe=True, status=200)
