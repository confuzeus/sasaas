import unittest.mock
from unittest.mock import MagicMock
from django.test import TestCase

from my_awesome_project.core.utils import captcha as captcha_util


class UtilsTests(TestCase):
    def test_captcha(self):

        h_captcha = captcha_util.Captcha(captcha_util.Captcha.H_CAPTCHA)
        self.assertEqual(h_captcha.provider_url, captcha_util.Captcha.H_CAPTCHA_URL)

        with self.assertRaises(NotImplementedError):
            captcha_util.Captcha(captcha_util.Captcha.RECAPTCHA)

        with unittest.mock.patch.object(captcha_util, "requests") as mock:
            response = MagicMock()
            mock.post.return_value = response

            response.status_code = 200
            response.json.return_value = {"success": True}

            self.assertTrue(h_captcha.captcha_success("abcd"))

            mock.post.side_effect = Exception()
            self.assertFalse(h_captcha.captcha_success("abcd"))

            mock.post.side_effect = None

            response.json.side_effect = Exception()
            self.assertFalse(h_captcha.captcha_success("abcd"))

            response.json.side_effect = None

            response.status_code = 400
            self.assertFalse(h_captcha.captcha_success("abcd"))
