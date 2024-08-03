import os
import django
from django.db.models import Q, Count, Sum, Avg, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut, Mission, Spacecraft


# Create queries within functions
def get_astronauts(search_string=None) -> str:
    if search_string is None:
        return ""

    astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)
    ).order_by('name')

    if not astronauts.exists():
        return ""

    result = [
        f"Astronaut: {a.name}, phone number: {a.phone_number}, status: {'Active' if a.is_active else 'Inactive'}"
        for a in astronauts
    ]

    return '\n'.join(result)


def get_top_astronaut() -> str:
    astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()

    if not astronaut or astronaut.mission_count == 0:
        return "No data."

    return f"Top Astronaut: {astronaut.name} with {astronaut.mission_count} missions."


def get_top_commander() -> str:
    commanders = Astronaut.objects.annotate(
        commanded_mission_count=Count('commanders')
    ).order_by('-commanded_mission_count', 'phone_number').first()

    if not commanders or commanders.commanded_mission_count == 0:
        return "No data."

    return f"Top Commander: {commanders.name} with {commanders.commanded_mission_count} commanded missions."


def get_last_completed_mission() -> str:
    mission = (Mission.objects.filter(status=Mission.SatusChoices.COMPLETED)
               .select_related('commander', 'spacecraft')
               .prefetch_related('astronauts')
               .order_by('-launch_date')
               .first())

    if not mission:
        return "No data."

    commander_name = mission.commander.name if mission.commander else "TBA"
    astronaut_names = ", ".join(a.name for a in mission.astronauts.order_by('name'))
    total_spacewalks = mission.astronauts.aggregate(Sum('spacewalks'))['spacewalks__sum'] or 0

    return (f"The last completed mission is: {mission.name}. "
            f"Commander: {commander_name}. "
            f"Astronauts: {astronaut_names}. "
            f"Spacecraft: {mission.spacecraft.name}. "
            f"Total spacewalks: {total_spacewalks}.")


def get_most_used_spacecraft():
    most_used_spacecraft = (Spacecraft.objects.annotate(num_missions=Count('missions'))
                            .order_by('-num_missions', 'name').first())

    if not most_used_spacecraft or most_used_spacecraft.num_missions == 0:
        return "No data."

    num_astronauts = Mission.objects.filter(spacecraft=most_used_spacecraft).values('astronauts').distinct().count()

    return (f"The most used spacecraft is: {most_used_spacecraft.name}, "
            f"manufactured by {most_used_spacecraft.manufacturer}, "
            f"used in {most_used_spacecraft.num_missions} missions, "
            f"astronauts on missions: {num_astronauts}.")


def decrease_spacecrafts_weight() -> str:
    affected_spacecrafts = Spacecraft.objects.filter(
        missions__status=Mission.SatusChoices.PLANED,
        weight__gte=200.0
    ).distinct()

    if not affected_spacecrafts.exists():
        return "No changes in weight."

    num_affected = affected_spacecrafts.update(weight=F('weight') - 200.0)
    avg_weight = Spacecraft.objects.aggregate(Avg('weight'))['weight__avg'] or 0.0

    return (f"The weight of {num_affected} spacecrafts has been decreased. "
            f"The new average weight of all spacecrafts is {avg_weight:.1f}kg")
