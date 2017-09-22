from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Region(models.Model):
    name = models.CharField(verbose_name='Name', max_length=250, blank=False, null=False, default='')
    description = models.TextField(verbose_name='Description', max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'


class Country(models.Model):
    name = models.CharField(verbose_name='Name', max_length=250, blank=False, null=False, default='')
    description = models.TextField(verbose_name='Description', max_length=500)
    region = models.ForeignKey(Region, verbose_name='Region', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class Sport(models.Model):
    icon = models.CharField(verbose_name='Icon', max_length=250, blank=True, null=True)
    image = models.CharField(verbose_name='Image', max_length=250, blank=True, null=True)
    name = models.CharField(verbose_name='Name', max_length=250, blank=True, null=True)
    description = models.TextField(verbose_name='Description', max_length=500)

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    class Meta:
        verbose_name = 'Sport'
        verbose_name_plural = 'Sports'


class League(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False, default='')
    description = models.TextField(max_length=750, blank=True, null=True)
    region = models.ForeignKey(Region, verbose_name='Region', blank=True, null=True)
    sport = models.ForeignKey(Sport, verbose_name='Sport', blank=True, null=True)
    in_popular_list = models.BooleanField(verbose_name='In popular list', blank=False, null=False, default=False)

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_league_length(self):
        return Match.objects.filter(league=self,complete=False).count()

    class Meta:
        verbose_name = 'League'
        verbose_name_plural = 'Leagues'


class Club(models.Model):
    name = models.CharField(verbose_name='Name', max_length=250, blank=False, null=False)
    short_name = models.CharField(verbose_name='Short name', max_length=150, blank=True, null=True)
    league = models.ForeignKey(League, verbose_name='League', blank=False, null=False)
    stadium = models.CharField(verbose_name='Stadium', max_length=250, blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name='Country', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_league(self):
        return self.league.name

    class Meta:
        verbose_name = 'Club'
        verbose_name_plural = 'Clubs'


class MatchResult(models.Model):
    name = models.CharField(verbose_name='Name', max_length=250, blank=False, null=False, default='')
    description = models.TextField(verbose_name='Description', blank=True, null=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Match Result'
        verbose_name_plural = 'Match Results'


class Match(models.Model):
    league = models.ForeignKey(League, verbose_name='League', blank=False, null=False)
    home_team = models.ForeignKey(Club, verbose_name='Home Team', blank=True, null=True, related_name='+')
    home_team_odds = models.FloatField(verbose_name='Home team odds', blank=True, null=True)
    away_team = models.ForeignKey(Club, verbose_name='Away Team', blank=True, null=True, related_name='+')
    away_team_odds = models.FloatField(verbose_name='Away team odds', blank=True, null=True)
    match_date = models.DateField(verbose_name='Date', blank=True, null=True)
    match_time = models.TimeField(verbose_name='Time', blank=True, null=True)
    prediction = models.ForeignKey(MatchResult, verbose_name='Prediction', blank=True, null=True, related_name='+')
    result = models.ForeignKey(MatchResult, verbose_name='Result', blank=True, null=True, related_name='+')
    complete = models.BooleanField(verbose_name='Complete', blank=False, null=False, default=False)

    def __str__(self):
        return self.get_prediction_name()

    def get_league(self):
        return self.league.name

    def get_home_team_name(self):
        return self.home_team.name

    def get_away_team_name(self):
        return self.away_team.name

    def get_prediction_name(self):
        return self.prediction.name

    class Meta:
        verbose_name = 'Match'
        verbose_name_plural = 'Matches'



