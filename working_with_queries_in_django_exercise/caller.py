import os
from typing import List

import django
from django.db.models import Case, When, Value, QuerySet

from main_app.choices import OperationSystemChoice, LaptopBrandChoice, MealTypeChoice, DungeonDifficultyChoice, \
    WorkoutTypeChoice

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal, Dungeon, Workout


# Create and check models

#   1.Artwork Gallery
def show_highest_rated_art() -> str:
    highest_rated_art = ArtworkGallery.objects.order_by('-rating', 'id').first()

    return f"{highest_rated_art.art_name} is the highest-rated art with a {highest_rated_art.rating} rating!"


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    ArtworkGallery.objects.bulk_create(
        [first_art,
         second_art,
         ])


def delete_negative_rated_arts() -> None:
    ArtworkGallery.objects.filter(rating__lt=0).delete()


#   2.Laptop
def show_the_most_expensive_laptop() -> str:
    me_laptop = Laptop.objects.order_by('-price', '-id').first()

    return f"{me_laptop.brand} is the most expensive laptop available for {me_laptop.price}$!"


def bulk_create_laptops(args: List[Laptop]) -> None:
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage() -> None:
    Laptop.objects.filter(brand__in=['Asus', 'Lenovo']).update(storage=512)


def update_to_16_GB_memory() -> None:
    Laptop.objects.filter(brand__in=["Apple", "Dell", "Acer"]).update(memory=16)


def update_operation_systems() -> None:
    Laptop.objects.update(
        operation_system=Case(
            When(brand=LaptopBrandChoice.ASUS, then=Value(OperationSystemChoice.WINDOWS)),
            When(brand=LaptopBrandChoice.APPLE, then=Value(OperationSystemChoice.MACOS)),
            When(brand__in=[LaptopBrandChoice.DELL, LaptopBrandChoice.ACER], then=Value(OperationSystemChoice.LINUX)),
            When(brand=LaptopBrandChoice.LENOVO, then=Value(OperationSystemChoice.CHROME_OS)),
        )
    )


def delete_inexpensive_laptops() -> None:
    Laptop.objects.filter(price__lt=1200).delete()


#   3.Chess Player
def bulk_create_chess_players(args: List[ChessPlayer]) -> None:
    ChessPlayer.objects.bulk_create(args)


def delete_chess_players() -> None:
    ChessPlayer.objects.filter(title='no title').delete()


def change_chess_games_won() -> None:
    ChessPlayer.objects.filter(title='GM').update(games_won=30)


def change_chess_games_lost() -> None:
    ChessPlayer.objects.filter(title='no title').update(games_lost=25)


def change_chess_games_drawn() -> None:
    ChessPlayer.objects.all().update(games_drawn=10)


def grand_chess_title_gb() -> None:
    ChessPlayer.objects.filter(rating__gt=2400).update(title='GM')


def grand_chess_title_IM() -> None:
    ChessPlayer.objects.filter(rating__in=[2300, 2399]).update(title='IM')


def grand_chess_title_FM() -> None:
    ChessPlayer.objects.filter(rating__in=[2200, 2299]).update(title='FM')


def grand_chess_title_regular_player() -> None:
    ChessPlayer.objects.filter(rating__in=[0, 2199]).update(title='regular player')


#    4. Meal
def set_new_chefs() -> None:
    Meal.objects.update(
        chef=Case(
            When(meal_type=MealTypeChoice.BREAKFAST, then=Value('Gordon Ramsay')),
            When(meal_type=MealTypeChoice.LUNCH, then=Value('Julia Child')),
            When(meal_type=MealTypeChoice.DINNER, then=Value('Jamie Oliver')),
            When(meal_type=MealTypeChoice.SNACK, then=Value('Thomas Keller')),
        )
    )


def set_new_preparation_times() -> None:
    Meal.objects.update(
        preparation_time=Case(
            When(meal_type=MealTypeChoice.BREAKFAST, then=Value('10 minutes')),
            When(meal_type=MealTypeChoice.LUNCH, then=Value('12 minutes')),
            When(meal_type=MealTypeChoice.DINNER, then=Value('15 minutes')),
            When(meal_type=MealTypeChoice.SNACK, then=Value('5 minutes')),
        )
    )


def update_low_calorie_meals() -> None:
    Meal.objects.filter(meal_type__in=[MealTypeChoice.BREAKFAST, MealTypeChoice.DINNER]).update(calories=400)


def update_high_calorie_meals() -> None:
    Meal.objects.filter(meal_type__in=[MealTypeChoice.LUNCH, MealTypeChoice.SNACK]).update(calories=700)


def delete_lunch_and_snack_meals() -> None:
    Meal.objects.filter(meal_type__in=[MealTypeChoice.LUNCH, MealTypeChoice.SNACK]).delete()


