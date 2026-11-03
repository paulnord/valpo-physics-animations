"""Partial stellar eclipse of equal, uniformly bright stars."""
from manim import *
import math

config.pixel_width = 900
config.pixel_height = 1600
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 24
config.background_color = '#080a0f'
CYAN, PINK, GOLD = '#48c8ed', '#f17ba9', '#f3cd70'
CREAM, MUTED, GRID = '#f5f0df', '#9aa4b7', '#272e3b'
B = 1.0

def overlap_area(s):
    r = math.hypot(float(s), B)
    if r >= 2:
        return 0.0
    return 2 * math.acos(r / 2) - r * math.sqrt(4-r*r) / 2


def flux(s):
    return 1 - overlap_area(s) / (2 * math.pi)

class PartialStellarEclipse(Scene):
    def construct(self):
        def label(text, y, size=28, color=CREAM):
            obj = Text(text, font='DejaVu Sans', font_size=size, color=color)
            if obj.width > 8.1:
                obj.scale_to_fit_width(8.1)
            return obj.move_to([0,y,0])
        self.add(label('A partial eclipse',7.05,51),
                 label('Two equally bright, equally sized stars',6.42,27),
                 label('Uniform surface brightness • opaque foreground star',5.83,20,MUTED))
        self.add(label('Rear star',5.12,24,CYAN).shift(LEFT*2),
                 label('Front star',5.12,24,PINK).shift(RIGHT*1.9))
        origin=np.array([0.,2.83,0.])
        scale=.88
        s=ValueTracker(-2.4)
        def moving_center():
            return origin + scale*np.array([s.get_value(),B,0.])
        self.add(Line(origin+LEFT*3.7,origin+RIGHT*3.7,color=GRID),
                 DashedLine(origin+LEFT*3.7+UP*scale,origin+RIGHT*3.7+UP*scale,
                            color=PINK,stroke_opacity=.55,stroke_width=1.5,dash_length=.12))
        self.add(Text('center path',font_size=18,color=PINK).move_to(origin+np.array([2.8,1.16,0.])))
        bracket_x=-3.35
        self.add(Line(origin+RIGHT*bracket_x,origin+RIGHT*bracket_x+UP*scale,color=CREAM,stroke_width=2),
                 Line(origin+RIGHT*(bracket_x-.09),origin+RIGHT*(bracket_x+.09),color=CREAM,stroke_width=2),
                 Line(origin+RIGHT*(bracket_x-.09)+UP*scale,origin+RIGHT*(bracket_x+.09)+UP*scale,color=CREAM,stroke_width=2),
                 Text('b = 1',font_size=20,color=CREAM).move_to(origin+np.array([bracket_x-.1,scale/2,0])).shift(LEFT*.6))
        fixed=Circle(radius=scale,color=CYAN,stroke_width=3,fill_color=CYAN,fill_opacity=1).move_to(origin)
        moving=always_redraw(lambda: Circle(radius=scale,color=PINK,stroke_width=3,fill_color=PINK,fill_opacity=1).move_to(moving_center()))
        def intersection():
            if math.hypot(s.get_value(),B)>=2:
                return VMobject()
            return Intersection(Circle(radius=scale).move_to(origin),Circle(radius=scale).move_to(moving_center()),
                                color=GOLD,stroke_width=2,fill_opacity=.12)
        self.add(fixed,moving)
        # Gold outline shows the rear-star area hidden behind the front star.
        # Draw annotation last so the whole hidden lens remains outlined.
        self.add(always_redraw(lambda: Circle(radius=scale,color=CYAN,stroke_width=1.5,stroke_opacity=.35).move_to(origin)),
                 always_redraw(lambda: Circle(radius=scale,color=PINK,stroke_width=3).move_to(moving_center())),
                 always_redraw(lambda: DashedLine(origin,moving_center(),color=CREAM,stroke_width=1.2,dash_length=.08)),
                 Dot(origin,radius=.045,color=CYAN),
                 always_redraw(lambda: Dot(moving_center(),radius=.045,color=PINK)))
        self.add(always_redraw(intersection))
        shift_label=Text('t = (s, 1)     s =',font_size=25,color=CREAM)
        shift_num=DecimalNumber(-2.4,num_decimal_places=2,include_sign=True,mob_class=Text,font_size=26,color=CREAM)
        self.add(VGroup(shift_label,shift_num).arrange(RIGHT,buff=.18).move_to([0,1.28,0]))
        shift_num.add_updater(lambda m:m.set_value(s.get_value()))
        self.add(label('Gold outline = rear-star light blocked',.64,25,GOLD))
        value_label=Text('Visible brightness =',font_size=27,color=GOLD)
        value=DecimalNumber(1,num_decimal_places=4,font_size=31,color=GOLD,mob_class=Text)
        self.add(VGroup(value_label,value).arrange(RIGHT,buff=.2).move_to([0,-.02,0]))
        value.add_updater(lambda m:m.set_value(flux(s.get_value())))
        self.add(label('Normalized total light • baseline = both full stars',-.78,20,MUTED))
        axes=Axes(x_range=[-2.5,2.5,1],y_range=[.45,1.08,.1],x_length=6.5,y_length=2.8,
                  axis_config={'color':MUTED,'include_ticks':False},tips=False).move_to([.15,-3.10,0])
        self.add(axes)
        for tick in [-2,-1,0,1,2]:
            self.add(Text(str(tick),font_size=20,color=MUTED).next_to(axes.c2p(tick,.45),DOWN,buff=.13))
        self.add(Text('s',font_size=23,color=CREAM).next_to(axes.c2p(2.5,.45),RIGHT,buff=.12))
        for y,txt in [(.5,'0.5'),(.8,'0.8'),(1.,'1.0')]:
            self.add(Line(axes.c2p(-2.5,y),axes.c2p(2.5,y),color=GRID,stroke_width=1),
                     Text(txt,font_size=22,color=MUTED).next_to(axes.c2p(-2.5,y),LEFT,buff=.12))
        self.add(Text('both stars unobscured',font_size=17,color=MUTED).next_to(axes.c2p(1.8,1),UP,buff=.10).shift(LEFT*.6))
        self.add(axes.plot(flux,x_range=[-2.4,2.4,.02],color='#51462b',stroke_width=2))
        trace=always_redraw(lambda:axes.plot(flux,x_range=[-2.4,max(-2.399,s.get_value()),.02],color=GOLD,stroke_width=4))
        dot=always_redraw(lambda:Dot(axes.c2p(s.get_value(),flux(s.get_value())),radius=.065,color=GOLD))
        def guide():
            x=s.get_value();a=flux(x)
            if a>.999:return VMobject()
            return DashedLine(axes.c2p(x,1),axes.c2p(x,a),color=GOLD,stroke_width=1.5,dash_length=.09)
        self.add(trace,always_redraw(guide),dot)
        caption=VGroup(label('The front star hides part of the rear star.',-5.48,24,GOLD),label('Its own light still reaches us.',-5.96,23,GOLD))
        self.add(caption,label('F / Fout = (2π − A) / 2π = 1 − A / 2π',-6.85,22),
                 label('A = hidden overlap area;   center offset b = 1',-7.34,21,MUTED))
        def caption_to(a,b):
            self.play(Transform(caption,VGroup(label(a,-5.48,25,GOLD),label(b,-5.96,23,GOLD))),run_time=.4)
        self.wait(2.5)
        caption_to('More of the rear star is hidden.','The combined brightness dips.')
        self.play(s.animate.set_value(0),run_time=10,rate_func=linear)
        caption_to('At closest approach: brightness ≈ 0.8045.','About 19.6% of the combined light is blocked.')
        self.wait(4.5)
        caption_to('The rear star emerges again.','The brightness returns to its original level.')
        self.play(s.animate.set_value(2.4),run_time=10,rate_func=linear)
        caption_to('An eclipse inverts the overlap into a dip.','Full alignment would leave half the total light.')
        self.wait(4)
