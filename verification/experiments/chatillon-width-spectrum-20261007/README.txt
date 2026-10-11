CHATILLON WIDTH-SPECTRUM EXPERIMENT
Historical record: 7 October 2026 | Package prepared: 11 October 2026 UTC

This text/code package preserves the saved October 7 exposed-input alignment
experiment. It is a historical sensitivity result, not a decipherment, a
recovered complete key, or an independent plaintext witness. No cipher
experiment was rerun when preparing this package.

WHAT THE SAVED RESULTS SHOW
There are 384 records: 12 named scenarios x 8 exact N2 widths x 4 control
conditions. Summing over named scenarios, the original-reference condition
has 110 prefix-alignment paths in 24 nonempty records. Every successful path
uses the conditional "sous" wording and one of two conditional token groupings;
the literal "soubz" scenarios have no saved paths. All three negative controls
(rotate, reverse, swap) have zero saved paths. These controls diagnose anchor
dependence, not statistical significance.

Exact N2 width:       1    2    3    4    5    6    7    8
Saved prefix paths: 20   10   10   30   30   10    0    0
Closed-sign output:  f    f    r  e/r  e/n    n    -    -

The alternatives r, e, and n first appear at exact widths 3, 4, and 5.
These are projections of exposed-reference alignments, not recovered key values.
Counts sum duplicated named scenarios and are not independent trials.

IMPORTANT LIMITS
- Unknown occurrences are independent slots. Repeated signs are not required
  to share a complete, coherent key. Eight inherited non-N2 mappings remain.
- The reference wording and earlier mappings were already exposed. Conditional
  spelling/token-grouping choices are not independent historical evidence.
- All saved successful paths end at positions 39, 42, or 43, counted as consumed
  characters from the start. The full references have 110 or 111 characters.
- Every strict full-reference count is zero, but this is guaranteed by the
  setup: the three grouping families can consume at most 50, 57, or 65
  characters even at N2 width 8. This zero cannot independently falsify a
  historical reading or demonstrate failure of a full-letter decipherment.
- The grandz/grands variation lies beyond the consumed prefix. The 12 named
  scenarios reduce to six effective input cases over that prefix.
- No probability, significance test, blind validation, or new primary-key
  evidence is provided. No broader search was performed for this package.

FILES
original/ contains seven byte-identical historical files. Its README and
SHA256SUMS.json refer to a DOCX report and a June-cipher data file that are
intentionally excluded from this Châtillon-only text/code package.
PROVENANCE.txt identifies the pinned input, checks, and historical caveats.
SAVED_RESULTS_SUMMARY.json is a read-only aggregation of the saved JSON.
verify_saved_artifacts.py checks integrity, record coverage, stored arithmetic,
Python syntax, and the derived summary. It does not enumerate alignment paths.
SHA256SUMS.txt covers every package file except itself.

CHECK THE PACKAGE WITHOUT RERUNNING THE EXPERIMENT
From this directory, using Python 3.8 or later, standard library only:
  python3 verify_saved_artifacts.py
Optionally, on systems providing sha256sum:
  sha256sum -c SHA256SUMS.txt
No installations, accounts, network requests, or manuscript scans are needed.

OPTIONAL HISTORICAL REPRODUCTION (NOT PERFORMED FOR THIS PACKAGE)
Work in a new directory so the saved evidence is preserved:
  mkdir replay
  cp original/test_widths.py original/independent_check.py original/config.json replay/
  python3 replay/test_widths.py
  python3 replay/independent_check.py
  cmp original/RESULTS.json replay/RESULTS.json
The first program overwrites RESULTS.json next to itself. The second checks
path counts and closed-sign/N2 histograms; it does not assert saved endpoint
histograms or strict full-reference counts. The original Python version was
not recorded in these seven files. Historical execution is not newly certified.