#    5.Dungeon
def show_hard_dungeons() -> str:
    hard_dungeons = Dungeon.objects.filter(difficulty=DungeonDifficultyChoice.HARD).order_by('-location')

    return '\n'.join(str(hard_dun) for hard_dun in hard_dungeons)


def bulk_create_dungeons(args: List[Dungeon]) -> None:
    Dungeon.objects.bulk_create(args)


def update_dungeon_names() -> None:
    Dungeon.objects.update(
        name=Case(
            When(difficulty=DungeonDifficultyChoice.EASY, then=Value('The Erased Thombs')),
            When(difficulty=DungeonDifficultyChoice.MEDIUM, then=Value('The Coral Labyrinth')),
            When(difficulty=DungeonDifficultyChoice.HARD, then=Value('The Lost Haunt')),
        )
    )


def update_dungeon_bosses_health() -> None:
    Dungeon.objects.filter(difficulty__in=[DungeonDifficultyChoice.MEDIUM,
                                           DungeonDifficultyChoice.HARD]).update(boss_health=500)


def boss_health() -> None:
    Dungeon.objects.update(
        recommended_level=Case(
            When(difficulty=DungeonDifficultyChoice.EASY, then=Value(25)),
            When(difficulty=DungeonDifficultyChoice.MEDIUM, then=Value(50)),
            When(difficulty=DungeonDifficultyChoice.HARD, then=Value(75)),
        )
    )


def update_dungeon_rewards() -> None:
    Dungeon.objects.update(
        reward=Case(
            When(boss_health=500, then=Value('1000 Gold')),
            When(location__startswith='E', then=Value('New dungeon unlocked')),
            When(location__endswith='s', then=Value('Dragonheart Amulet'))
        )
    )


def set_new_locations() -> None:
    Dungeon.objects.update(
        location=Case(
            When(recommended_level=25, then=Value('Enchanted Maze')),
            When(recommended_level=50, then=Value('Grimstone Mines')),
            When(recommended_level=75, then=Value('Shadowed Abyss')),
        )
    )


#   6.Workout
def show_workouts() -> str:
    filtered_workouts = Workout.objects.filter(
        workout_type__in=[
        WorkoutTypeChoice.CALISTHENICS, WorkoutTypeChoice.CROSSFIT
    ]).order_by('id')

    return '\n'.join(str(workout) for workout in filtered_workouts)


def get_high_difficulty_cardio_workouts() -> QuerySet:
    return Workout.objects.filter(
        workout_type=WorkoutTypeChoice.CARDIO,
        difficulty='High'
    ).order_by('instructor')


def set_new_instructors() -> None:
    Workout.objects.update(
        instructor=Case(
            When(workout_type=WorkoutTypeChoice.CARDIO, then=Value('John Smith')),
            When(workout_type=WorkoutTypeChoice.STRENGTH, then=Value('Michael Williams')),
            When(workout_type=WorkoutTypeChoice.YOGA, then=Value('Emily Johnson')),
            When(workout_type=WorkoutTypeChoice.CROSSFIT, then=Value('Sarah Davis')),
            When(workout_type=WorkoutTypeChoice.CALISTHENICS, then=Value('Chris Heria')),
        )
    )


def set_new_duration_times() -> None:
    Workout.objects.update(
        duration=Case(
            When(instructor='John Smith', then=Value('15 minutes')),
            When(instructor='Sarah Davis', then=Value('30 minutes')),
            When(instructor='Chris Heria', then=Value('45 minutes')),
            When(instructor='Michael Williams', then=Value('1 hour')),
            When(instructor='Emily Johnson', then=Value('1 hour and 30 minutes')),
        )
    )


def delete_workouts() -> None:
    Workout.objects.exclude(workout_type__in=[WorkoutTypeChoice.STRENGTH, WorkoutTypeChoice.CALISTHENICS]).delete()


# Run and print your queries

