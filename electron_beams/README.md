# Busch method: electron charge-to-mass ratio (e/m)

[BuschBeamCinematic.py](BuschBeamCinematic.py) is the recovered, text-free 3D Manim
scene. It shows an electron beam sweeping across a screen, discrete launch angles
becoming a ray bundle, and magnetic focusing as the field parameter changes.

## Source and preservation

Recovered from the saved `BuschBeamCinematic_text_removed.py` attachment dated
April 7, 2026. The only source edit for this repository was removing the leading
Jupyter/Colab command `%%writefile BuschBeamCinematic.py` so the file runs as an
ordinary Python module. Comments, parameters, camera presets, and animation logic
are otherwise preserved.

**This saved version already comments out several field ramps and camera moves**,
including the second-focus ramp. Those sections are retained as comments, not
silently restored. The active sequence includes the single-beam sweep, discrete
positions, continuous bundle, first focus, a ramp to 1.5 turns, an oblique camera
move, and a return to half a turn. It should not be described as a fully active
seven-act sequence.

## Render

Use the repository's [environment setup](../README.md#setup), then run:

```sh
python -m manim -ql --renderer cairo electron_beams/BuschBeamCinematic.py BuschBeamCinematic
```

For a final-frame smoke check:

```sh
python -m manim -s -ql --renderer cairo electron_beams/BuschBeamCinematic.py BuschBeamCinematic
```

The class is `BuschBeamCinematic`. It uses standard landscape dimensions, unlike
the portrait convolution scenes. `FAST_MODE = False` is preserved from the saved
file; setting it to `True` reduces the ray count, curve sampling, and timings.
Use `-qh` for higher-resolution output. The 3D ray redraws can be slow.

## Model

The beam travels along x at constant speed `vx`, with initial transverse velocity
`vy0` and angular frequency `omega`. At nonzero field:

- `x(t) = x0 + vx*t`
- `y(t) = (vy0/omega)*sin(omega*t)`
- `z(t) = -(vy0/omega)*(1-cos(omega*t))`

The zero-field branch is a straight ray. At the screen time, integer complete
turns refocus the rays to the axis. This is an illustrative uniform-field
trajectory model supporting the Busch e/m experiment, not a calibrated extraction
of e/m from experimental measurements. The included numerical tests evaluate the
actual nested trajectory function without changing the preserved scene source.
