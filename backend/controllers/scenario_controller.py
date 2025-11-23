from flask import request, jsonify
from models import db, Scenario, Business, User


class ScenarioController:
    @staticmethod
    def create_scenario():
        data = request.get_json()

        if not data or not data.get("business_id"):
            return jsonify({"error": "business_id is required"}), 400

        business = Business.query.get(data["business_id"])
        if not business:
            return jsonify({"error": "Business not found"}), 404

        if "run_by" in data and data["run_by"]:
            user = User.query.get(data["run_by"])
            if not user:
                return jsonify({"error": "User not found"}), 404

        scenario = Scenario(
            business_id=data["business_id"],
            name=data.get("name"),
            params=data.get("params"),
            result_summary=data.get("result_summary"),
            run_by=data.get("run_by"),
        )

        db.session.add(scenario)
        db.session.commit()

        return jsonify(
            {
                "id": scenario.id,
                "business_id": scenario.business_id,
                "name": scenario.name,
                "created_at": scenario.created_at.isoformat()
                if scenario.created_at
                else None,
                "params": scenario.params,
                "result_summary": scenario.result_summary,
                "run_by": scenario.run_by,
            }
        ), 201

    @staticmethod
    def get_scenarios():
        scenarios = Scenario.query.all()
        return jsonify(
            [
                {
                    "id": scenario.id,
                    "business_id": scenario.business_id,
                    "name": scenario.name,
                    "created_at": scenario.created_at.isoformat()
                    if scenario.created_at
                    else None,
                    "params": scenario.params,
                    "result_summary": scenario.result_summary,
                    "run_by": scenario.run_by,
                }
                for scenario in scenarios
            ]
        )

    @staticmethod
    def get_scenario(scenario_id):
        scenario = Scenario.query.get(scenario_id)
        if not scenario:
            return jsonify({"error": "Scenario not found"}), 404

        return jsonify(
            {
                "id": scenario.id,
                "business_id": scenario.business_id,
                "name": scenario.name,
                "created_at": scenario.created_at.isoformat()
                if scenario.created_at
                else None,
                "params": scenario.params,
                "result_summary": scenario.result_summary,
                "run_by": scenario.run_by,
            }
        )

    @staticmethod
    def update_scenario(scenario_id):
        scenario = Scenario.query.get(scenario_id)
        if not scenario:
            return jsonify({"error": "Scenario not found"}), 404

        data = request.get_json()

        if "business_id" in data:
            business = Business.query.get(data["business_id"])
            if not business:
                return jsonify({"error": "Business not found"}), 404
            scenario.business_id = data["business_id"]

        if "name" in data:
            scenario.name = data["name"]

        if "params" in data:
            scenario.params = data["params"]

        if "result_summary" in data:
            scenario.result_summary = data["result_summary"]

        if "run_by" in data:
            if data["run_by"]:
                user = User.query.get(data["run_by"])
                if not user:
                    return jsonify({"error": "User not found"}), 404
            scenario.run_by = data["run_by"]

        db.session.commit()

        return jsonify(
            {
                "id": scenario.id,
                "business_id": scenario.business_id,
                "name": scenario.name,
                "created_at": scenario.created_at.isoformat()
                if scenario.created_at
                else None,
                "params": scenario.params,
                "result_summary": scenario.result_summary,
                "run_by": scenario.run_by,
            }
        )

    @staticmethod
    def delete_scenario(scenario_id):
        scenario = Scenario.query.get(scenario_id)
        if not scenario:
            return jsonify({"error": "Scenario not found"}), 404

        db.session.delete(scenario)
        db.session.commit()

        return jsonify({"message": "Scenario deleted successfully"})

    @staticmethod
    def get_scenarios_by_business(business_id):
        business = Business.query.get(business_id)
        if not business:
            return jsonify({"error": "Business not found"}), 404

        scenarios = Scenario.query.filter_by(business_id=business_id).all()
        return jsonify(
            [
                {
                    "id": scenario.id,
                    "business_id": scenario.business_id,
                    "name": scenario.name,
                    "created_at": scenario.created_at.isoformat()
                    if scenario.created_at
                    else None,
                    "params": scenario.params,
                    "result_summary": scenario.result_summary,
                    "run_by": scenario.run_by,
                }
                for scenario in scenarios
            ]
        )

    @staticmethod
    def get_scenarios_by_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        scenarios = Scenario.query.filter_by(run_by=user_id).all()
        return jsonify(
            [
                {
                    "id": scenario.id,
                    "business_id": scenario.business_id,
                    "name": scenario.name,
                    "created_at": scenario.created_at.isoformat()
                    if scenario.created_at
                    else None,
                    "params": scenario.params,
                    "result_summary": scenario.result_summary,
                    "run_by": scenario.run_by,
                }
                for scenario in scenarios
            ]
        )
