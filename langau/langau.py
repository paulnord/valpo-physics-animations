"""Real sampled Langau quadrature; no decorative/artificial ripples.

Render with: manim langau.py LangauUndersampling
Legacy grid: NewStructure/TileSpectra.cc langaufun, 100 midpoints, x +/- 5 sigma.
Illustrative parameters only: ROOT Landau width=.012, MPV=0, Gaussian sigma=1.
SciPy's Landau is transformed to ROOT's standard parameterization. This was
checked against ROOT's CERNLIB G110 implementation at representative points
(-3,-1,-.22278298,0,1,5,20), relative differences below 3e-9.
"""
from manim import *
import numpy as np
from scipy.stats import landau

config.pixel_width=900
config.pixel_height=1600
config.frame_width=9
config.frame_height=16
config.frame_rate=24
config.background_color='#080a0f'
CYAN='#48c8ed'; PINK='#f17ba9'; GOLD='#f3cd70'; CREAM='#f5f0df'; MUTED='#9aa4b7'; GRID='#272e3b'; GREEN='#75dfb2'
XI=.012
SIGMA=1.
def L(u):
    z=np.asarray(u)/XI-.22278298
    return landau.pdf((z-np.log(np.pi/2))/(np.pi/2))/(XI*np.pi/2)
def G(v):return np.exp(-.5*(np.asarray(v)/SIGMA)**2)/(np.sqrt(2*np.pi)*SIGMA)
def quadrature(x,n):
    x=np.asarray(x)
    u=x[...,None]-5*SIGMA+(np.arange(n)+.5)*10*SIGMA/n
    return np.sum(L(u)*G(x[...,None]-u),axis=-1)*10*SIGMA/n

