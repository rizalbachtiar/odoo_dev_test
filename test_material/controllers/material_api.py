# -*- coding: utf-8 -*-
from odoo import http, api, SUPERUSER_ID
from odoo.http import request
import json


class APIMaterial(http.Controller):
    def _get_material_data(self, materials):
        result = []
        for m in materials:
            result.append(
                {
                    "id": m.id,
                    "material_code": m.material_code,
                    "name": m.name,
                    "material_type": m.material_type,
                    "buy_price": m.buy_price,
                    "supplier": {
                        "id": m.supplier_id.id,
                        "name": m.supplier_id.name
                    },
                }
            )
        return result

    @http.route("/api/materials", type="http", auth="public", methods=["GET"])
    def get_materials(self, material_type=None):
        try:
            domain = []
            if material_type:
                domain.append(("material_type", "=", material_type))
            materials = request.env["test.material"].sudo().search(domain)
            result = self._get_material_data(materials)
            return http.Response(
                json.dumps({
                    "status": "success",
                    "message": f"{len(result)}, Data Found",
                    "result": result
                }),
                content_type="application/json"
            )
        except Exception as e:
            return http.Response(
                json.dumps({
                    "status": "error",
                    "message": str(e),
                    "result": []
                }),
                content_type="application/json"
            )

    @http.route("/api/materials", type="http", auth="public", methods=["POST"], csrf=False)
    def create_material(self, **data):
        try:
            material = request.env["test.material"].sudo().create({
                "material_code": data.get("material_code"),
                "name": data.get("name"),
                "material_type": data.get("material_type"),
                "buy_price": float(data.get("buy_price")),
                "supplier_id": int(data.get("supplier_id")),
            })
            result = self._get_material_data(material)
            return http.Response(
                json.dumps({
                    "status": "success",
                    "message": "Insert data Material succeeded",
                    "result": result
                }),
                content_type="application/json"
            )
        except Exception as e:
            request.env.cr.rollback()
            return http.Response(
                json.dumps({
                    "status": "error",
                    "message": str(e),
                    "result": []
                }),
                content_type="application/json"
            )
        finally:
            request.env.cr.commit()

    @http.route("/api/materials/<int:material_id>", type="http", auth="public", methods=["PUT"], csrf=False)
    def update_material(self, material_id, **data):
        try:
            vals = {
                "material_code": data.get("material_code"),
                "name": data.get("name"),
                "material_type": data.get("material_type"),
                "buy_price": float(data.get("buy_price")),
                "supplier_id": int(data.get("supplier_id")),
            }
            material = request.env["test.material"].sudo().search([("id", "=", material_id)])
            if not material:
                return http.Response(
                    json.dumps({
                        "status": "error",
                        "message": "Material not found",
                        "result": []
                    }),
                    content_type="application/json"
                )
            material.sudo().write(vals)
            result = self._get_material_data(material)
            return http.Response(
                json.dumps({
                    "status": "success",
                    "message": "Update data Material succeeded",
                    "result": result
                }),
                content_type="application/json"
            )
        except Exception as e:
            request.env.cr.rollback()
            return http.Response(
                json.dumps({
                    "status": "error",
                    "message": str(e),
                    "result": []
                }),
                content_type="application/json"
            )
        finally:
            request.env.cr.commit()

    @http.route("/api/materials/<int:material_id>", type="http", auth="public", methods=["DELETE"], csrf=False)
    def delete_material(self, material_id):
        try:
            material = request.env["test.material"].sudo().search([("id", "=", material_id)])
            if not material:
                return http.Response(
                    json.dumps({
                        "status": "error",
                        "message": "Material not found",
                        "result": []
                    }),
                    content_type="application/json"
                )
            material.unlink()
            return http.Response(
                json.dumps({
                    "status": "success",
                    "message": "Delete data Material succeeded",
                    "result": []
                }),
                content_type="application/json"
            )
        except Exception as e:
            return http.Response(
                json.dumps({
                    "status": "error",
                    "message": str(e),
                    "result": []
                }),
                content_type="application/json"
            )
