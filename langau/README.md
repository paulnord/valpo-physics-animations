# Landau–Gaussian convolution and quadrature

- [SmoothLangau](smooth_langau.py): Landau scale `xi=1`, MPV 0, Gaussian `sigma=0.45`.
  Integrates the Gaussian coordinate over `[-8, 8]` with Gauss–Legendre quadrature.
- [LangauUndersampling](langau.py): narrow Landau scale `xi=0.012`, Gaussian `sigma=1`.
  Demonstrates artifacts from a moving, finite midpoint grid.
- [LangauMidpointRectangles](langau_rectangles.py): shows the actual midpoint sum boxes.
- [LangauOverlapRectangles](langau_overlap_rectangles.py): shows both inputs and their
  product together with the midpoint boxes.

The three narrow-Landau scenes integrate over `x ± 5 sigma`, starting from 100
midpoints. Their waves come from the sampled integral rather than decorative
oscillations. Displayed inputs in the overlap-boxes scene are peak-normalized;
the physical output restores both peak normalization factors.

The Landau distribution has no finite standard deviation: `xi` is a scale
parameter. The source transforms SciPy's Landau parameterization into the
ROOT/CERN convention. These parameters illustrate numerical behavior and do not
represent a particular detector fit. Comments recording earlier ROOT comparisons
are provenance; the included tests do not require or run ROOT.

See the [root README](../README.md#render) for render commands and references.
