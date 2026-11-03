from manim import *
import numpy as np


class BuschBeamCinematic(ThreeDScene):
    def construct(self):
        # ============================================================
        # MASTER SWITCH
        # ============================================================
        FAST_MODE = False

        # ============================================================
        # CAMERA PRESETS: tweak these numbers to change perspectives
        # Format is (phi, theta) in DEGREES
        # ============================================================
        VIEW_OBLIQUE = (70, 30)
        VIEW_SCREEN  = (89, 0)
        VIEW_SIDE    = (65, 85)
        VIEW_HIGH    = (80, 40)

        # ============================================================
        # FAST / FINAL RENDER SETTINGS
        # ============================================================
        if FAST_MODE:
            vy_vals = np.linspace(-0.20, 0.20, 7)
            curve_step = 0.10
            ray_stroke_width = 2
            ray_opacity = 0.75
            mean_stroke_width = 4
            dot_radius = 0.022
            line_thickness = 0.040
            pause_short = 0.2
            pause_med = 0.4
            rt_camera = 1.2
            rt_short = 0.8
            rt_med = 2.0
            rt_long = 2.8
        else:
            vy_vals = np.linspace(-0.20, 0.20, 15)
            curve_step = 0.04
            ray_stroke_width = 2
            ray_opacity = 0.75
            mean_stroke_width = 4
            dot_radius = 0.025
            line_thickness = 0.040
            pause_short = 0.4
            pause_med = 0.8
            rt_camera = 2.0
            rt_short = 1.0
            rt_med = 3.0
            rt_long = 5.0

        # ============================================================
        # PHYSICS / GEOMETRY SETTINGS
        # ============================================================
        x0 = -6.0
        x_screen = 6.0
        L = x_screen - x0
        vx = 1.0
        t_screen = L / vx

        OMEGA_0 = 0.0
        OMEGA_HALF = np.pi / t_screen
        OMEGA_1 = 2 * np.pi / t_screen
        OMEGA_3HALF = 3 * np.pi / t_screen
        OMEGA_2 = 4 * np.pi / t_screen

        screen_size = 5.0
        field_ring_radius = 2.0
        field_ring_count = 10

        omega_tracker = ValueTracker(0.0)

        # ============================================================
        # HELPER FUNCTIONS
        # ============================================================
        def pos(t, vy0, omega):
            if abs(omega) < 1e-8:
                return np.array([x0 + vx * t, vy0 * t, 0.0])

            x = x0 + vx * t
            y = (vy0 / omega) * np.sin(omega * t)
            z = -(vy0 / omega) * (1 - np.cos(omega * t))
            return np.array([x, y, z])

        def screen_point(vy0, omega):
            return pos(t_screen, vy0, omega)

        def make_screen():
            scr = Rectangle(width=screen_size, height=screen_size, color=WHITE)
            scr.rotate(PI / 2, axis=UP)
            scr.move_to([x_screen, 0, 0])
            scr.set_fill(GREY, opacity=0.12)
            return scr

        def make_field_rings():
            rings = VGroup()
            for x in np.linspace(x0 + 0.7, x_screen - 0.7, field_ring_count):
                ring = Circle(radius=field_ring_radius, color=TEAL)
                ring.rotate(PI / 2, axis=UP)
                ring.move_to([x, 0, 0])
                ring.set_stroke(width=2, opacity=0.30)
                rings.add(ring)
            return rings

        # ============================================================
        # STATIC GEOMETRY
        # ============================================================
        axis = Line3D(
            start=[x0, 0, 0],
            end=[x_screen, 0, 0],
            thickness=0.01,
            color=GREY_B,
        )
        axis.set_stroke(opacity=0.1)

        gun = Cylinder(radius=0.12, height=0.45, direction=RIGHT, color=GREY_B)
        gun.move_to([x0 - 0.25, 0, 0])

        screen = make_screen()
        field_rings = make_field_rings()

        # ============================================================
        # DYNAMIC OBJECTS
        # ============================================================
        mean_path = always_redraw(
            lambda: ParametricFunction(
                lambda t: pos(t, 0.0, omega_tracker.get_value()),
                t_range=[0, t_screen, curve_step],
                color=YELLOW,
                stroke_width=mean_stroke_width,
                use_smoothing=not FAST_MODE,
            )
        )

        ray_bundle = always_redraw(
            lambda: VGroup(*[
                ParametricFunction(
                    lambda t, vy0=vy: pos(t, vy0, omega_tracker.get_value()),
                    t_range=[0, t_screen, curve_step],
                    color=BLUE if vy > 0 else RED if vy < 0 else YELLOW,
                    stroke_opacity=ray_opacity,
                    stroke_width=ray_stroke_width,
                    use_smoothing=not FAST_MODE,
                )
                for vy in vy_vals
            ])
        )

        screen_dots = always_redraw(
            lambda: VGroup(*[
                Dot3D(
                    point=screen_point(vy, omega_tracker.get_value()),
                    radius=dot_radius,
                    color=BLUE if vy > 0 else RED if vy < 0 else YELLOW,
                )
                for vy in vy_vals
            ])
        )

        def make_screen_line_or_dot():
            omega = omega_tracker.get_value()
            p_lo = screen_point(vy_vals[0], omega)
            p_hi = screen_point(vy_vals[-1], omega)
            spread = np.linalg.norm(p_hi - p_lo)

            if spread < 0.06:
                return Dot3D(point=screen_point(0.0, omega), radius=0.06, color=WHITE)
            else:
                return Line3D(
                    start=p_lo,
                    end=p_hi,
                    thickness=line_thickness,
                    color=WHITE,
                )

        screen_line = always_redraw(make_screen_line_or_dot)

        # ============================================================
        # LABELS
        # ============================================================
