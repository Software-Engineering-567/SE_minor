from typing import List

from django.test import TestCase

from YH15.models import Bar


class TestSQLite(TestCase):
    def test_create_and_delete_models(self) -> None:
        total_bar_models: int = 100
        bar_models: List[Bar] = []

        for index in range(total_bar_models):
            bar = Bar.objects.create(
                bar_name=f"test_bar_name_{index}",
            )
            bar_models.append(bar)

        self.assertEqual(
            len(Bar.objects.all()),
            total_bar_models,
        )

        for bar in bar_models:
            bar.delete()

        self.assertEqual(
            len(Bar.objects.all()),
            0
        )