French cipher key audit 7 October 2026

New test: exact N2 lengths 1..8 in saved exposed-source Châtillon alignment.
Run with Python 3 standard library only:
python test_widths.py
python independent_check.py

No installations or network are needed. test_widths.py writes RESULTS.json.
The second program explicitly enumerates paths and compares every result.
The DOCX is the four-page standalone research report. No historical scans are included.

Sources pinned:
Châtillon: Cipher-Atelier/chatillon-to-servien-cipher-letter-1635
commit 5440c0a2f845a7cb92181ea99d640dc09e508274
config.json source path verification/experiments/chatillon-1635/config.json
SHA256 b130ebb024676a41749532a473e5918078f64f572be83ed20f76a56f2b48b872
June: Cipher-Atelier/louis-xiii-cipher-letter-june-1635
commit fdd5fa83289c101eab02ca390868b1fe64397381
june_partial_predictions.json source path verification/experiments/louis-xiii-june-1635/partial_predictions.json

Model limits: every unknown occurrence is an independent slot; no coherent complete key inferred. All successful original paths use conditional sous, not literal soubz. Twelve named scenarios duplicate effective cases. Negative controls are diagnostic, not a calibrated probability. No new primary key, independent literal witness, or full decipherment obtained.