#         mode_text = "FAST MODE" if FAST_MODE else "FINAL MODE"
# 
#         title = Text("Busch method beam evolution", font_size=32).to_corner(UL)
#         subtitle = Text(
#             f"screen line rotates and refocuses as B increases   [{mode_text}]",
#             font_size=22
#         ).next_to(title, DOWN, aligned_edge=LEFT)
# 
#         turns_label = always_redraw(
#             lambda: Text(
#                 f"turns to screen = {omega_tracker.get_value() * t_screen / (2*np.pi):.2f}",
#                 font_size=24
#             ).to_corner(UR)
#         )
# 
#         caption = Text("", font_size=26).to_edge(DOWN)

        #self.add_fixed_in_frame_mobjects(title, subtitle, turns_label, caption)

        # ============================================================
        # INITIAL CAMERA
        # ============================================================
        self.set_camera_orientation(
            phi=VIEW_OBLIQUE[0] * DEGREES,
            theta=VIEW_OBLIQUE[1] * DEGREES,
        )

        # ============================================================
        # BUILD SCENE
        # ============================================================
        print("Building First Scene", flush=True)
#         self.play(FadeIn(title), FadeIn(subtitle), run_time=rt_short)
        self.play(Create(axis), FadeIn(gun), FadeIn(screen), run_time=rt_short)
        self.play(FadeIn(field_rings), run_time=rt_short)
        #self.add(mean_path, ray_bundle, screen_dots, screen_line)

        # ------------------------------------------------------------
        # ACT 1: Field off
        # ------------------------------------------------------------
        print("Starting Act 1", flush=True)
