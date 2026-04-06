from manim import *
import numpy as np

# Phase 1: Definition der Grundpunkte P und D
class Phase1(Scene):
    def construct(self):
        #Raster erzeugen
        gitter = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-6, 6, 1],
            background_line_style={
                "stroke_color": PURPLE,
                "stroke_opacity": 0.2,
                "stroke_width": 1
            }
        )

        #Rechteck
        ur_quadrat = Rectangle(
            width=1, height=1,
            color=YELLOW,
            stroke_opacity=0.3,
            stroke_width=2
        ).move_to([1.5, 1.5, 0]) #Zentrum des Quadrats

        self.add(gitter, ur_quadrat)

        # Koordinaten definieren
        self.punkt_p = np.array([0, 3, 0])
        self.punkt_d = np.array([4, 3, 0])

        # Main-Dots erstellen
        self.dot_p = Dot(self.punkt_p, color=RED)
        self.dot_d = Dot(self.punkt_d, color=BLUE)

        # Beschriftung
        self.label_p = MathTex("P").next_to(self.dot_p, UP)
        self.label_d = MathTex("D").next_to(self.dot_d, UP)

        self.add(self.dot_p, self.dot_d, self.label_p, self.label_d)

# Phase 2: Hinzufügen der Tiefenlinien (Orthogonalen)
class Phase2(Phase1):
    def construct(self):
        super().construct() # Lädt Phase 1
        
        tiefenlinien = VGroup()
        for i in range(-5, 6):
            start_punkt = [i, -4, 0]
            linie = Line(start_punkt, self.punkt_p, stroke_width=2, color=GRAY)
            tiefenlinien.add(linie)
            
        self.add(tiefenlinien)

# Phase 3: Konstruktion der Diagonale und Querlinien
class Phase3(Phase2):
    def construct(self):
        super().construct() # Lädt Phase 2
        
        # Diagonale zum Distanzpunkt D
        self.dot_l = Dot([-5, -4, 0], color=GREEN)
        self.diagonale = Line(self.dot_l, self.punkt_d, color=GREEN)

        querlinien = VGroup()
        for i in range(-5, 6):
            # Die perspektivische Höhe berechnen
            y_pos = (3*i - 1) / (i + 9)
            
            # Die Breite an dieser Höhe berechnen (Strahlensatz) 
            x_r = (15 - 5*y_pos) / 7
            x_l = -x_r
            
            linie = Line([x_l, y_pos, 0], [x_r, y_pos, 0], color=WHITE, stroke_width=2)
            querlinien.add(linie)

        self.add(self.dot_l, self.diagonale, querlinien)

# Phase 4: Das finale anamorphotische Quadrat
class Phase4(Phase3):
    def construct(self):
        super().construct() # Lädt Phase 3
        
        def transform_point(x, y):
            y_n = (3*y - 1) / (y + 9)
            x_n = x * (3 - y_n) / 7
            return np.array([x_n, y_n, 0])

        # Sampling des Quadrats (dein bewährter Ansatz)
        p_unten = [transform_point(x, 1) for x in np.linspace(1, 2, 100)]
        p_rechts = [transform_point(2, y) for y in np.linspace(1, 2, 100)]
        p_oben = [transform_point(x, 2) for x in np.linspace(2, 1, 100)]
        p_links = [transform_point(1, y) for y in np.linspace(2, 1, 100)]

        alle_p = p_unten + p_rechts + p_oben + p_links
        verzerrtes_quadrat = VMobject()
        verzerrtes_quadrat.set_points_as_corners(alle_p).set_color(YELLOW)

        self.add(verzerrtes_quadrat)