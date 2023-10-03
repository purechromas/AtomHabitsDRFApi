from rest_framework import status
from rest_framework.reverse import reverse

from habits.models import Habit
from habits.tests.base import BaseApiTestCase


class TestHabitViewSet(BaseApiTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.list_and_create_url = reverse("habits:habit-list")

    def test_habit_post_correct_data(self):
        response = self.client.post(path=self.list_and_create_url, data={
            "action": "Testing my project",
            "time": "13:00",
            "place": "At home",
            "is_pleasant": True,
            "frequency": Habit.Frequency.DAILY,
            "time_complete": 60,
            "is_public": False
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(response.json()["is_public"], False)

    def test_habit_post_incorrect_data_validator_PleasantHabitNoRelatedHabitOrReward(self):
        response = self.client.post(path=self.list_and_create_url, data={
            "action": "Testing my project",
            "time": "13:00",
            "place": "At home",
            "is_pleasant": True,  # PleasantHabitNoRelatedHabitOrReward
            "frequency": Habit.Frequency.DAILY,
            "time_complete": 60,
            "is_public": False,
            "reward": "Eat Icecream"  # PleasantHabitNoRelatedHabitOrReward
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(
            response.json()['non_field_errors'],
            ["You can't add reward or related habit on pleasant habit"]
        )

    def test_habit_post_incorrect_data_validator_RelatedHabitOnlyPleasantHabit(self):
        habit = Habit.objects.create(
            action="Testing my project",
            time="13:00:00",
            place="At home",
            is_pleasant=False,  # RelatedHabitOnlyPleasantHabit
            time_complete=60,
            reward="Sweet cake",
            creator=self.user  # base.py user
        )

        response = self.client.post(path=self.list_and_create_url, data={
            "action": "Testing my project",
            "time": "13:00",
            "place": "At home",
            "is_pleasant": False,
            "frequency": Habit.Frequency.DAILY,
            "time_complete": 60,
            "is_public": False,
            "related_habit": habit.id  # RelatedHabitOnlyPleasantHabit
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(
            response.json()['non_field_errors'],
            ['The selected habit is not pleasant']
        )

    def test_habit_post_incorrect_data_validator_TimeMaximum(self):
        response = self.client.post(path=self.list_and_create_url, data={
            "action": "Testing my project",
            "time": "13:00",
            "place": "At home",
            "is_pleasant": True,
            "frequency": Habit.Frequency.DAILY,
            "time_complete": 121,  # TimeMaximum
            "is_public": False,
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(
            response.json()['non_field_errors'],
            ['Time for complete must be less then 120 seconds']
        )

    def test_habit_post_incorrect_data_validator_RewardOrPleasantHabit(self):
        habit = Habit.objects.create(
            action="Testing my project",
            time="13:00:00",
            place="At home",
            is_pleasant=True,
            time_complete=60,
            creator=self.user  # base.py user
        )

        response = self.client.post(path=self.list_and_create_url, data={
            "action": "Testing my project",
            "time": "13:00",
            "place": "At home",
            "is_pleasant": False,
            "frequency": Habit.Frequency.DAILY,
            "time_complete": 60,
            "is_public": False,
            "related_habit": habit.id,  # RewardOrPleasantHabit
            "reward": "Chocolate"  # RewardOrPleasantHabit
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(
            response.json()['non_field_errors'],
            ["Provide either 'related_habit' or 'reward' not both"]
        )

        response1 = self.client.post(path=self.list_and_create_url, data={
            "action": "Testing my project",
            "time": "13:00",
            "place": "At home",
            "is_pleasant": False,
            "frequency": Habit.Frequency.DAILY,
            "time_complete": 60,
            "is_public": False
        })

        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response1.json(), dict)
        self.assertEqual(
            response1.json()['non_field_errors'],
            ["Provide either 'related_habit' or 'reward'"]
        )

    def test_habit_get_list(self):
        Habit.objects.create(
            action="Testing my project",
            time="13:00:00",
            place="At home",
            is_pleasant=False,
            time_complete=60,
            creator=self.user  # base.py user
        )
        Habit.objects.create(
            action="Testing my project",
            time="13:00:00",
            place="At home",
            is_pleasant=True,
            time_complete=60,
            creator=self.user  # base.py user
        )

        response = self.client.get(self.list_and_create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(response.json()['count'], 2)
        self.assertEqual(len(response.json()['results']), 2)

    def test_habit_get_retrieve(self):
        habit = Habit.objects.create(
            action="Testing my project",
            time="13:00:00",
            place="At home",
            is_pleasant=False,
            time_complete=60,
            creator=self.user  # base.py user
        )

        url = reverse("habits:habit-detail", args=[habit.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(response.json()['action'], 'Testing my project')

    def test_habit_patch(self):
        habit = Habit.objects.create(
            action="Testing my project",
            time="13:00:00",
            place="At home",
            is_pleasant=False,
            time_complete=60,
            creator=self.user  # base.py user
        )

        url = reverse("habits:habit-detail", args=[habit.id])
        response = self.client.patch(url, {
            "action": "Lal"
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_habit_put(self):
        habit = Habit.objects.create(
            action="Testing my project",
            time="13:00:00",
            place="At home",
            is_pleasant=False,
            time_complete=60,
            creator=self.user  # base.py user
        )

        url = reverse("habits:habit-detail", args=[habit.id])
        response = self.client.put(url, {
            "action": "Lal",
            "time": "13:00",
            "place": "outside",
            "is_pleasant": True,
            "time_complete": 30
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_delete(self):
        habit = Habit.objects.create(
            action="Testing my project",
            time="13:00:00",
            place="At home",
            is_pleasant=False,
            time_complete=60,
            creator=self.user  # base.py user
        )

        successful_url = reverse("habits:habit-detail", args=[habit.id])
        response = self.client.delete(successful_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        unsuccessful_url = reverse("habits:habit-detail", args=[2])
        response = self.client.delete(unsuccessful_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestHabitPublicAPIView(BaseApiTestCase):
    def test_habit_get_list_public(self):
        Habit.objects.create(
            action="Testing my project",
            time="13:00:00",
            place="At home",
            is_pleasant=False,
            time_complete=60,
            creator=self.user,  # base.py user
            is_public=True
        )
        Habit.objects.create(
            action="Testing my project",
            time="13:00:00",
            place="At home",
            is_pleasant=True,
            time_complete=60,
            creator=self.user,  # base.py user
            is_public=False
        )

        url = reverse("habits:habit_public")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(len(response.json()['results']), 1)
