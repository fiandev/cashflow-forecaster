from flask import request, jsonify
from models import db, ModelRun, Model


class ModelRunController:
    @staticmethod
    def create_model_run():
        data = request.get_json()

        if not data or not data.get("model_id"):
            return jsonify({"error": "model_id is required"}), 400

        model = Model.query.get(data["model_id"])
        if not model:
            return jsonify({"error": "Model not found"}), 404

        model_run = ModelRun(
            model_id=data["model_id"],
            input_summary=data.get("input_summary"),
            output_summary=data.get("output_summary"),
            run_status=data.get("run_status", "completed"),
            notes=data.get("notes"),
        )

        db.session.add(model_run)
        db.session.commit()

        return jsonify(
            {
                "id": model_run.id,
                "model_id": model_run.model_id,
                "run_at": model_run.run_at.isoformat() if model_run.run_at else None,
                "input_summary": model_run.input_summary,
                "output_summary": model_run.output_summary,
                "run_status": model_run.run_status,
                "notes": model_run.notes,
            }
        ), 201

    @staticmethod
    def get_model_runs():
        model_runs = ModelRun.query.all()
        return jsonify(
            [
                {
                    "id": run.id,
                    "model_id": run.model_id,
                    "run_at": run.run_at.isoformat() if run.run_at else None,
                    "input_summary": run.input_summary,
                    "output_summary": run.output_summary,
                    "run_status": run.run_status,
                    "notes": run.notes,
                }
                for run in model_runs
            ]
        )

    @staticmethod
    def get_model_run(run_id):
        model_run = ModelRun.query.get(run_id)
        if not model_run:
            return jsonify({"error": "Model run not found"}), 404

        return jsonify(
            {
                "id": model_run.id,
                "model_id": model_run.model_id,
                "run_at": model_run.run_at.isoformat() if model_run.run_at else None,
                "input_summary": model_run.input_summary,
                "output_summary": model_run.output_summary,
                "run_status": model_run.run_status,
                "notes": model_run.notes,
            }
        )

    @staticmethod
    def update_model_run(run_id):
        model_run = ModelRun.query.get(run_id)
        if not model_run:
            return jsonify({"error": "Model run not found"}), 404

        data = request.get_json()

        if "model_id" in data:
            model = Model.query.get(data["model_id"])
            if not model:
                return jsonify({"error": "Model not found"}), 404
            model_run.model_id = data["model_id"]

        if "input_summary" in data:
            model_run.input_summary = data["input_summary"]

        if "output_summary" in data:
            model_run.output_summary = data["output_summary"]

        if "run_status" in data:
            model_run.run_status = data["run_status"]

        if "notes" in data:
            model_run.notes = data["notes"]

        db.session.commit()

        return jsonify(
            {
                "id": model_run.id,
                "model_id": model_run.model_id,
                "run_at": model_run.run_at.isoformat() if model_run.run_at else None,
                "input_summary": model_run.input_summary,
                "output_summary": model_run.output_summary,
                "run_status": model_run.run_status,
                "notes": model_run.notes,
            }
        )

    @staticmethod
    def delete_model_run(run_id):
        model_run = ModelRun.query.get(run_id)
        if not model_run:
            return jsonify({"error": "Model run not found"}), 404

        db.session.delete(model_run)
        db.session.commit()

        return jsonify({"message": "Model run deleted successfully"})

    @staticmethod
    def get_model_runs_by_model(model_id):
        model = Model.query.get(model_id)
        if not model:
            return jsonify({"error": "Model not found"}), 404

        model_runs = ModelRun.query.filter_by(model_id=model_id).all()
        return jsonify(
            [
                {
                    "id": run.id,
                    "model_id": run.model_id,
                    "run_at": run.run_at.isoformat() if run.run_at else None,
                    "input_summary": run.input_summary,
                    "output_summary": run.output_summary,
                    "run_status": run.run_status,
                    "notes": run.notes,
                }
                for run in model_runs
            ]
        )

    @staticmethod
    def get_model_runs_by_status(run_status):
        model_runs = ModelRun.query.filter_by(run_status=run_status).all()
        return jsonify(
            [
                {
                    "id": run.id,
                    "model_id": run.model_id,
                    "run_at": run.run_at.isoformat() if run.run_at else None,
                    "input_summary": run.input_summary,
                    "output_summary": run.output_summary,
                    "run_status": run.run_status,
                    "notes": run.notes,
                }
                for run in model_runs
            ]
        )
