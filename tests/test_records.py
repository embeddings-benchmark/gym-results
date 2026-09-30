from pathlib import Path

from mteb_gym import Result


def test_records_load_with_the_gym():
    """Every file loads as a gym record and sits in results/<its task>/."""
    for path in Path("results").rglob("*.json"):
        result = Result.from_disk(path)
        task = result.record["task_name"]
        assert path.parent == Path("results") / task, f"{path}: belongs in results/{task}/"
        assert not result.to_dataframe().empty, f"{path}: no ratings"