class LangauUndersampling(Scene):
    def construct(self):
        def txt(s,y,size=25,color=CREAM):
            m=Text(s,font='DejaVu Sans',font_size=size,color=color)
            if m.width>8.15:m.scale_to_fit_width(8.15)
            return m.move_to([0,y,0])
        self.add(txt('When convolution gets wavy',7.2,36),
                 txt('Landau ∗ Gaussian',6.61,30),
                 txt('The model is smooth. A coarse integral can wobble.',6.12,21,MUTED))
        x=ValueTracker(-1.5)
        n=[100]
        caption=VGroup(txt('A narrow Landau needs a fine integration grid.',-6.3,23,GOLD),
                       txt('The grid below moves with x, just as in legacy langaufun.',-6.75,19,MUTED))
        self.add(caption)
        inputs=Axes(x_range=[-2.5,2.5,1],y_range=[0,1.1,.5],x_length=7.5,y_length=1.65,
                    axis_config={'color':MUTED,'include_ticks':False},tips=False).move_to([0,4.45,0])
        self.add(inputs,txt('Inputs, each scaled to its own peak height',5.53,20,MUTED))
        us=np.unique(np.r_[np.linspace(-2.5,2.5,350),np.linspace(-.09,.35,350)])
        def path(ax,xs,ys,color,width=3):
            p=VMobject(color=color,stroke_width=width)
            origin=ax.c2p(0,0)
            dx=ax.c2p(1,0)-origin; dy=ax.c2p(0,1)-origin
            p.set_points_as_corners(origin + np.asarray(xs)[:,None]*dx + np.asarray(ys)[:,None]*dy)
            return p
        self.add(path(inputs,us,L(us)/L(0),CYAN,3))
        gaussian=always_redraw(lambda:path(inputs,us,G(x.get_value()-us)/G(0),PINK,3))
        self.add(gaussian,txt('L(u): narrow, fixed        G(x − u): broad, moving',3.29,20))
        self.add(txt('Zoom: the product L(u)G(x − u)',2.72,25,GOLD))
        product=Axes(x_range=[-.1,.35,.1],y_range=[0,6.5,2],x_length=7.5,y_length=2.05,
                     axis_config={'color':MUTED,'include_ticks':False},tips=False).move_to([0,1.18,0])
        self.add(product)
        for a in [0,.1,.2,.3]:
            self.add(Text(f'{a:.1f}',font_size=16,color=MUTED).next_to(product.c2p(a,0),DOWN,buff=.1))
        self.add(Text('u',font_size=20,color=CREAM).next_to(product.c2p(.35,0),RIGHT,buff=.1))
        zz=np.linspace(-.1,.35,400)
        curve=always_redraw(lambda:path(product,zz,L(zz)*G(x.get_value()-zz),GOLD,3))
        self.add(curve)
        def samples():
            shift=x.get_value();step=10/n[0]
            u=shift-5+(np.arange(n[0])+.5)*step
            u=u[(u>=-.1)&(u<=.35)]
            group=VGroup()
            for z in u:
                h=float(L(z)*G(shift-z))
                group.add(Line(product.c2p(z,0),product.c2p(z,h),color=PINK if n[0]==100 else GREEN,stroke_width=1.2),
                          Dot(product.c2p(z,h),radius=.047 if n[0]==100 else .021,color=PINK if n[0]==100 else GREEN))
            return group
        self.add(always_redraw(samples))
        status=txt('100 midpoints across x ± 5σ   •   Δu = 0.1σ',-.35,23,PINK)
        self.add(status,txt('Illustration: Landau width ξ = 0.012σ  (not fitted data)',-.83,19,MUTED))
        outputs=Axes(x_range=[-1.6,1.6,1],y_range=[0,.85,.2],x_length=7.5,y_length=2.4,
                     axis_config={'color':MUTED,'include_ticks':False},tips=False).move_to([0,-3.18,0])
        self.add(outputs,txt('Area of the product → convolution at x',-1.45,24,GOLD))
        for a in [-1,0,1]:self.add(Text(str(a),font_size=18,color=MUTED).next_to(outputs.c2p(a,0),DOWN,buff=.1))
        self.add(Text('x',font_size=20,color=CREAM).next_to(outputs.c2p(1.6,0),RIGHT,buff=.1))
        for a in [.4,.8]:self.add(Text(f'{a:.1f}',font_size=16,color=MUTED).next_to(outputs.c2p(-1.6,a),LEFT,buff=.1))
        xs=np.linspace(-1.5,1.5,1801)
        coarse=quadrature(xs,100);fine=quadrature(xs,4000); refined=quadrature(xs,1000)
        # A denser independent midpoint evaluation validates the reference.
        assert np.max(np.abs(fine[::20]-quadrature(xs[::20],8000)))<1e-7
        self.add(path(outputs,xs,fine,GOLD,3))
        def trace():
            mask=xs<=x.get_value()
            if np.count_nonzero(mask)<2:return VMobject()
            return path(outputs,xs[mask],(coarse if n[0]==100 else refined)[mask],PINK if n[0]==100 else GREEN,3)
        tracing=always_redraw(trace)
        dot=always_redraw(lambda:Dot(outputs.c2p(x.get_value(),float(quadrature(x.get_value(),n[0]))),radius=.055,color=PINK if n[0]==100 else GREEN))
        self.add(tracing,dot)
        legend=txt('Gold: fine reference     Pink: 100-point sum',-4.95,22)
        self.add(legend)
        formula=txt('C(x) ≈ Δu Σ L(uᵢ) G(x − uᵢ)',-5.55,26)
        self.add(formula,txt('Same functions. Same ±5σ bounds. Only sampling changes.',-7.43,18,MUTED))
        def explain(a,b):
            self.play(Transform(caption,VGroup(txt(a,-6.3,23,GOLD),txt(b,-6.75,20,MUTED))),run_time=.4)
        self.wait(4)
        explain('Some shifts hit the narrow peak. Others miss it.', 'Watch the pink sample heights and the output rise and fall.')
        self.play(x.animate.set_value(1.5),run_time=18,rate_func=linear)
        explain('Those ripples are integration error, not extra peaks.', 'The sample grid repeats its alignment every Δx = Δu.')
        self.wait(3)
        oldtrace=path(outputs,xs,coarse,PINK,1.5).set_opacity(.27)
        self.add(oldtrace)
        n[0]=1000;x.set_value(-1.5)
        self.play(Transform(status,txt('1,000 midpoints   •   Δu = 0.01σ',-.35,23,GREEN)),
                  Transform(legend,txt('Gold: fine reference     Green: 1,000-point sum',-4.95,22)),run_time=.6)
        explain('Resolve the narrow peak with a finer grid.', 'The same sum now follows the smooth reference.')
        self.play(x.animate.set_value(1.5),run_time=12,rate_func=linear)
        explain('Fix the integral: refine or use adaptive quadrature.', 'More points drawn on the screen do not fix this error.')
        self.wait(5)

if __name__=='__main__':
    xs=np.linspace(-1.5,1.5,301)
    fine=quadrature(xs,4000)
    print('max reference change 4000 -> 8000:',np.max(np.abs(fine-quadrature(xs,8000))))
    print('max coarse error:',np.max(np.abs(quadrature(xs,100)-fine)))
    print('max refined error:',np.max(np.abs(quadrature(xs,1000)-fine)))
