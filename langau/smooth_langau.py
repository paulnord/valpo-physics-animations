"""A broad Landau smeared slightly by a narrower Gaussian (genuine Manim).

Illustrative model, not detector fit data. ROOT/CERN Landau width xi=1,
MPV=0; Gaussian sigma=0.45. The Landau has no finite standard deviation:
xi is a scale parameter, never its standard deviation. Gaussian convolution
uses Gauss-Legendre quadrature on z in [-8,8], with convergence tests at
160 and 320 nodes. Gaussian omitted probability is about 1.3e-15.
"""
from manim import *
import numpy as np
from scipy.stats import landau
from scipy.special import roots_legendre

config.pixel_width=900
config.pixel_height=1600
config.frame_width=9
config.frame_height=16
config.frame_rate=24
config.background_color='#080a0f'
CYAN='#48c8ed'; PINK='#f17ba9'; GOLD='#f3cd70'; CREAM='#f5f0df'; MUTED='#9aa4b7'
XI=1.
SIGMA=.45

def L(u):
    z=np.asarray(u)/XI-.22278298
    return landau.pdf((z-np.log(np.pi/2))/(np.pi/2))/(XI*np.pi/2)

def G(v):
    return np.exp(-.5*(np.asarray(v)/SIGMA)**2)/(np.sqrt(2*np.pi)*SIGMA)

def convolution(x,n=160):
    z,w=roots_legendre(n);z=z*8;w=w*8
    return np.sum(L(np.asarray(x)[...,None]+SIGMA*z)*np.exp(-z*z/2)*w/np.sqrt(2*np.pi),axis=-1)

class SmoothLangau(Scene):
    def construct(self):
        def txt(s,y,size=24,color=CREAM):
            m=Text(s,font='DejaVu Sans',font_size=size,color=color)
            if m.width>8.12:m.scale_to_fit_width(8.12)
            return m.move_to([0,y,0])
        def path(ax,xs,ys,color,width=3):
            origin=ax.c2p(0,0);dx=ax.c2p(1,0)-origin;dy=ax.c2p(0,1)-origin
            p=VMobject(color=color,stroke_width=width)
            return p.set_points_as_corners(origin+np.asarray(xs)[:,None]*dx+np.asarray(ys)[:,None]*dy)
        def axes(y, ymax,height,xlo=-3,xhi=7):
            a=Axes(x_range=[xlo,xhi,2],y_range=[0,ymax,ymax/2],x_length=7.3,y_length=height,
                axis_config={'color':MUTED,'include_ticks':False},tips=False).move_to([0,y,0])
            self.add(a)
            return a
        self.add(txt('A little blur, not a new shape',7.2,35),
            txt('Landau ∗ narrow Gaussian',6.6,29),
            txt('Intrinsic energy loss + measurement resolution',6.08,21,MUTED))
        x=ValueTracker(-3)
        us=np.linspace(-6,10,1501)
        xs=np.linspace(-3,7,1201)
        result=convolution(xs)
        assert np.max(np.abs(result-convolution(xs,320)))<1e-10
        top=axes(4.36,1.1,1.75,-6,10)
        self.add(txt('Inputs, each scaled to its own peak height',5.5,20,MUTED))
        self.add(path(top,us,L(us)/L(0),CYAN))
        self.add(always_redraw(lambda:path(top,us,G(x.get_value()-us)/G(0),PINK)))
        self.add(txt('Landau: broad, fixed       Gaussian: narrow, sliding',3.18,20),
            txt('Landau scale ξ = 1      Gaussian σ = 0.45',2.72,21,MUTED))
        prod=axes(1.05,.18,1.75,-6,10)
        self.add(txt('Multiply, then integrate the product',2.22,25,GOLD))
        def product_shape():
            yy=L(us)*G(x.get_value()-us)
            line=path(prod,us,yy,GOLD)
            pts=[prod.c2p(us[0],0)]+list(line.get_anchors())+[prod.c2p(us[-1],0)]
            fill=Polygon(*pts,stroke_width=0,fill_color=GOLD,fill_opacity=.25)
            return VGroup(fill,line)
        self.add(always_redraw(product_shape))
        self.add(txt('L(u)G(x − u)       gold area = convolution at x',-.13,21,GOLD))
        self.add(txt('The narrow Gaussian averages nearby Landau values.',-.71,21,MUTED))
        out=axes(-3.01,.205,2.45)
        self.add(txt('Result: the smooth Landau–Gaussian (Langau)',-1.25,24,GOLD))
        for v in [-2,0,2,4,6]:self.add(Text(str(v),font_size=18,color=MUTED).next_to(out.c2p(v,0),DOWN,buff=.12))
        self.add(Text('x',font_size=21,color=CREAM).next_to(out.c2p(7,0),RIGHT,buff=.1))
        for v in [.1,.2]:self.add(Text(f'{v:.1f}',font_size=17,color=MUTED).next_to(out.c2p(-3,v),LEFT,buff=.1))
        original=DashedVMobject(path(out,xs,L(xs),CYAN,2),num_dashes=75,dashed_ratio=.55)
        self.add(original)
        def trace():
            idx=xs<=x.get_value()
            if np.sum(idx)<2:return VMobject()
            return path(out,xs[idx],result[idx],GOLD,4)
        self.add(always_redraw(trace),always_redraw(lambda:Dot(out.c2p(x.get_value(),float(convolution(x.get_value()))),radius=.055,color=GOLD)))
        self.add(txt('Cyan dashed: Landau      Gold: after smearing',-4.92,21),
            txt('C(x) = ∫ L(u)G(x − u) du',-5.47,28))
        caption=VGroup(txt('The Landau sets the dominant shape.',-6.03,25,GOLD),txt('A narrower Gaussian adds only modest broadening.',-6.51,22,MUTED))
        self.add(caption,txt('Illustrative parameters • normalized PDFs • converged integral',-7.4,18,MUTED))
        self.wait(3)
        self.play(x.animate.set_value(0),run_time=6,rate_func=linear)
        self.play(Transform(caption,VGroup(txt('The sharp peak softens a little.',-6.03,25,GOLD),txt('Nearby values are averaged, while the long tail remains.',-6.51,22,MUTED))),run_time=.4)
        self.wait(2)
        self.play(x.animate.set_value(7),run_time=14,rate_func=linear)
        self.play(Transform(caption,VGroup(txt('Landau before smearing. Langau after.',-6.03,25,GOLD),txt('A narrow response preserves the dominant energy-loss shape.',-6.51,21,MUTED))),run_time=.4)
        self.wait(5)

if __name__=='__main__':
    xs=np.linspace(-3,7,1201)
    ref=convolution(xs)
    print('Max 160→320 node convergence difference:',np.max(np.abs(ref-convolution(xs,320))))
    print('Original peak:',float(L(0)),'Smeared peak:',float(ref.max()))
