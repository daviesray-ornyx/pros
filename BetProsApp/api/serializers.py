from rest_framework.serializers import ModelSerializer, StringRelatedField

from BetProsApp.models import (Region, Country, Sport, League, Club, MatchResult, Match)


class RegionSerializer(ModelSerializer):

    class Meta:
        model = Region
        fields = ['name', 'description']


class CountrySerializer(ModelSerializer):

    region = StringRelatedField(many=False)

    class Meta:
        model = Country
        fields = ['name', 'description', 'region']


class SportSerializer(ModelSerializer):

    class Meta:
        model = Sport
        fields = ['icon', 'image', 'name', 'description']


class LeagueSerializer(ModelSerializer):
    region = StringRelatedField(many=False)
    sport = StringRelatedField(many=False)

    class Meta:
        model = League
        fields = ['name', 'description', 'region', 'sport', 'in_popular_list',]


class ClubSerializer(ModelSerializer):
    league = StringRelatedField(many=False)
    country = StringRelatedField(many=False)

    class Meta:
        model = Club
        fields = ['name', 'name_short', 'league', 'country', 'stadium']


class MatchResultSerializer(ModelSerializer):

    class Meta:
        model = MatchResult
        fields = ['name', 'description', ]


class MatchSerializer(ModelSerializer):
    league = StringRelatedField(many=False)
    home_team = StringRelatedField(many=False)
    away_team = StringRelatedField(many=False)
    prediction = StringRelatedField(many=False)
    result = StringRelatedField(many=False)

    class Meta:
        model = Match
        fields = ['league', 'home_team', 'home_team_odds', 'away_team', 'away_team_odds', 'match_date', 'match_time',
                  'prediction', 'result', 'complete']


