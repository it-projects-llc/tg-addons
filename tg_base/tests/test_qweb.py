from lxml import etree

from odoo.tests.common import TransactionCase

# Tests are based on is_t_cache_disable=True
# tests from from odoo.addons.base.tests.test_qweb


class TestQWebTField(TransactionCase):
    def test_render_xml_dont_use_cache_base(self):
        view1 = self.env["ir.ui.view"].create(
            {
                "name": "dummy",
                "type": "qweb",
                "arch": """
                <t t-name="base.dummy">
                    <div t-cache="cache_id" class="toto">
                        <table>
                            <tr><td><span t-esc="value[0]"/></td></tr>
                            <tr><td><span t-esc="value[1]"/></td></tr>
                            <tr><td><span t-esc="value[2]"/></td></tr>
                        </table>
                    </div>
                </t>
            """,
            }
        )
        IrQweb = self.env["ir.qweb"]

        result = etree.fromstring(
            IrQweb._render(view1.id, {"cache_id": 1, "value": [1, 2, 3]})
        )
        self.assertEqual(
            result,
            etree.fromstring(
                """
            <div class="toto">
                <table>
                    <tr><td><span>1</span></td></tr>
                    <tr><td><span>2</span></td></tr>
                    <tr><td><span>3</span></td></tr>
                </table>
            </div>
        """
            ),
            "First rendering",
        )

        result = etree.fromstring(
            IrQweb._render(view1.id, {"cache_id": 1, "value": [10, 20, 30]})
        )
        self.assertEqual(
            result,
            etree.fromstring(
                """
            <div class="toto">
                <table>
                    <tr><td><span>10</span></td></tr>
                    <tr><td><span>20</span></td></tr>
                    <tr><td><span>30</span></td></tr>
                </table>
            </div>
        """
            ),
            "Next rendering cannot cache (use_qweb_t_cache is False)",
        )

    def test_render_xml_dont_use_cache_different(self):
        view1 = self.env["ir.ui.view"].create(
            {
                "name": "dummy",
                "type": "qweb",
                "arch": """
                <t t-name="base.dummy">
                    <div class="toto">
                        <table t-cache="cache_id">
                            <tr><td><span t-esc="value[0]"/></td></tr>
                            <tr><td><span t-esc="value[1]"/></td></tr>
                            <tr><td><span t-esc="value[2]"/></td></tr>
                        </table>
                        <table t-cache="cache_id2">
                            <tr><td><span t-esc="value2[0]"/></td></tr>
                            <tr><td><span t-esc="value2[1]"/></td></tr>
                            <tr><td><span t-esc="value2[2]"/></td></tr>
                        </table>
                    </div>
                </t>
            """,
            }
        )
        IrQweb = self.env["ir.qweb"]

        # use same cache id, display the same content
        result = etree.fromstring(
            IrQweb._render(
                view1.id,
                {
                    "cache_id": 1,
                    "cache_id2": 1,
                    "value": [1, 2, 3],
                    "value2": [10, 20, 30],
                },
            )
        )
        self.assertEqual(
            result,
            etree.fromstring(
                """
            <div class="toto">
                <table>
                    <tr><td><span>1</span></td></tr>
                    <tr><td><span>2</span></td></tr>
                    <tr><td><span>3</span></td></tr>
                </table>
                <table>
                    <tr><td><span>10</span></td></tr>
                    <tr><td><span>20</span></td></tr>
                    <tr><td><span>30</span></td></tr>
                </table>
            </div>
        """
            ),
            "First rendering",
        )

        result = etree.fromstring(
            IrQweb._render(
                view1.id,
                {
                    "cache_id": (2, 5, 6),
                    "cache_id2": (2, 5, 5),
                    "value": [41, 42, 43],
                    "value2": [51, 52, 53],
                },
            )
        )
        self.assertEqual(
            result,
            etree.fromstring(
                """
            <div class="toto">
                <table>
                    <tr><td><span>41</span></td></tr>
                    <tr><td><span>42</span></td></tr>
                    <tr><td><span>43</span></td></tr>
                </table>
                <table>
                    <tr><td><span>51</span></td></tr>
                    <tr><td><span>52</span></td></tr>
                    <tr><td><span>53</span></td></tr>
                </table>
            </div>
        """
            ),
            "Use different cache id",
        )

    def test_render_xml_dont_use_cache_contains_nocache(self):
        view1 = self.env["ir.ui.view"].create(
            {
                "name": "dummy",
                "type": "qweb",
                "arch": """
                <t t-name="base.dummy">
                    <div t-cache="cache_id" class="toto">
                        <table>
                            <tr><td><span t-esc="value[0]"/></td></tr>
                            <tr t-nocache=""><td><span t-esc="value[1]"/></td></tr>
                            <tr><td><span t-esc="value[2]"/></td></tr>
                        </table>
                    </div>
                </t>
            """,
            }
        )
        IrQweb = self.env["ir.qweb"]

        result = etree.fromstring(
            IrQweb._render(view1.id, {"cache_id": 1, "value": [1, 2, 3]})
        )
        self.assertEqual(
            result,
            etree.fromstring(
                """
            <div class="toto">
                <table>
                    <tr><td><span>1</span></td></tr>
                    <tr><td><span>2</span></td></tr>
                    <tr><td><span>3</span></td></tr>
                </table>
            </div>
        """
            ),
            "First rendering",
        )

        result = etree.fromstring(
            IrQweb._render(view1.id, {"cache_id": 1, "value": [10, 20, 30]})
        )
        self.assertEqual(
            result,
            etree.fromstring(
                """
            <div class="toto">
                <table>
                    <tr><td><span>10</span></td></tr>
                    <tr><td><span>20</span></td></tr>
                    <tr><td><span>30</span></td></tr>
                </table>
            </div>
        """
            ),
            "Next rendering cannot use cache (use_qweb_t_cache is False)",
        )

    def test_render_xml_dont_use_cache_recursive(self):
        view1 = self.env["ir.ui.view"].create(
            {
                "name": "dummy",
                "type": "qweb",
                "arch": """
                <t t-name="base.dummy">
                    <div class="toto">
                        <table t-cache="cache_id">
                            <tr><td><t t-esc="value[0]"/></td></tr>
                            <tr>
                                <td>
                                    <table t-nocache="" t-cache="cache_id2">
                                        <tr><td><t t-esc="value2[0]"/></td></tr>
                                        <tr><td><t t-esc="value2[1]"/></td></tr>
                                        <tr><td><t t-esc="value2[2]"/></td></tr>
                                    </table>
                                </td>
                            </tr>
                            <tr><td><t t-esc="value[2]"/></td></tr>
                        </table>
                    </div>
                </t>
            """,
            }
        )
        IrQweb = self.env["ir.qweb"]

        # use same cache id, display the same content
        result = etree.fromstring(
            IrQweb._render(
                view1.id,
                {
                    "cache_id": (1, 0),
                    "cache_id2": (2, 0),
                    "value": [1, 2, 3],
                    "value2": [10, 20, 30],
                },
            )
        )
        self.assertEqual(
            result,
            etree.fromstring(
                """
            <div class="toto">
                <table>
                    <tr><td>1</td></tr>
                    <tr>
                        <td>
                            <table>
                                <tr><td>10</td></tr>
                                <tr><td>20</td></tr>
                                <tr><td>30</td></tr>
                            </table>
                        </td>
                    </tr>
                    <tr><td>3</td></tr>
                </table>
            </div>
        """
            ),
            "First rendering",
        )

        result = etree.fromstring(
            IrQweb._render(
                view1.id,
                {
                    "cache_id": (1, 0),
                    "cache_id2": (2, 1),
                    "value": [41, 42, 43],
                    "value2": [51, 52, 53],
                },
            )
        )
        self.assertEqual(
            result,
            etree.fromstring(
                """
            <div class="toto">
                <table>
                    <tr><td>41</td></tr>
                    <tr>
                        <td>
                            <table>
                                <tr><td>51</td></tr>
                                <tr><td>52</td></tr>
                                <tr><td>53</td></tr>
                            </table>
                        </td>
                    </tr>
                    <tr><td>43</td></tr>
                </table>
            </div>
        """
            ),
            "Next rendering cannot use cache (use_qweb_t_cache is False)",
        )

        result = etree.fromstring(
            IrQweb._render(
                view1.id,
                {
                    "cache_id": (1, 1),
                    "cache_id2": (2, 0),
                    "value": [31, 32, 33],
                    "value2": [51, 52, 53],
                },
            )
        )
        self.assertEqual(
            result,
            etree.fromstring(
                """
            <div class="toto">
                <table>
                    <tr><td>31</td></tr>
                    <tr>
                        <td>
                            <table>
                                <tr><td>51</td></tr>
                                <tr><td>52</td></tr>
                                <tr><td>53</td></tr>
                            </table>
                        </td>
                    </tr>
                    <tr><td>33</td></tr>
                </table>
            </div>
        """
            ),
            "Third rendering cannot use cache (use_qweb_t_cache is False)",
        )

    def test_render_xml_dont_use_cache_false_recursive(self):
        view1 = self.env["ir.ui.view"].create(
            {
                "name": "dummy",
                "type": "qweb",
                "arch": """
                <t t-name="base.dummy">
                    <div class="toto">
                        <table t-cache="cache_id">
                            <tr><td><t t-esc="value[0]"/></td></tr>
                            <tr t-nocache="">
                                <td>
                                    <table t-cache="cache_id2">
                                        <tr><td><t t-esc="value2[0]"/></td></tr>
                                        <tr><td><t t-esc="value2[1]"/></td></tr>
                                        <tr><td><t t-esc="value2[2]"/></td></tr>
                                    </table>
                                </td>
                            </tr>
                            <tr><td><t t-esc="value[2]"/></td></tr>
                        </table>
                    </div>
                </t>
            """,
            }
        )
        IrQweb = self.env["ir.qweb"]

        # use same cache id, display the same content
        result = etree.fromstring(
            IrQweb._render(
                view1.id,
                {
                    "cache_id": (1, 0),
                    "cache_id2": (2, 0),
                    "value": [1, 2, 3],
                    "value2": [10, 20, 30],
                },
            )
        )
        self.assertEqual(
            result,
            etree.fromstring(
                """
            <div class="toto">
                <table>
                    <tr><td>1</td></tr>
                    <tr>
                        <td>
                            <table>
                                <tr><td>10</td></tr>
                                <tr><td>20</td></tr>
                                <tr><td>30</td></tr>
                            </table>
                        </td>
                    </tr>
                    <tr><td>3</td></tr>
                </table>
            </div>
        """
            ),
            "First rendering",
        )

        result = etree.fromstring(
            self.env["ir.qweb"]._render(
                view1.id,
                {
                    "cache_id": (1, 0),
                    "cache_id2": (2, 1),
                    "value": [41, 42, 43],
                    "value2": [51, 52, 53],
                },
            )
        )
        self.assertEqual(
            result,
            etree.fromstring(
                """
            <div class="toto">
                <table>
                    <tr><td>41</td></tr>
                    <tr>
                        <td>
                            <table>
                                <tr><td>51</td></tr>
                                <tr><td>52</td></tr>
                                <tr><td>53</td></tr>
                            </table>
                        </td>
                    </tr>
                    <tr><td>43</td></tr>
                </table>
            </div>
        """
            ),
            "Next rendering cannot use cache (use_qweb_t_cache is False)",
        )

        result = etree.fromstring(
            self.env["ir.qweb"]._render(
                view1.id,
                {
                    "cache_id": (1, 1),
                    "cache_id2": (2, 0),
                    "value": [31, 32, 33],
                    "value2": [51, 52, 53],
                },
            )
        )
        self.assertEqual(
            result,
            etree.fromstring(
                """
            <div class="toto">
                <table>
                    <tr><td>31</td></tr>
                    <tr>
                        <td>
                            <table>
                                <tr><td>51</td></tr>
                                <tr><td>52</td></tr>
                                <tr><td>53</td></tr>
                            </table>
                        </td>
                    </tr>
                    <tr><td>33</td></tr>
                </table>
            </div>
        """
            ),
            "Third rendering cannot use cache (use_qweb_t_cache is False)",
        )
