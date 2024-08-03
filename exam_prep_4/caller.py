import os
import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import *


def get_tennis_players(search_name=None, search_country=None) -> str:
    if search_name is None and search_country is None:
        return ""

    query = Q()
    if search_name:
        query &= Q(full_name__icontains=search_name)
    if search_country:
        query &= Q(country__icontains=search_country)

    players = TennisPlayer.objects.filter(query).order_by('ranking')

    if not players:
        return ""

    result = [
        f"Tennis Player: {tp.full_name}, country: {tp.country}, ranking: {tp.ranking}"
        for tp in players
    ]

    return '\n'.join(result)


def get_top_tennis_player() -> str:
    player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if not player:
        return ""

    return f"Top Tennis Player: {player.full_name} with {player.win_count} wins."


def get_tennis_player_by_matches_count() -> str:
    player = TennisPlayer.objects.annotate(
        match_count=Count('player_matches')
    ).order_by('-match_count', 'ranking').first()

    if not player or player.match_count == 0:
        return ""

    return f"Tennis Player: {player.full_name} with {player.match_count} matches played."


def get_tournaments_by_surface_type(surface=None) -> str:
    if surface is None:
        return ""

    tournaments = Tournament.objects.filter(
        surface_type__icontains=surface
    ).annotate(
        num_matches=Count('tournament_matches')
    ).order_by('-start_date')

    if not tournaments.exists():
        return ""

    result = [
        f"Tournament: {t.name}, start date: {t.start_date}, matches: {t.num_matches}"
        for t in tournaments
    ]

    return '\n'.join(result)


def get_latest_match_info() -> str:
    latest_match = Match.objects.order_by('-date_played', '-id').first()

    if not latest_match:
        return ""

    players = latest_match.players.all().order_by('full_name')
    players_vs = " vs ".join(player.full_name for player in players)

    winner_name = latest_match.winner.full_name if latest_match.winner else "TBA"

    result = (
        f"Latest match played on: {latest_match.date_played}, "
        f"tournament: {latest_match.tournament.name}, score: {latest_match.score}, "
        f"players: {players_vs}, winner: {winner_name}, summary: {latest_match.summary}"
    )

    return result


def get_matches_by_tournament(tournament_name=None) -> str:
    if tournament_name is None:
        return "No matches found."

    if not Tournament.objects.filter(name__exact=tournament_name).exists():
        return "No matches found."

    matches = Match.objects.select_related('tournament', 'winner') \
        .filter(tournament__name__exact=tournament_name) \
        .order_by('-date_played')

    if not matches.exists():
        return "No matches found."

    result = [
        f"Match played on: {m.date_played}, score: {m.score}, winner: {m.winner.full_name if m.winner else 'TBA'}"
        for m in matches
    ]

    return '\n'.join(result)
