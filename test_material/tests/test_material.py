import odoo
from odoo.tests import HttpCase, tagged
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json

HOST = '127.0.0.1'


@tagged("-at_install", "post_install", "test_material")
class TestMaterial(HttpCase):
    def setUp(self):
        super().setUp()
        self.supplier = self.env["res.partner"].create({
            "name": "Partner Test",
        })
        self.material = self.env["test.material"].create({
            "material_code": "Test Code 01",
            "name": "Test Name",
            "material_type": "jeans",
            "buy_price": 200,
            "supplier_id": self.supplier.id,
        })
        self.base_url = f"http://{HOST}:{odoo.tools.config['http_port']}"

    def test_get_materials(self):
        response = self.url_open("/api/materials")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertIn("success", data["status"])

    def test_create_material_invalid_price(self):
        data = {
            "material_code": "M001234",
            "name": "Test Material",
            "material_type": "cotton",
            "buy_price": str(1),
            "supplier_id": str(self.supplier.id),
        }
        response = self.url_open(
            "/api/materials",
            data=data,
        )
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.text)
        self.assertEqual(res["message"], "Buy price must be at least 100.")

    def test_update_material(self):
        data = {
            "material_code": "Test Code 01",
            "name": "Test Name Update",
            "material_type": "jeans",
            "buy_price": str(200),
            "supplier_id": str(self.supplier.id),
        }
        req = Request(
            f"{self.base_url}/api/materials/{self.material.id}",
            data=urlencode(data).encode('utf-8'),
            method='PUT'
        )
        with urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            self.assertEqual(response.code, 200)
            self.assertEqual(result["message"], "Update data Material succeeded")
            self.assertEqual(result["result"][0]["name"], "Test Name Update")

    def test_delete_material(self):
        req = Request(
            f"{self.base_url}/api/materials/{self.material.id}",
            method='DELETE'
        )
        with urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            self.assertEqual(response.code, 200)
            self.assertEqual(result["message"], "Delete data Material succeeded")
