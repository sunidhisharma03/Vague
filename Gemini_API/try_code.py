from manim import *

class ProjectileMotion(Scene):
    def construct(self):
        # --- Scene Setup ---
        # Constants
        g = 9.8  # Acceleration due to gravity (m/s^2)
        v0 = 20  # Initial velocity (m/s)
        theta_degrees = 45  # Launch angle (degrees)
        theta_radians = np.radians(theta_degrees)

        # Time range for trajectory calculation
        t_range = (0, 2 * v0 * np.sin(theta_radians) / g, 0.01) # Accurate time range


        # Trajectory function
        def trajectory(t):
            x = v0 * np.cos(theta_radians) * t
            y = v0 * np.sin(theta_radians) * t - 0.5 * g * t**2
            return np.array([x, y, 0])

        # Axes
        axes = Axes(
            x_range=[0, 40, 5],
            y_range=[0, 25, 5],
            x_axis_config={"numbers_to_include": np.arange(0, 41, 10)},
            y_axis_config={"numbers_to_include": np.arange(0, 26, 5)},
            tips=False,
        )
        axes.to_edge(DL)
        axes_labels = axes.get_axis_labels(x_label="Horizontal Distance (m)", y_label="Vertical Distance (m)")

        # --- Animation ---
        # Projectile Path
        path = ParametricFunction(trajectory, t_range=t_range, color=YELLOW)

        # Projectile
        projectile = Dot(point=path.points[0], color=RED)

        # Initial Velocity Vector
        v0_vector = Arrow(
            start=path.points[0],
            end=path.points[0] + np.array([v0 * np.cos(theta_radians), v0 * np.sin(theta_radians), 0]),
            buff=0,
            color=GREEN,
        )
        v0_text = MathTex(r"\vec{v}_0").next_to(v0_vector, UP)

        # Max Height
        t_max_height = v0 * np.sin(theta_radians) / g
        max_height_point = trajectory(t_max_height)
        max_height_dot = Dot(max_height_point, color=BLUE)
        max_height_text = MathTex("Maximum Height").next_to(max_height_dot, RIGHT)

        # Animation 
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(path))
        self.play(Create(projectile), GrowArrow(v0_vector), Write(v0_text))
        self.play(
            MoveAlongPath(projectile, path),
            Create(max_height_dot),
            Write(max_height_text),
            run_time=t_range[1],
            rate_func=linear
        )
        #Add more animations and elements as needed here.  This is a basic framework to get you started.



        # ---Cleanup (optional)---
        # self.wait(1)
        # self.remove(projectile,path,v0_vector, v0_text, max_height_dot, max_height_text,axes,axes_labels)