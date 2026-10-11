# Châtillon source glyph limitation audit, 11 October 2026

The named pair `v139R_C01_023` / `v139R_C02_017` remains **UNRESOLVED under the frozen source gate**, regardless of later anonymous crop ratings. Ordered local anchors support proposed physical locations conditional on the supplied old-ID sequence. They do not independently establish the full row ordering, the grouping of the earlier C02 cluster, or the historical coordinates. This audit neither repairs that criterion nor supplies a cipher key or reruns the earlier calculations.

Read [SOURCE_GATE_REVIEW.txt](SOURCE_GATE_REVIEW.txt) for the reason, [PRE_OBSERVER_SCOPE.json](PRE_OBSERVER_SCOPE.json) for the scope recorded before observer ratings, and [FROZEN_PROTOCOL.json](FROZEN_PROTOCOL.json) for the unchanged rubric. The localizer's narrower “PASS” statements are retained as reported findings; they are not the overall gate decision.

## Source and capture provenance

The document is BnF Français 3758, item 104, Châtillon to Servien, 3 August 1635; the inspected region is the right-hand page of Gallica view 139. The exact source URLs are:

- [Item viewer](https://gallica.bnf.fr/ark:/12148/btv1b9058223v/f139.item)
- [Observed high-resolution derivative](https://gallica.bnf.fr/ark:/12148/btv1b9058223v/f139.highres)
- [Zoom viewer used for captures](https://gallica.bnf.fr/ark:/12148/btv1b9058223v/f139.item.zoom)

These URLs identify the source view, not a guarantee that a future viewer session returns the same bytes, viewport, pan or scale. The screenshots are JPEG viewer display derivatives, not archival masters. No rotation, EXIF reorientation, interpolated enlargement, generative enhancement or stroke edits were used for the inspection packet.

| Recorded image | Dimensions | Bytes | SHA256 | Metadata |
| --- | --- | --- | --- | --- |
| High-resolution derivative | 1366 × 1054 | 319228 | `280e87f86231baf87abe40d7679aeed7c9fc11796db7ec22b9863fbe067853f0` | [SOURCE_IMAGE.json](SOURCE_IMAGE.json) |
| First zoom capture | 1816 × 1129 | 216484 | `e3a53c0e7640abc0a7fbea220729448c71b8df7dbd028375c92956a5c185c287` | [CAPTURE_IMAGE.json](CAPTURE_IMAGE.json) |
| Second zoom capture | 1816 × 1129 | 263975 | `1914bffa3e1947bbc9fda70f6670ed88531347a200b00ba7b9a9d3652c1151c4` | [CAPTURE_IMAGE_02.json](CAPTURE_IMAGE_02.json) |

The first capture is retained as failed coverage evidence: the second target's neighborhood lay outside its main viewport. No second-target box is certified in that capture. The second capture supports the reported local attachment of both selected positions, but its missing first-line prefix and cropped earlier second-line cluster leave the stronger ordering and grouping requirements unresolved. Coordinates from one capture must not be transferred to another.

The Library original archive remains unresolved: **“Library prepare_materialize is not available”**. This package makes no claim to have materialized that archive, recovered its original coordinate map, or obtained it through an access workaround. The frozen protocol retains the historical inventory name and expected hash as provenance references only.

## Proposed native coordinate correspondences

The convention is `[x, y, width, height]`, integer decoded-image pixels from the upper-left origin, with a half-open rectangle. These are isolating boxes, not exact ink masks. The reported alternatives, missing prefix, unresolved cluster and edge tolerances remain in [LOCALIZER_REPORT.txt](LOCALIZER_REPORT.txt) and [LOCALIZER_CAPTURE_SUPPLEMENT.txt](LOCALIZER_CAPTURE_SUPPLEMENT.txt).

| Selected old-ID location | Derivative native box / line context | Capture 02 box / reported context |
| --- | --- | --- |
| C01_023 | `[1262,95,17,21]` / `[798,95,482,36]` | `[1334,328,74,104]` / `[213,328,1195,198]` |
| C02_017 | `[1075,128,15,25]` / `[800,120,483,42]` | `[200,531,82,110]` / `[11,483,1429,170]` |

[COORDINATOR_REGISTRY.json](COORDINATOR_REGISTRY.json) records the realized randomized presentation order, controls and source regions. [PACKET_SPEC.json](PACKET_SPEC.json) records the exact crop and local boundary-context rectangles used in the anonymous packet. Those contexts are selected local regions; they do not independently supply the missing full-line ordering evidence. [PACKET_MANIFEST.json](PACKET_MANIFEST.json) records the native and optional 3× PNG hashes, sizes and relative packet paths. The referenced PNGs are withheld and are not links to published image files.

## Frozen timing, observer scope and AI roles

The protocol was locally recorded before new source-localization and class ratings. Registry order and controls were locally recorded before observer ratings. This is **local ordering only, not an independently authenticated preregistration**; timestamps and hashes do not attest to uninspected workflow events.

The coordinator knew the earlier calculations. A source-only AI localizer inspected authorized source pixels and annotations. A separate AI source-gate reviewer read only the frozen protocol, localization input and two localizer reports, with no pixel inspection or class-rating remit. Requested Opus/Sonnet models were unavailable; these roles used the allowed inherited AI model. A fresh AI observer was scoped to anonymous crops, the unchanged feature rubric and no inherited conversation. The implementation assistant prepared packet code and this publication package; it did not visually inspect or rate the private images. The optional read-only verifier decodes the explicitly supplied exact capture for automated byte and dimension checks only. These are disclosed AI roles, not external human expert validation.

[BLINDED_OBSERVER_PROMPT.txt](BLINDED_OBSERVER_PROMPT.txt) is a disclosed path-redacted publication copy of the actual prompt. It is not presented as byte-identical to the local original. Anonymous crop descriptions, raw observer responses and control outcomes are ancillary. They cannot establish an admissible physical-class conclusion for the named historical pair while its source gate is unresolved.

## Recorded ancillary outcome

[BLINDED_OBSERVER_RAW.txt](BLINDED_OBSERVER_RAW.txt) preserves the complete observer response unchanged. [RESULTS.json](RESULTS.json) records its decisions and the unchanged all-controls-pass rule. **The control gate FAILED: 3 of 4 controls passed.** No control was replaced, no rating was retried, and no readability criterion was repaired after the response.

| Anonymous pair | Frozen coordinator role | Raw observer decision | Control outcome |
| --- | --- | --- | --- |
| P01 | Positive duplicate 1 | `same_physical_class` | Passed |
| P02 | Negative 2 | `different_physical_class` | Passed |
| P03 | Selected target crops | `unresolved` | Ancillary target, not a control |
| P04 | Negative 1 | `different_physical_class` | Passed |
| P05 | Positive duplicate 2 | `unresolved` | Failed |

P05 contains the same crop bytes on both sides, but the observer could not resolve attachment versus detachment of a faint upper-right trail. Under the frozen requirement that every critical feature be readable, it rated that control unresolved. Byte identity confirms duplicate construction; it does not override the raw rating or change the control gate.

For P03, the observer described a readable lower enclosure in B, while dense ink obscured the corresponding enclosure and attachment in A. It could establish neither agreement nor a stable difference. Do not infer a loop's absence from that unreadability. The ancillary target interpretation is invalidated by the failed control gate, and the named final decision remains **UNRESOLVED** independently because its source gate was already unresolved before observer ratings.

[RUNTIME_AND_CHECKS.json](RUNTIME_AND_CHECKS.json) preserves the recorded Python 3.13.9 / Pillow 11.3.0 runtime, original builder hash and coordinator integrity-check account. Those accounts and hashes establish recorded data provenance, not external validation of the scientific gates.

## Text integrity and public reproducibility limits

Only selected text, JSON and Python are published here. Source images, crops, screenshots, archives, cookies, browser inventories, Library IDs and private notes are excluded. Source-specific credits and restrictions still apply; no image redistribution permission or blanket licence is asserted.

[PUBLICATION_TRANSFORMS.json](PUBLICATION_TRANSFORMS.json) records the original SHA256 and publication SHA256 for every copied artifact. Frozen internal references to originals are unchanged. In source/capture metadata, filesystem-location keys `path` / `local_path` were removed; the remaining JSON values were retained. The localization input and observer prompt replace only the exact original workspace prefix with `<LOCAL_WORKSPACE>`. The prefix is identified by its SHA256 in the disclosure rather than republished. Other selected artifacts are copied verbatim. Published-byte checks and original-hash provenance claims are distinct: original bytes of transformed files are not available in the public package for independent rehashing.

Run this package's independent read-only integrity check:

```sh
python3 verification/experiments/chatillon-source-glyph-audit-20261011/verify_audit.py
```

The default uses only the Python standard library. It checks the package SHA256 manifest, publication transformations, recorded original-hash references, source associations, frozen scope and crop rectangles/dimensions. It does not load images, access the network, write files, rerun historical experiments or validate a cipher key. Successful metadata verification cannot independently validate the withheld pixels, localizer observations, control ground truth or named-ID binding.

If you already possess a manually supplied **exact capture 02** matching its recorded SHA256, optional Pillow verification recomputes the packet PNGs in memory and compares them with the recorded hashes and dimensions:

```sh
python3 verification/experiments/chatillon-source-glyph-audit-20261011/verify_audit.py \
  --source /your/local/exact-capture-02.jpg
```

This performs no disk writes. It rejects a mismatched source. The original packet used Pillow 11.3.0; PNG encoding differences in another Pillow version may prevent byte-hash reproduction even when decoded pixels agree. No automatic download, alternate capture substitution, source repair or access workaround is provided.

To create a new local packet from that same exact source, with Pillow installed and a new output directory whose parent exists:

```sh
python3 verification/experiments/chatillon-source-glyph-audit-20261011/build_packet.py \
  --source /your/local/exact-capture-02.jpg \
  --spec verification/experiments/chatillon-source-glyph-audit-20261011/PACKET_SPEC.json \
  --output-dir /your/local/new-inspection-packet --enlarge-3x
```

The helper writes native PNG crops and boundary contexts, optionally adds nearest-neighbor 3× views, and refuses existing output directories or unsafe labels/boxes. It never copies the complete source file. Do not replace the recorded source with a similar image and call that reproduction. This separate limitation audit leaves all earlier research files and calculations unchanged.
