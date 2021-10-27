from django.test import TestCase
from unittest.mock import Mock, patch
from manage import main


class TestManage(TestCase):
    def test_main(self) -> None:
        with self.assertRaises(RuntimeError), patch("manage.main", Mock(side_effect=ImportError)):
            main()