# Valpo Physics Animations

Editable physics and mathematics animations made with **Manim Community Edition**.
The initial collection contains seven portrait-format scenes. Everything needed to
build the scenes is source code: no external images, detector data, or TeX installation
is required. Rendered movies and intermediate caches are not committed.

## Browse by topic

| Topic | Animation | Source and scene |
| --- | --- | --- |
| Convolution | Overlap of two unit disks | [circles.py](convolution/circles.py) · `CircleConvolution` |
| Convolution | Unit disks on an offset path | [offset_circles.py](convolution/offset_circles.py) · `OffsetCircleConvolution` |
| Stars and eclipses | Partial eclipse of equal, uniformly bright stars | [partial_eclipse.py](stars/partial_eclipse.py) · `PartialStellarEclipse` |
| Landau × Gaussian | Smooth convolution of a broad Landau and narrower Gaussian | [smooth_langau.py](langau/smooth_langau.py) · `SmoothLangau` |
| Numerical integration | Genuine undersampling artifacts in Langau quadrature | [langau.py](langau/langau.py) · `LangauUndersampling` |
| Numerical integration | Midpoint rectangles and missed narrow peaks | [langau_rectangles.py](langau/langau_rectangles.py) · `LangauMidpointRectangles` |
| Numerical integration | Inputs, product, and midpoint boxes together | [langau_overlap_rectangles.py](langau/langau_overlap_rectangles.py) · `LangauOverlapRectangles` |

Topic notes: [Convolution](convolution/README.md), [Stars](stars/README.md), [Langau](langau/README.md).

## Setup

Install [Miniforge](https://github.com/conda-forge/miniforge), then run:

```sh
git clone https://github.com/paulnord/valpo-physics-animations.git
cd valpo-physics-animations
conda env create -f environment.yml
conda activate valpo-physics-animations
python -m manim --version
```

The environment pins Python 3.12, Manim 0.22.1, NumPy 2.5.4, and SciPy 1.18.1,
matching the tested rendering environment. Conda resolves platform-specific
transitive dependencies; this is not a fully locked environment. Manim requires
native Cairo/Pango libraries, which conda-forge supplies. SciPy must provide
`scipy.stats.landau`. Text uses DejaVu Sans, with fonts supplied by the environment.

## Render

Run from the repository root. Scene files set a **900 × 1600**, **24 fps** portrait
canvas themselves, so quality flags do not reliably override those settings.

```sh
python -m manim --renderer cairo convolution/circles.py CircleConvolution
python -m manim --renderer cairo convolution/offset_circles.py OffsetCircleConvolution
python -m manim --renderer cairo stars/partial_eclipse.py PartialStellarEclipse
python -m manim --renderer cairo langau/smooth_langau.py SmoothLangau
python -m manim --renderer cairo langau/langau.py LangauUndersampling
python -m manim --renderer cairo langau/langau_rectangles.py LangauMidpointRectangles
python -m manim --renderer cairo langau/langau_overlap_rectangles.py LangauOverlapRectangles
```

Manim prints the output path under `media/videos/`. Add `-p` to open a rendered
movie locally. For a fast final-frame check instead of a movie, use `-s`:

```sh
python -m manim -s --renderer cairo stars/partial_eclipse.py PartialStellarEclipse
```

Edit `config.pixel_width`, `config.pixel_height`, and `config.frame_rate` at the top
of a source file to change output resolution or frame rate. Keep `frame_width` and
`frame_height` unchanged to retain the layout. Render each source in a separate
command because these files configure Manim globally.

## Checks

```sh
python -m compileall -q convolution stars langau tests
python -m unittest discover -s tests -v
```

The tests check disk overlap geometry, eclipse flux, finite/nonnegative Langau
values, consistency of the three quadrature variants, and smooth-convolution
convergence. They do not replace inspecting a rendered movie.

## References

- [Manim Community documentation](https://docs.manim.community/)
- [SciPy Landau distribution](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.landau.html)
- [ROOT Landau–Gaussian convolution tutorial](https://root.cern.ch/doc/master/langaus_8C.html)

These scenes are illustrative teaching models, not fits to measured data.
