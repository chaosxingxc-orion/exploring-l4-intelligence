# RC2R3 runtime intake addendum

The RC2R2 coding semantics and neutral instructions remain controlling. This addendum changes no
paper label and introduces no expected answer.

## Frozen agreement threshold

Every paper field, object segmentation gate and object critical-field gate uses exactly `0.85`.
`NOT_CALIBRATED` remains non-passing. A caller-supplied threshold other than `0.85` invalidates the
intake before metrics are computed.

## Receiver-side receipt

The receiver passes the exact delivered bytes for the eight allowlisted artifacts and the prompt to
the receipt builder. The builder recomputes each byte length and SHA256, the ordered bundle digest and
the prompt SHA256. It emits no receipt on a missing name, extra name, non-byte value or one-byte
difference. Coder, transaction, process and task identities are independently bound for A and B.

The receipt proves what the controlled builder observed; it is not represented as a provider-level
signature or human-independent attestation.

## Typed structural paths

Path authorization distinguishes dictionary keys from list indices before any display serialization.
Only the exact identity fields under actual `items` arrays are exempt from the named-expectation value
scan. Literal keys containing brackets, dots, slashes or JSON-pointer escape sequences receive no
identity exemption. The blind packet also rejects every unexpected top-level key.
