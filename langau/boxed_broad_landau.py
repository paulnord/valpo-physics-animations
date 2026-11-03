"""Two-panel broad Landau/narrow Gaussian midpoint-grid animation.

The displayed functions are peak-normalized f=L/Lmax and g=G/Gmax.
On a fixed grid u_i, f_D(u)=f(u_i) and g_{D,x}(u)=g(x-u_i)
inside cell i. Their product has exactly area D*sum(f(u_i)*g(x-u_i)).
The Gaussian is resampled as it slides: this is midpoint quadrature, not
an assertion that continuously translating a frozen histogram gives this sum.
Finite grid [-9,18]; output x in [-3,7]; Gaussian sigma=.18, ROOT xi=1.
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
SIGMA=.18
STEPS=[.06,.45,.9]
def L(u):
 z=np.asarray(u)-.22278298
 return landau.pdf((z-np.log(np.pi/2))/(np.pi/2))/(np.pi/2)
def f(u):return L(u)/L(0)
def g(v):return np.exp(-.5*(np.asarray(v)/SIGMA)**2)
def grid(step):return -9+(np.arange(round(27/step))+.5)*step
def midpoint(x,step):
 u=grid(step)
 return np.sum(f(u)*g(np.asarray(x)[...,None]-u),axis=-1)*step
def reference(x,n=160):
 z,w=roots_legendre(n);z*=8;w*=8
 return np.sum(f(np.asarray(x)[...,None]+SIGMA*z)*np.exp(-z*z/2)*w,axis=-1)*SIGMA

class BoxedBroadLandau(Scene):
 def construct(self):
  def txt(s,y,size=25,color=CREAM):
   m=Text(s,font='DejaVu Sans',font_size=size,color=color)
   if m.width>8.15:m.scale_to_fit_width(8.15)
   return m.move_to([0,y,0])
  def path(ax,xs,ys,color,width=3):
   origin=ax.c2p(0,0);dx=ax.c2p(1,0)-origin;dy=ax.c2p(0,1)-origin
   return VMobject(color=color,stroke_width=width).set_points_as_corners(origin+np.asarray(xs)[:,None]*dx+np.asarray(ys)[:,None]*dy)
  self.add(txt('Convolution with boxes',7.16,40),txt('Broad Landau ∗ narrow Gaussian',6.57,27),
   txt('Both inputs scaled to peak height 1',6.04,22,MUTED))
  x=ValueTracker(-3);stage=[0]
  top=Axes(x_range=[-4.5,8.5,2],y_range=[0,1.12,.5],x_length=7.6,y_length=3.1,
    axis_config={'color':MUTED,'include_ticks':False},tips=False).move_to([0,3.63,0])
  self.add(top,txt('Cyan: Landau    Pink: Gaussian    Gold: product',5.53,21))
  self.add(Text('1',font_size=18,color=MUTED).next_to(top.c2p(-4.5,1),LEFT,buff=.1))
  for v in [-4,-2,0,2,4,6,8]:self.add(Text(str(v),font_size=18,color=MUTED).next_to(top.c2p(v,0),DOWN,buff=.1))
  self.add(Text('u',font_size=22,color=CREAM).next_to(top.c2p(8.5,0),RIGHT,buff=.1))
  def rectangles(vals,color,opacity,stroke):
   d=STEPS[stage[0]];u=grid(d);group=VGroup()
   for z,h in zip(u,vals):
    if z+d/2<=-4.5 or z-d/2>=8.5 or h<1e-6:continue
    left=max(-4.5,z-d/2);right=min(8.5,z+d/2)
    group.add(Polygon(top.c2p(left,0),top.c2p(right,0),top.c2p(right,h),top.c2p(left,h),
      stroke_color=color,stroke_width=stroke,fill_color=color,fill_opacity=opacity))
   return group
  landau_boxes=rectangles(f(grid(STEPS[stage[0]])),CYAN,.14,.65)
  gauss_boxes=always_redraw(lambda:rectangles(g(x.get_value()-grid(STEPS[stage[0]])),PINK,.18,1.1))
  product_boxes=always_redraw(lambda:rectangles(f(grid(STEPS[stage[0]]))*g(x.get_value()-grid(STEPS[stage[0]])),GOLD,.48,1.5))
  self.add(landau_boxes,gauss_boxes,product_boxes)
  status=txt('1 / 3   Fine boxes: Δu = 0.06',1.42,27,GOLD)
  self.add(status,txt('Fixed midpoint grid; Gaussian resampled as it slides',.86,20,MUTED),
   txt('Each gold height = cyan height × pink height',.25,23,GOLD))
  out=Axes(x_range=[-3,7,2],y_range=[0,1.05,.5],x_length=7.6,y_length=3.15,
    axis_config={'color':MUTED,'include_ticks':False},tips=False).move_to([0,-2.56,0])
  self.add(out,txt('Sampled convolution versus the ideal curve',-.55,25,GOLD))
  for v in [-2,0,2,4,6]:self.add(Text(str(v),font_size=19,color=MUTED).next_to(out.c2p(v,0),DOWN,buff=.13))
  for v in [.5,1]:self.add(Text(str(v),font_size=18,color=MUTED).next_to(out.c2p(-3,v),LEFT,buff=.12))
  self.add(Text('x',font_size=22,color=CREAM).next_to(out.c2p(7,0),RIGHT,buff=.1))
  xs=np.linspace(-3,7,1601);ref=reference(xs)
  assert np.max(abs(ref-reference(xs,320)))<1e-10
  values=[midpoint(xs,d) for d in STEPS]
  self.add(path(out,xs,ref,CREAM,3.4))
  def trace():
   mask=xs<=x.get_value()
   if np.sum(mask)<2:return VMobject()
   return path(out,xs[mask],values[stage[0]][mask],GOLD,3.5)
  self.add(always_redraw(trace),always_redraw(lambda:Dot(out.c2p(x.get_value(),float(midpoint(x.get_value(),STEPS[stage[0]]))),radius=.055,color=GOLD)))
  self.add(txt('White: ideal convolution     Gold: sampled sum',-4.72,22),
   txt('CΔ(x) = Δu Σ f(uᵢ)g(x − uᵢ)',-5.35,28))
  caption=VGroup(txt('Many small boxes resolve the narrow Gaussian.',-6.12,24,GOLD),txt('The summed overlap changes smoothly.',-6.61,22,MUTED))
  self.add(caption,txt('Ideal = converged integral of the same two functions',-7.05,18,CREAM),txt('Landau scale ξ = 1    Gaussian σ = 0.18    Illustrative shapes',-7.53,17,MUTED))
  self.wait(2)
  self.play(x.animate.set_value(7),run_time=12,rate_func=linear)
  self.wait(1)
  for j,d,lines in [(1,.45,('Wider boxes start to miss the narrow peak.','The numerical result begins to ripple.')),
                   (2,.9,('Very wide boxes alternately hit and miss it.','These waves come from sampling, not the true convolution.'))]:
   stage[0]=j;x.set_value(-3)
   landau_boxes.become(rectangles(f(grid(STEPS[stage[0]])),CYAN,.14,.65))
   self.play(Transform(status,txt(f'{j+1} / 3   Wider boxes: Δu = {d:.2f}',1.42,27,GOLD)),
    Transform(caption,VGroup(txt(lines[0],-6.12,24,GOLD),txt(lines[1],-6.61,22,MUTED))),run_time=.5)
   self.wait(1)
   self.play(x.animate.set_value(7),run_time=12,rate_func=linear)
   self.wait(1.5)
  self.play(Transform(caption,VGroup(txt('Same functions, three grid spacings.',-6.12,24,GOLD),
    txt('To recover the smooth curve, resolve the narrowest feature.',-6.61,21,MUTED))),run_time=.4)
  self.wait(4)

if __name__=='__main__':
 xs=np.linspace(-3,7,1601);ref=reference(xs)
 for d in STEPS:print('step',d,'max error',np.max(abs(midpoint(xs,d)-ref)))
 print('reference check',np.max(abs(ref-reference(xs,320))))
