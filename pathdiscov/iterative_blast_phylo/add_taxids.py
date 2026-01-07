import csv
import time
from Bio import Entrez
import sys
Entrez.email = "your.email@example.com"  # REQUIRED

INPUT_TSV = sys.argv[1]
OUTPUT_TSV = sys.argv[2]
# OUTPUT_TSV = INPUT_TSV + ".ann"
NCBI_DB = "nuccore"  # change to "protein" if needed
BATCH_SIZE = 50      # safe batch size
SLEEP_SEC = 0.4      # rate limiting


def fetch_taxids(refseq_ids):
    """Fetch TaxIDs for a list of RefSeq accessions using esummary."""
    taxid_map = {}

    handle = Entrez.esummary(
        db=NCBI_DB,
        id=",".join(refseq_ids),
        retmode="xml"
    )
    summaries = Entrez.read(handle)
    handle.close()

    for summary in summaries:
        acc = summary["AccessionVersion"]
        taxid = summary.get("TaxId")
        desc = summary.get("Title")
        taxid_map[acc] = (taxid, desc)

    return taxid_map


# ---- Read input TSV ----
with open(INPUT_TSV) as infile:
    fieldnames = ["contig_id", "refseq_id", "97.007", "2138", "64", "0", "20", "2157", "1", "2138", "0.0", "3594"]
    reader = csv.DictReader(infile, delimiter="\t", fieldnames=fieldnames)
    rows = list(reader)

    fieldnames = reader.fieldnames


# ---- Collect RefSeq IDs needing lookup ----
to_lookup = []
for row in rows:
   to_lookup.append(row["refseq_id"])

# Deduplicate while preserving order
to_lookup = list(dict.fromkeys(to_lookup))

# ---- Batch Entrez lookups ----
taxid_lookup = {}

for i in range(0, len(to_lookup), BATCH_SIZE):
    batch = to_lookup[i:i + BATCH_SIZE]
    try:
        taxid_lookup.update(fetch_taxids(batch))
        time.sleep(SLEEP_SEC)
    except Exception as e:
        print("Warning: batch failed ({batch}): ", str(e))

# ---- Update rows ----
for row in rows:
    row["taxid"] = int(taxid_lookup.get(row["refseq_id"], ["-1",""])[0])
    row["description"] = taxid_lookup.get(row["refseq_id"], ["-1",""])[1]

# ---- Write output TSV ----
# with open(OUTPUT_TSV, "w", newline="") as outfile:
#     writer = csv.DictWriter(outfile, fieldnames=fieldnames + ["taxid", "description"], delimiter="\t")
#     writer.writeheader()
#     writer.writerows(rows)
ann_rows = [ [x["contig_id"], x["taxid"], x["description"]] for x in rows ]
with open(OUTPUT_TSV, "w") as outfile:
    # writer = csv.DictWriter(outfile, fieldnames=fieldnames + ["taxid", "description"], delimiter="\t")
    writer = csv.writer(outfile, delimiter="\t")
    # writer.writeheader()
    writer.writerows(ann_rows)
# print(f"Done. Wrote {OUTPUT_TSV}")

