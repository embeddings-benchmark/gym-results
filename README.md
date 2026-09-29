# MTEB Gym results

Results of [MTEB Gym](https://github.com/embeddings-benchmark/MTEB-gym-v2), which ranks embedding models on a corpus with an LLM judge.

Each file under `results/<task>/` is the record of one run: the dataset and its revision, the gym and mteb versions, the configuration (models and their revisions, judge and generator with their settings, the queries, the pairs judged), the judge's diagnostics, and for each model its rating with a confidence interval, its wins, losses and ties, and its nDCG@10.

The queries and judge verdicts behind the records are in the dataset [mteb/gym-runs](https://huggingface.co/datasets/mteb/gym-runs):

```text
queries/<task>/<query set>.json      the generated queries; a record's config.query_set names its file
verdicts/<task>/<pair>-<key>.jsonl   one line per comparison; the key identifies the judge and its settings
```

Retrieval predictions are not stored. They are rerun from a record's models, revisions and query set.

## Adding results

Run the gym with one output folder per task, then:

```bash
make install
uv run --group publish python publish.py <output folder> --pr
```

This copies the folder's records into `results/<task>/` and opens a pull request on the dataset with its queries and verdicts. Commit the records and open a pull request here.

## License

CC0.
