import json
from pathlib import Path


def test_every_file_is_a_record_in_its_task_folder():
    for path in Path("results").rglob("*.json"):
        record = json.loads(path.read_text())
        task = record["task_name"]
        assert path.parent == Path("results") / task, (
            f"{path}: belongs in results/{task}/"
        )
        assert path.name.startswith(f"{task}__"), (
            f"{path}: name must start with {task}__"
        )
        for key in ("corpus_id", "gym_revision", "config", "diagnostics", "ratings"):
            assert key in record, f"{path}: missing {key}"
        assert {"models", "model_revisions", "query_set"} <= record["config"].keys(), (
            f"{path}: incomplete config"
        )
        for rating in record["ratings"]:
            assert {
                "model",
                "revision",
                "rating",
                "ci_low",
                "ci_high",
            } <= rating.keys(), f"{path}: incomplete rating"
