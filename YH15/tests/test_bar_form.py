from django.test import TestCase
from YH15.forms import BarForm


class TestBarForm(TestCase):
    def test_bar_form(self) -> None:
        bar_form = BarForm()
        self.assertTrue(isinstance(bar_form, BarForm))