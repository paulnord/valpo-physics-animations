"""Render: manim -qh circles.py CircleConvolution (Manim Community Edition)."""
from manim import *
import math

config.pixel_width = 900
config.pixel_height = 1600
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 24
config.background_color = '#080a0f'

CYAN = '#48c8ed'
PINK = '#f17ba9'
GOLD = '#f3cd70'
CREAM = '#f5f0df'
MUTED = '#9aa4b7'
GRID = '#272e3b'


def overlap_area(s):
    """Exact convolution of unit-disk indicator functions at displacement (s,0)."""
    r = abs(float(s))
    if r >= 2:
        return 0.0
    return 2 * math.acos(r / 2) - r * math.sqrt(4 - r * r) / 2


class CircleConvolution(Scene):
    def construct(self):
        def label(text, y, size=28, color=CREAM):
            obj = Text(text, font='DejaVu Sans', font_size=size, color=color)
            if obj.width > 8.1:
                obj.scale_to_fit_width(8.1)
            return obj.move_to([0, y, 0])

        self.add(label('Convolution', 7.05, 54),
                 label('of two filled circles', 6.42, 31),
                 label('Unit disks: 1 inside, 0 outside', 5.83, 22, MUTED))
        self.add(label('f(u)  fixed', 5.05, 25, CYAN).shift(LEFT * 2),
                 label('g(t − u)  slides', 5.05, 25, PINK).shift(RIGHT * 1.9))
        origin = np.array([0., 2.9, 0.])
        scale = 1.08
        s = ValueTracker(-2.4)
        self.add(Line(origin + LEFT * 4, origin + RIGHT * 4, color=GRID),
                 Line(origin + DOWN * 1.3, origin + UP * 1.3, color=GRID))
        fixed = Circle(radius=scale, color=CYAN, stroke_width=3,
                       fill_color=CYAN, fill_opacity=.18).move_to(origin)
        moving = always_redraw(lambda: Circle(radius=scale, color=PINK,
            stroke_width=3, fill_color=PINK, fill_opacity=.18)
            .move_to(origin + RIGHT * scale * s.get_value()))
        # Boolean geometry is rebuilt from actual Manim circles at each frame.
        def intersection():
            shift = s.get_value()
            if abs(shift) >= 2:
                return VMobject()
            if abs(shift) < 1e-6:
                return Circle(radius=scale, stroke_width=0,
                    fill_color=GOLD, fill_opacity=.65).move_to(origin)
            return Intersection(Circle(radius=scale).move_to(origin),
                Circle(radius=scale).move_to(origin + RIGHT * scale * shift),
                color=GOLD, stroke_width=0, fill_opacity=.65)
        overlap = always_redraw(intersection)
        self.add(fixed, moving, overlap)
        self.add(always_redraw(lambda: Circle(radius=scale, color=CYAN,
            stroke_width=3).move_to(origin)),
            always_redraw(lambda: Circle(radius=scale, color=PINK,
            stroke_width=3).move_to(origin + RIGHT * scale * s.get_value())))
        self.add(Dot(origin, radius=.035, color=CYAN),
            always_redraw(lambda: Dot(origin + RIGHT * scale * s.get_value(),
                                     radius=.035, color=PINK)))
        shift_label = Text('t = (s, 0)     s =', font_size=25, color=CREAM)
        shift_num = DecimalNumber(-2.4, num_decimal_places=2, include_sign=True, mob_class=Text,
                                  font_size=26, color=CREAM)
        shift_group = VGroup(shift_label, shift_num).arrange(RIGHT, buff=.18).move_to([0,1.08,0])
        shift_num.add_updater(lambda m: m.set_value(s.get_value()))
        self.add(shift_group, label('Convolution = overlapping area', .48, 27, GOLD))
        value_label = Text('(f ∗ g)(s, 0) =', font_size=29, color=GOLD)
        value = DecimalNumber(0, num_decimal_places=3, font_size=31, color=GOLD, mob_class=Text)
        values = VGroup(value_label, value).arrange(RIGHT, buff=.2).move_to([0,-.16,0])
        value.add_updater(lambda m: m.set_value(overlap_area(s.get_value())))
        self.add(values, label('2D convolution · horizontal cross-section', -.91, 21, MUTED))
        axes = Axes(x_range=[-2.5,2.5,1], y_range=[0,3.5,1],
                    x_length=6.5, y_length=2.8,
                    axis_config={'color':MUTED,'include_ticks':False},
                    tips=False).move_to([.15,-3.22,0])
        self.add(axes)
        for tick in [-2,-1,0,1,2]:
            self.add(Text(str(tick),font_size=20,color=MUTED).next_to(axes.c2p(tick,0),DOWN,buff=.13))
        self.add(Text('s',font_size=23,color=CREAM).next_to(axes.c2p(2.5,0),RIGHT,buff=.12))
        for y, txt in [(math.pi/2,'π/2'),(math.pi,'π')]:
            self.add(Line(axes.c2p(-2.5,y),axes.c2p(2.5,y),color=GRID,stroke_width=1),
                Text(txt,font_size=22,color=MUTED).next_to(axes.c2p(-2.5,y),LEFT,buff=.12))
        self.add(axes.plot(overlap_area,x_range=[-2.4,2.4,.025],color='#51462b',stroke_width=2))
        trace = always_redraw(lambda: axes.plot(overlap_area,
             x_range=[-2.4,max(-2.399,s.get_value()),.025],color=GOLD,stroke_width=4))
        dot = always_redraw(lambda: Dot(axes.c2p(s.get_value(),overlap_area(s.get_value())),radius=.065,color=GOLD))
        def guide():
            x=s.get_value(); a=overlap_area(x)
            if a<.01:return VMobject()
            return DashedLine(axes.c2p(x,0),axes.c2p(x,a),color=GOLD,stroke_width=1.5,dash_length=.09)
        self.add(trace,always_redraw(guide),dot)
        caption = VGroup(label('Slide one disk across the other.',-5.65,24,GOLD),
                         label('Measure their shared area at every shift.',-6.12,23,GOLD))
        self.add(caption,
                 label('A(r) = 2 arccos(r/2) − (r/2)√(4 − r²)',-7.03,22),
                 label('r = |t| ≤ 2;   A(r) = 0 for r > 2',-7.49,20,MUTED))
        def caption_to(a,b):
            target=VGroup(label(a,-5.65,24,GOLD),label(b,-6.12,23,GOLD))
            self.play(Transform(caption,target),run_time=.4)
        self.wait(3)
        caption_to('The gold overlap grows.','So does the convolution.')
        self.play(s.animate.set_value(0),run_time=12,rate_func=linear)
        caption_to('At perfect alignment, the disks coincide.','The maximum is their full area: π.')
        self.wait(3)
        caption_to('The overlap shrinks as the disk moves on.','At distance 2, it reaches zero.')
        self.play(s.animate.set_value(2.4),run_time=12,rate_func=linear)
        caption_to('Unlike rectangles, disks give a curved profile.','In 2D, the result is rotationally symmetric.')
        self.wait(4)