#         caption.become(Text("Field off: straight line on the screen", font_size=26).to_edge(DOWN))
#         self.play(FadeIn(caption), run_time=rt_short)
#         self.play(omega_tracker.animate.set_value(OMEGA_0), run_time=rt_short)
#         self.wait(pause_med)
# 
#         # ------------------------------------------------------------
#         # ACT 1.5: Single beam sweeps back and forth with field off
#         # ------------------------------------------------------------
#         print("Starting Act 1.5", flush=True)
#         caption.become(Text(
#             "With the magnetic field off, the beam can sweep back and forth",
#             font_size=26
#         ).to_edge(DOWN))
        self.wait(pause_short)

        # A single moving beam with a controllable launch angle
        sweep_vy = ValueTracker(0.0)

        sweeping_beam = always_redraw(
            lambda: ParametricFunction(
                lambda t: pos(t, sweep_vy.get_value(), 0.0),
                t_range=[0, t_screen, curve_step],
                color=YELLOW,
                stroke_width=mean_stroke_width,
                use_smoothing=not FAST_MODE,
            )
        )

        sweeping_dot = always_redraw(
            lambda: Dot3D(
                point=pos(t_screen, sweep_vy.get_value(), 0.0),
                radius=dot_radius * 1.4,
                color=YELLOW,
            )
        )

        # Temporarily hide the many-ray picture and show only one swept beam
        self.remove(mean_path, ray_bundle, screen_dots, screen_line)
        self.add(sweeping_beam, sweeping_dot)

        # Sweep upward
        self.play(
            sweep_vy.animate.set_value(vy_vals[-1]),
            run_time=rt_med,
            rate_func=smooth
        )

        # Sweep downward
        self.play(
            sweep_vy.animate.set_value(vy_vals[0]),
            run_time=rt_long,
            rate_func=smooth
        )

        # Return to center
        self.play(
            sweep_vy.animate.set_value(0.0),
            run_time=rt_med,
            rate_func=smooth
        )
        self.wait(pause_short)

        # ------------------------------------------------------------
        # ACT 1.6: Freeze into a few discrete positions
        # ------------------------------------------------------------
        print("Starting Act 1.6", flush=True)
#         caption.become(Text(
#             "Now imagine several beam positions at once",
#             font_size=26
#         ).to_edge(DOWN))

        discrete_vys = np.linspace(vy_vals[0], vy_vals[-1], 5)

        discrete_beams = VGroup(*[
            ParametricFunction(
                lambda t, vy0=vy: pos(t, vy0, 0.0),
                t_range=[0, t_screen, curve_step],
                color=BLUE if vy > 0 else RED if vy < 0 else YELLOW,
                stroke_width=ray_stroke_width + 1,
                stroke_opacity=0.75,
                use_smoothing=not FAST_MODE,
            )
            for vy in discrete_vys
        ])

        discrete_dots = VGroup(*[
            Dot3D(
                point=pos(t_screen, vy, 0.0),
                radius=dot_radius * 1.2,
                color=BLUE if vy > 0 else RED if vy < 0 else YELLOW,
            )
            for vy in discrete_vys
        ])

        discrete_line = Line3D(
            start=pos(t_screen, discrete_vys[0], 0.0),
            end=pos(t_screen, discrete_vys[-1], 0.0),
            thickness=line_thickness,
            color=WHITE,
        )

        self.play(
            FadeIn(discrete_beams),
            FadeIn(discrete_dots),
            Create(discrete_line),
            FadeOut(sweeping_beam),
            FadeOut(sweeping_dot),
            run_time=rt_med
        )
        self.wait(pause_med)

        # ------------------------------------------------------------
        # ACT 1.7: Replace discrete positions with the full continuous line
        # ------------------------------------------------------------
        print("Starting Act 1.7", flush=True)
#         caption.become(Text(
#             "Taken all together, these positions form the full line",
#             font_size=26
#         ).to_edge(DOWN))

        self.play(
            FadeOut(discrete_beams),
            FadeOut(discrete_dots),
            FadeOut(discrete_line),
            FadeIn(mean_path),
            FadeIn(ray_bundle),
            FadeIn(screen_dots),
            FadeIn(screen_line),
            run_time=rt_med
        )
        self.wait(pause_med)

        # ------------------------------------------------------------
        # ACT 2: Ramp up to halfway to first focus
        # ------------------------------------------------------------
        print("Starting Act 2", flush=True)
