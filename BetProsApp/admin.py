from __future__ import unicode_literals
from django.contrib import admin
from BetProsApp.models import *


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


admin.site.register(Region, RegionAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


admin.site.register(Country, CountryAdmin)


class SportAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'image', 'description')
    search_fields = ('name',)


admin.site.register(Sport, SportAdmin)


class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'sport', 'description', 'in_popular_list')
    search_fields = ('name', 'region', 'sport')


admin.site.register(League, LeagueAdmin)


class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'league', 'stadium')
    search_fields = ('name', 'short_name', 'league', 'stadium')


admin.site.register(Club, ClubAdmin)


class MatchResultAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


admin.site.register(MatchResult, MatchResultAdmin)


class MatchAdmin(admin.ModelAdmin):
    list_display = ('league', 'home_team_odds', 'away_team_odds', 'match_date', 'match_time',
                    'prediction', 'result')
    search_fields = ('league', 'match_date')


admin.site.register(Match, MatchAdmin)
