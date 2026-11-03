# Convolution of disks

- [Centered crossing](circles.py): convolution of two unit-disk indicator functions.
- [Offset crossing](offset_circles.py): the moving center follows `(s, 1)`.
- [Stellar eclipse application](../stars/README.md).

For center distance `r < 2`, the overlap area is
`A(r) = 2 acos(r/2) - r sqrt(4-r²)/2`; otherwise it is zero.
The centered case has `r = |s|`, and the offset case has `r = sqrt(s²+1)`.

See the [root README](../README.md#render) for render commands.