#         caption.become(Text("Increase B: the screen image rotates and shrinks", font_size=26).to_edge(DOWN))
#         self.play(
#             omega_tracker.animate.set_value(OMEGA_HALF),
#             run_time=rt_long,
#             rate_func=linear
#         )
#         self.wait(pause_short)
# 
#         # ------------------------------------------------------------
#         # CAMERA MOVE: look more directly at the screen
#         # ------------------------------------------------------------
#         self.move_camera(
#             phi=VIEW_SCREEN[0] * DEGREES,
#             theta=VIEW_SCREEN[1] * DEGREES,
#             run_time=rt_camera
#         )
#         self.wait(pause_short)
# 
#         # ------------------------------------------------------------
#         # ACT 3: First focus
#         # ------------------------------------------------------------
#         print("Starting Act 3", flush=True)
#         caption.become(Text("First focus: one full turn to the screen", font_size=26).to_edge(DOWN))
        self.play(
            omega_tracker.animate.set_value(OMEGA_1),
            run_time=rt_med,
            rate_func=linear
        )
        self.wait(pause_med)

        # ------------------------------------------------------------
        # ACT 4: Back field down
        # ------------------------------------------------------------
        print("Starting Act 4", flush=True)
#         caption.become(Text("Reduce B: the spot opens back into a line", font_size=26).to_edge(DOWN))
#         self.play(
#             omega_tracker.animate.set_value(OMEGA_0),
#             run_time=rt_long,
#             rate_func=linear
#         )
#         self.wait(pause_med)
# 
#         # ------------------------------------------------------------
#         # CAMERA MOVE: side view to emphasize hidden trajectories
#         # ------------------------------------------------------------
#         self.move_camera(
#             phi=VIEW_SIDE[0] * DEGREES,
#             theta=VIEW_SIDE[1] * DEGREES,
#             run_time=rt_camera
#         )
#         self.wait(pause_short)
# 
#         # ------------------------------------------------------------
#         # ACT 5: Ramp again, beyond first focus
#         # ------------------------------------------------------------
#         print("Starting Act 5", flush=True)
#         caption.become(Text("Increase B further: the line rotates again", font_size=26).to_edge(DOWN))
        self.play(
            omega_tracker.animate.set_value(OMEGA_3HALF),
            run_time=rt_long,
            rate_func=linear
        )
        self.wait(pause_short)

        # ------------------------------------------------------------
        # CAMERA MOVE: another oblique view
        # ------------------------------------------------------------
        self.move_camera(
            phi=VIEW_HIGH[0] * DEGREES,
            theta=VIEW_HIGH[1] * DEGREES,
            run_time=rt_camera
        )
        self.wait(pause_short)

        # ------------------------------------------------------------
        # ACT 6: Second focus
        # ------------------------------------------------------------
        print("Starting Act 6", flush=True)
#         caption.become(Text("Second focus: two full turns to the screen", font_size=26).to_edge(DOWN))
#         self.play(
#             omega_tracker.animate.set_value(OMEGA_2),
#             run_time=rt_med,
#             rate_func=linear
#         )
#         self.wait(pause_med)
# 
#         # ------------------------------------------------------------
#         # ACT 7: Return to a broad view and cycle back a little
#         # ------------------------------------------------------------
#         print("Starting Act 7", flush=True)
#         self.move_camera(
#             phi=VIEW_OBLIQUE[0] * DEGREES,
#             theta=VIEW_OBLIQUE[1] * DEGREES,
#             run_time=rt_camera
#         )
#         caption.become(Text("Field lowered again for comparison", font_size=26).to_edge(DOWN))
        self.play(
            omega_tracker.animate.set_value(OMEGA_HALF),
            run_time=rt_med,
            rate_func=linear
        )
        self.wait(pause_med)

#         caption.become(Text("Field lowered to zero", font_size=26).to_edge(DOWN))
#         self.play(
#             omega_tracker.animate.set_value(OMEGA_0),
#             run_time=rt_med,
#             rate_func=linear
#         )
#         self.wait(pause_med)
# 
#         self.play(FadeOut(caption), run_time=rt_short)
#         self.wait(pause_short)
#         print("Finished Rendering", flush=True)