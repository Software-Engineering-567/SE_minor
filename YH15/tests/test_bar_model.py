from YH15.models import Bar
from django.test import TestCase
from django.core.exceptions import ValidationError


class TestBarModel(TestCase):
    def test_bar_default_setting(self) -> None:
        bar = Bar.objects.create(
            bar_name="test_bar_name",
        )

        self.assertTrue(
            isinstance(bar, Bar)
        )

        self.assertEqual(
            bar.bar_name, "test_bar_name"
        )

        self.assertEqual(
            bar.bar_rating, 0,
        )

        self.assertEqual(
            bar.bar_occupancy, 0,
        )

        self.assertEqual(
            bar.bar_capacity, 0
        )

    def test_bar_normal_setting(self) -> None:
        bar = Bar.objects.create(
            bar_name="test_bar_name",
            bar_rating=4,
            bar_occupancy=100,
            bar_capacity=120,
        )

        self.assertEqual(
            bar.bar_name, "test_bar_name"
        )

        self.assertEqual(
            bar.bar_rating, 4,
        )

        self.assertEqual(
            bar.bar_occupancy, 100,
        )

        self.assertEqual(
            bar.bar_capacity, 120
        )

    def test_bar_invalid_setting(self) -> None:
        with self.assertRaisesMessage(ValidationError, "Invalid bar rating value -100"):
            Bar.objects.create(
                bar_name="test_bar_name",
                bar_rating=-100,
                bar_occupancy=100,
                bar_capacity=120,
            )

        with self.assertRaisesMessage(ValidationError, "Invalid bar rating value 6"):
            Bar.objects.create(
                bar_name="test_bar_name",
                bar_rating=6,
                bar_capacity=120,
                bar_occupancy=100,
            )

        with self.assertRaisesMessage(ValidationError, "Invalid bar capacity value -1"):
            Bar.objects.create(
                bar_name="test_bar_name",
                bar_rating=3,
                bar_capacity=-1,
                bar_occupancy=1,
            )

        with self.assertRaisesMessage(ValidationError, "Invalid bar capacity value 1001"):
            Bar.objects.create(
                bar_name="test_bar_name",
                bar_rating=3,
                bar_capacity=Bar.MAX_BAR_CAPACITY+1,
                bar_occupancy=1,
            )

        with self.assertRaisesMessage(ValidationError, "Invalid bar occupancy value -1"):
            Bar.objects.create(
                bar_name="test_bar_name",
                bar_rating=3,
                bar_capacity=1000,
                bar_occupancy=-1,
            )

        with self.assertRaisesMessage(ValidationError, "Invalid bar occupancy value 101"):
            Bar.objects.create(
                bar_name="test_bar_name",
                bar_rating=4,
                bar_capacity=100,
                bar_occupancy=101,
            )

    def test_check_enough_occupancy(self) -> None:
        bar = Bar.objects.create(
            bar_name="test_bar_name",
            bar_rating=4,
            bar_occupancy=100,
            bar_capacity=120,
        )

        self.assertTrue(bar.check_enough_occupancy(20))

        self.assertFalse(bar.check_enough_occupancy(21))

    def test_add_customers(self) -> None:
        bar = Bar.objects.create(
            bar_name="test_bar_name",
            bar_rating=4,
            bar_occupancy=100,
            bar_capacity=120,
        )

        with self.assertRaisesMessage(ValueError, "Cannot add 21 more customers to the bar!"):
            bar.add_customers(21)

        bar.add_customers(20)
        self.assertEqual(bar.bar_occupancy, 120)

    def test_customers_leave(self) -> None:
        bar = Bar.objects.create(
            bar_name="test_bar_name",
            bar_rating=4,
            bar_occupancy=100,
            bar_capacity=120,
        )

        with self.assertRaisesMessage(ValueError, "Less 101 customers in the bar!"):
            bar.customers_leave(101)

        bar.customers_leave(100)
        self.assertEqual(bar.bar_occupancy, 0)

    def test___eq__(self) -> None:
        bar1 = Bar.objects.create(
            bar_name="test_bar_name",
            bar_rating=4,
            bar_occupancy=100,
            bar_capacity=120,
        )
        bar2 = Bar.objects.create(
            bar_name="test_bar_name",
            bar_rating=4,
            bar_occupancy=100,
            bar_capacity=120,
        )
        self.assertTrue(bar1.__eq__(bar2))

        self.assertFalse(bar1.__eq__(list()))

