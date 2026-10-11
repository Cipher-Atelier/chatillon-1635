# Read this investigation

[Repository overview](README.md) · [Technical verification](verification/README.md)

## Understand the document

Châtillon’s cipher letter to Servien from Nijmegen, dated 3 August 1635. Graphical signs and numerical groups are compared with possible clear-text counterparts.

Start with the [source catalogue or manuscript](https://gallica.bnf.fr/ark:/12148/btv1b9058223v/f135.item). It identifies the historical object. The source image is the evidence; the tables in this repository are recorded readings of that evidence.

## Read the current result

This is an unfinished reconstruction and a test of assumptions, not a complete decipherment. The current reproducible result shows how the possible reading of a crossed sign changes when the neighboring numeral N2 is allowed to emit more letters.

Open [Saved assumption-test results](verification/experiments/verification_results.json) and the [research account](chatillon-1635/README.md). A literal preserves the recorded output before making it smoother to read. An English explanation or translation adds interpretation and should not silently repair it.

Example:

```text
N2: one letter → {f}; up to eight letters → {e, f, n, r}
```

These sets describe outputs allowed by a declared alignment model. They do not establish the historical meaning of N2 or of the crossed sign.

The successful local repeat example does not validate a global repeat operator. Complete-passage fits fail or depend on exposed text and grouping assumptions. No complete plaintext or unique full key is available. The [saved-width package](verification/experiments/chatillon-width-spectrum-20261007/README.txt) checks 384 historical records separately. The [equality diagnostic](verification/experiments/chatillon-slash-loop-consistency-20261011/README.md) and [source audit](verification/experiments/chatillon-source-glyph-audit-20261011/README.md) are also published; [their separate command scopes](verification/README.md#separate-package-scopes) distinguish them from the baseline replay. A full literal or translated edition is not included.

## Check one example by hand

1. Open the [recorded test results](verification/experiments/verification_results.json). Under `closed_values_by_n2_max_width`, the key `"1"` lists `["f"]`, while `"8"` lists `["e", "f", "n", "r"]`.
2. Here *width* means the number of output letters a cipher group may consume. If N2 consumes one letter under the retained assumptions, the tested closed sign is forced to `f`. Allowing N2 to consume up to eight letters permits four candidate values instead.
3. Open [config.json](verification/experiments/chatillon-1635/config.json). `active_mapping` contains nine inherited assignments, including a conditional `N2: "r"`; `scenarios` retains source grouping and wording alternatives. An entry in this configuration is an assumption to test, not a recovered historical key value.
4. The automated verifier enumerates 512 subsets of nine assignments across 12 recorded conditions: `512 × 12 = 6,144`. Several conditions share the same reachable alignment problem. They are not 6,144 independent confirmations. The separate width test covers 24 conditions.
5. Follow the [research account’s manuscript links](chatillon-1635/README.md#research-task) to check letter boundaries and the source groups on views 139–140. The royal letter on the opposite page is a different document.

This example checks a dependency in the proposed model. A securely bounded same-key occurrence establishing N2’s output length, a contemporary key or an independent literal witness would test the historical interpretation more strongly.

## Choose the check you want

- **Understand the result:** read the literal/test result beside the research account. You can do this in GitHub without installing anything.
- **Check the calculation:** follow the example above, then [run the supported Python check](verification/README.md). This verifies the saved transformation or declared model.
- **Check the source:** compare recorded signs with the original image and retain disagreements. Scans/crops are not included; obtain access under the provider’s terms. Original coordinates, when present, refer to the specified image version.
- **Evaluate the historical reading:** examine alternative signs, key evidence, language, document boundaries and prior readings. A successful calculation does not settle these questions.

To report a problem, use [Work on existing research](https://github.com/Cipher-Atelier/chatillon-to-servien-cipher-letter-1635/issues/new?template=research.yml). Give the file, row/position, source reference, your observation, and what changes in the output. Distinguish a different source reading from a changed key or an editorial interpretation.

## What the files mean

| Open this | It contains |
| --- | --- |
| [Research account](chatillon-1635/README.md) | Historical context, method, interpretation, credits and limits |
| [Saved assumption-test results](verification/experiments/verification_results.json) | The saved text or bounded test result |
| [Recorded source groups and model assumptions](verification/experiments/chatillon-1635/config.json) | The recorded input/assignments used in the example |
| [Conditional inherited mappings](verification/experiments/chatillon-1635/config.json) | The proposed transformation, historical key, or tested assumptions |
| [Technical verification](verification/README.md) | Setup, command, expected output and what the check covers |
| [Source scope](verification/TOPIC_SCOPE_INDEX.json) | Machine-readable release boundaries and omitted material |
| [Publication provenance](SOURCE_PROVENANCE.json) | Where this package came from and what documentation changed |

CSV and TSV are tables: GitHub or a spreadsheet can display them. TSV uses tabs between columns. JSON stores named fields and lists; `null` means no value in that field, and its interpretation depends on the record. You do not need to start by reading every JSON file.

## Terms used in the research

- **Ciphertext:** the recorded encrypted signs or letters.
- **Key/mapping:** the rule assigning output to a cipher sign. It may be a hypothesis, a surviving historical key, or an assumption in a test; those are different kinds of evidence.
- **Literal reading:** the saved output with gaps and awkward wording retained, before editorial translation or repair.
- **Coverage:** how many recorded positions receive a value. It does not measure how many values are historically correct.
- **Frozen:** saved unchanged at a particular stage so a later correction cannot replace an earlier test result.
- **Replay:** applying saved rules to saved inputs again. It checks reproducibility within the declared scope.
- **Training/heldout:** material used to fit a rule, and material excluded from that fitting. Prior viewing or later correction can limit how independent a heldout test is; read the case-specific account.
