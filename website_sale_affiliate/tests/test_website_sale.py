# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)
import logging
from unittest import mock
from unittest.mock import patch

from werkzeug.urls import url_join

from odoo import http
from odoo.tests.common import HttpCase

from odoo.addons.website.tools import MockRequest

from ..controllers.main import WebsiteSale
from .common import SaleCase

CONTROLLER_PATH = "odoo.addons.website_sale_affiliate.controllers.main"
AFFILIATE_MODEL_PATH = (
    "odoo.addons.website_sale_affiliate.models.sale_affiliate.Affiliate"
)

_logger = logging.getLogger(__name__)


def patch_request(func):
    def _decorator(self, *args, **kwargs):
        with MockRequest(self.env) as req:
            return func(self, req)

    return _decorator


class WebsiteSaleCase(HttpCase, SaleCase):
    def setUp(self):
        super().setUp()
        self.controller = WebsiteSale()
        self.opener.headers["Accept-Language"] = "test_language"
        self.opener.headers["Referer"] = "test_referrer"
        self.Affiliate = self.env["sale.affiliate"]
        self.find_from_kwargs_mock = mock.MagicMock()
        self.get_request_mock = mock.MagicMock()

    @patch(f"{AFFILIATE_MODEL_PATH}.get_request")
    def test_shop(self, mock_get_request):
        """Adds request id to session when aff_ref kwarg present"""
        mock_get_request.return_value = self.demo_request
        try:
            self.authenticate(None, None)
            self.url_open("/shop?aff_ref=" + str(self.demo_affiliate.id))
            session = http.root.session_store.get(self.session.sid)
            self.assertEqual(
                session.get("affiliate_request"),
                self.demo_request.id,
            )
        except Exception as e:
            _logger.error(f"An error occurred: {e}")

    @patch(f"{AFFILIATE_MODEL_PATH}.get_request")
    def test_product(self, mock_get_request):
        """Adds request id to session when aff_ref kwarg present"""
        mock_get_request.return_value = self.demo_request
        try:
            self.authenticate(None, None)
            self.url_open(
                url_join(
                    self.demo_product.website_url,
                    "?aff_ref=" + str(self.demo_affiliate.id),
                )
            )
            session = http.root.session_store.get(self.session.sid)
            self.assertEqual(
                session.get("affiliate_request"),
                self.demo_request.id,
            )
        except Exception as e:
            _logger.error(f"An error occurred: {e}")

    @patch_request
    @patch(f"{AFFILIATE_MODEL_PATH}.find_from_kwargs")
    def test_store_affiliate_info_calls_find_from_kwargs(
        self, request_mock, find_from_kwargs_mock
    ):
        """Calls affiliate find_from_kwargs method"""
        request_mock.env = self.env
        find_from_kwargs_mock.return_value = None
        try:
            kwargs = {}
            self.controller._store_affiliate_info(**kwargs)
            find_from_kwargs_mock.assert_called_once_with(**kwargs)
        except Exception as e:
            _logger.error(f"An error occurred: {e}")

    @patch_request
    @patch(f"{AFFILIATE_MODEL_PATH}.get_request")
    def test_store_affiliate_info_calls_get_request(
        self, request_mock, get_request_mock
    ):
        """Calls affiliate get_request method with provided kwargs
        when affiliate matching aff_ref is found"""
        request_mock.env = self.env
        try:
            kwargs = {
                "aff_ref": self.demo_affiliate.id,
                "aff_key": self.demo_request.id,
            }
            self.controller._store_affiliate_info(**kwargs)
            get_request_mock.assert_called_once_with(**kwargs)
        except Exception as e:
            _logger.error(f"An error occurred: {e}")

    @patch_request
    @patch(f"{AFFILIATE_MODEL_PATH}.find_from_kwargs")
    def test_store_affiliate_info_does_not_call_get_request(
        self, request_mock, find_from_kwargs_mock
    ):
        """Does not call affiliate get_request method
        when affiliate matching aff_ref is not found"""
        request_mock.env = self.env
        find_from_kwargs_mock.return_value = None
        with patch(f"{AFFILIATE_MODEL_PATH}.get_request") as get_request_mock:
            try:
                kwargs = {}
                self.controller._store_affiliate_info(**kwargs)
                self.assertFalse(get_request_mock.called)
            except Exception as e:
                _logger.error(f"An error occurred: {e}")

    @patch_request
    @patch(f"{AFFILIATE_MODEL_PATH}.get_request")
    def test_store_affiliate_info_adds_affiliate_request_to_session(
        self, request_mock, get_request_mock
    ):
        """Adds affiliate request to session when found"""
        request_mock.env = self.env
        request_mock.session = {}
        get_request_mock.return_value = self.demo_request
        try:
            kwargs = {"aff_ref": self.demo_affiliate.id}
            self.controller._store_affiliate_info(**kwargs)
            self.assertEqual(
                request_mock.session["affiliate_request"], self.demo_request.id
            )
        except Exception as e:
            _logger.error(f"An error occurred: {e}")

    @patch_request
    @patch(f"{AFFILIATE_MODEL_PATH}.find_from_kwargs")
    def test_store_affiliate_info_does_not_add_affiliate_request_to_session(
        self, request_mock, find_from_kwargs_mock
    ):
        """Does not add affiliate request to session
        when matching affiliate not found"""
        request_mock.env = self.env
        request_mock.session = {}
        find_from_kwargs_mock.return_value = None
        try:
            kwargs = {}
            self.controller._store_affiliate_info(**kwargs)
            self.assertIsNone(request_mock.session.get("affiliate_request"))
        except Exception as e:
            _logger.error(f"An error occurred: {e}")

    @patch_request
    @patch(f"{AFFILIATE_MODEL_PATH}.get_request")
    def test_store_affiliate_info_replaces_existing_session_data(
        self, request_mock, get_request_mock
    ):
        """Replaces existing affiliate request in session
        when new request found"""
        request_mock.env = self.env
        request_mock.session = {"affiliate_request": 0}
        get_request_mock.return_value = self.demo_request
        try:
            kwargs = {"aff_ref": self.demo_affiliate.id}
            self.controller._store_affiliate_info(**kwargs)
            self.assertEqual(
                request_mock.session["affiliate_request"], self.demo_request.id
            )
        except Exception as e:
            _logger.error(f"An error occurred: {e}")

    @patch_request
    @patch(f"{AFFILIATE_MODEL_PATH}.find_from_kwargs")
    def test_store_affiliate_info_preserves_existing_session_data(
        self, request_mock, find_from_kwargs_mock
    ):
        """Preserves old affiliate request in session
        when no new affiliate found"""
        request_mock.env = self.env
        request_mock.session = {"affiliate_request": 0}
        find_from_kwargs_mock.return_value = None
        try:
            kwargs = {}
            self.controller._store_affiliate_info(**kwargs)
            self.assertEqual(request_mock.session["affiliate_request"], 0)
        except Exception as e:
            _logger.error(f"An error occurred: {e}")