# 1.Artwork Gallery
# artwork1 = ArtworkGallery(artist_name='Vincent van Gogh', art_name='Starry Night', rating=4, price=1200000.0)
# artwork2 = ArtworkGallery(artist_name='Leonardo da Vinci', art_name='Mona Lisa', rating=5, price=1500000.0)
#
# bulk_create_arts(artwork1, artwork2)
# print(show_highest_rated_art())
# print(ArtworkGallery.objects.all())
####################################################################################################################
# 2.Laptop
# laptop1 = Laptop(
#     brand='Asus',
#     processor='Intel Core i5',
#     memory=8,
#     storage=256,
#     operation_system='MacOS',
#     price=899.99
# )
# laptop2 = Laptop(
#     brand='Apple',
#     processor='Chrome OS',
#     memory=16,
#     storage=256,
#     operation_system='MacOS',
#     price=1399.99
# )
# laptop3 = Laptop(
#     brand='Lenovo',
#     processor='AMD Ryzen 7',
#     memory=12,
#     storage=256,
#     operation_system='Linux',
#     price=999.99,
# )
#
# # Create a list of instances
# laptops_to_create = [laptop1, laptop2, laptop3]
#
# # Use bulk_create to save the instances
# bulk_create_laptops(laptops_to_create)
#
# update_to_512_gb_storage()
# update_operation_systems()
#
# # Retrieve 2 laptops from the database
# asus_laptop = Laptop.objects.filter(brand__exact='Asus').get()
# lenovo_laptop = Laptop.objects.filter(brand__exact='Lenovo').get()
#
# print(asus_laptop.storage)
# print(lenovo_laptop.operation_system)
####################################################################################################################
# 3.Chess Player
# player1 = ChessPlayer(
#     username='Player1',
#     title='no title',
#     rating=2200,
#     games_played=50,
#     games_won=20,
#     games_lost=25,
#     games_drawn=5,
# )
# player2 = ChessPlayer(
#     username='Player2',
#     title='IM',
#     rating=2350,
#     games_played=80,
#     games_won=40,
#     games_lost=25,
#     games_drawn=15,
# )
#
# # Call the bulk_create_chess_players function
# bulk_create_chess_players([player1, player2])
#
# # Call the delete_chess_players function
# delete_chess_players()
#
# # Check that the players are deleted
# print("Number of Chess Players after deletion:", ChessPlayer.objects.count())
####################################################################################################################
# 4.Meal
# meal1 = Meal.objects.create(
#     name="Pancakes",
#     meal_type="Breakfast",
#     preparation_time="20 minutes",
#     difficulty=3,
#     calories=350,
#     chef="Jane",
# )
#
# meal2 = Meal.objects.create(
#     name="Spaghetti Bolognese",
#     meal_type="Dinner",
#     preparation_time="45 minutes",
#     difficulty=4,
#     calories=550,
#     chef="Sarah",
# )
# # Test the set_new_chefs function
# set_new_chefs()
#
# # Test the set_new_preparation_times function
# set_new_preparation_times()
#
# # Refreshes the instances
# meal1.refresh_from_db()
# meal2.refresh_from_db()
#
# # Print the updated meal information
# print("Meal 1 Chef:", meal1.chef)
# print("Meal 1 Preparation Time:", meal1.preparation_time)
# print("Meal 2 Chef:", meal2.chef)
# print("Meal 2 Preparation Time:", meal2.preparation_time)
####################################################################################################################
#   5.Dungeon
# # Create two instances
# dungeon1 = Dungeon(
#     name="Dungeon 1",
#     boss_name="Boss 1",
#     boss_health=1000,
#     recommended_level=75,
#     reward="Gold",
#     location="Eternal Hell",
#     difficulty="Hard",
# )
#
# dungeon2 = Dungeon(
#     name="Dungeon 2",
#     boss_name="Boss 2",
#     boss_health=400,
#     recommended_level=25,
#     reward="Experience",
#     location="Crystal Caverns",
#     difficulty="Easy",
# )
#
# # Bulk save the instances
# bulk_create_dungeons([dungeon1, dungeon2])
#
# # Update boss's health
# update_dungeon_bosses_health()
#
# # Show hard dungeons
# hard_dungeons_info = show_hard_dungeons()
# print(hard_dungeons_info)
#
# # Change dungeon names based on difficulty
# update_dungeon_names()
# dungeons = Dungeon.objects.order_by('boss_health')
# print(dungeons[0].name)
# print(dungeons[1].name)
#
# # Change the dungeon rewards
# update_dungeon_rewards()
# dungeons = Dungeon.objects.order_by('boss_health')
# print(dungeons[0].reward)
# print(dungeons[1].reward)
####################################################################################################################
#   6.Workout
# # Create two Workout instances
# workout1 = Workout.objects.create(
#     name="Push-Ups",
#     workout_type="Calisthenics",
#     duration="10 minutes",
#     difficulty="Intermediate",
#     calories_burned=200,
#     instructor="Bob"
# )
#
# workout2 = Workout.objects.create(
#     name="Running",
#     workout_type="Cardio",
#     duration="30 minutes",
#     difficulty="High",
#     calories_burned=400,
#     instructor="Lilly"
# )
#
# # Run the functions
# print(show_workouts())
#
# high_difficulty_cardio_workouts = get_high_difficulty_cardio_workouts()
# for workout in high_difficulty_cardio_workouts:
#     print(f"{workout.name} by {workout.instructor}")
#
# set_new_instructors()
# for workout in Workout.objects.all():
#     print(f"Instructor: {workout.instructor}")
#
# set_new_duration_times()
# for workout in Workout.objects.all():
#     print(f"Duration: {workout.duration}")
