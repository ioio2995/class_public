# ROFT extension for CLASS

This branch adds a phenomenological late--time dark energy model where the fluid
obeys
\(w(a) = -1 + \alpha / [3 R(a)]\) with \(R(a) = 1 - \alpha \ln a\).
The implementation introduces two new input parameters:

- `alpha_roft` &mdash; controls the deviation from $\Lambda$CDM. Setting
  `alpha_roft = 0` exactly reproduces $\Lambda$CDM.
- `roft_model` &mdash; selects the variant of the model. At the moment only the
  `add` model is implemented. A future `lapse` model is blocked by a safety
  check.

## Example run

An example configuration is provided in `test_roft.ini`:

```
./class test_roft.ini
```

The file enables background and perturbation outputs for `alpha_roft = 0.1`.
To compare with the $\Lambda$CDM limit set `alpha_roft = 0` in the same file.

## Regression check

A small script `scripts/test_roft_regression.py` runs CLASS twice and checks that
`alpha_roft = 0` matches a pure $\Lambda$CDM run within $10^{-4}$ for the
background expansion and CMB spectra:

```
python scripts/test_roft_regression.py
```

## Notes

The code guards against negative values of $R(a)$; if this happens CLASS will
stop with an error message. Only the `add` model affects the background and
perturbations. The `lapse` option is reserved for future work.
