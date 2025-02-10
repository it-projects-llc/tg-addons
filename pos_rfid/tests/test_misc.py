from odoo.tests.common import HttpCase


class TestMisc(HttpCase):
    def test_session_info_no_keyerror(self):
        config = self.env["pos.config"].create(
            {
                "name": "Shop",
            }
        )

        self.authenticate("admin", "admin")

        # no sessions for this config
        # just make sure it does not return 500 error with KeyError
        resp = self.url_open(
            f"/pos/ui?config_id={config.id}", allow_redirects=False, timeout=10000
        )
        self.assertEqual(resp.status_code, 303)
