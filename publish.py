"""Publish one gym output folder: its records into results/<task>/, its queries and verdicts to the dataset."""

import argparse
import json
import shutil
import tempfile
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "folder", type=Path, help="a gym output folder holding one task's runs"
    )
    ap.add_argument("--dataset", default="mteb/gym-runs")
    ap.add_argument(
        "--pr",
        action="store_true",
        help="open a pull request on the dataset instead of committing",
    )
    args = ap.parse_args()

    records = sorted((args.folder / "records").glob("*.json"))
    tasks = {json.loads(p.read_text())["task_name"] for p in records}
    if len(tasks) != 1:
        raise SystemExit(
            f"expected the records of one task, found {sorted(tasks) or 'none'}"
        )
    task = tasks.pop()

    out = Path("results") / task
    out.mkdir(parents=True, exist_ok=True)
    for p in records:
        shutil.copy(p, out / p.name)

    with tempfile.TemporaryDirectory() as tmp:
        staged = Path(tmp)
        (staged / "queries" / task).mkdir(parents=True)
        for p in (args.folder / "queries").glob("*.json"):
            shutil.copy(p, staged / "queries" / task / p.name)

        # a pair's verdicts are streamed to a .jsonl and snapshotted to a .json: publish each comparison once
        (staged / "verdicts" / task).mkdir(parents=True)
        for stem in sorted(
            {p.stem for p in (args.folder / "verdicts").glob("*.json*")}
        ):
            by_qid = {}
            jsonl = args.folder / "verdicts" / f"{stem}.jsonl"
            if jsonl.exists():
                by_qid.update(
                    {
                        v["qid"]: v
                        for v in map(json.loads, jsonl.read_text().splitlines())
                        if v
                    }
                )
            snapshot = args.folder / "verdicts" / f"{stem}.json"
            if snapshot.exists():
                by_qid.update({v["qid"]: v for v in json.loads(snapshot.read_text())})
            lines = "".join(json.dumps(v) + "\n" for v in by_qid.values())
            (staged / "verdicts" / task / f"{stem}.jsonl").write_text(lines)

        from huggingface_hub import upload_folder

        commit = upload_folder(
            repo_id=args.dataset,
            repo_type="dataset",
            folder_path=staged,
            commit_message=f"{task}: queries and verdicts",
            create_pr=args.pr,
        )
    print(f"{len(records)} records -> {out}\nqueries and verdicts -> {commit}")


if __name__ == "__main__":
    main()
