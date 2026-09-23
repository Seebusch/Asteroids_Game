MIN_ASTEROID_DISTANCE = 250
MANEUVERABILITY = 3
ACCELERATION = 0.2
BULLET_SPEED = 3
# Flugweite in Referenzpixeln. Schüsse verschwinden danach und am Bildschirmrand.
BULLET_RANGE = 560

# Startgröße des Fensters. Größe und Vollbild lassen sich zur Laufzeit ändern.
WINDOW_SIZE = (1280, 720)
# Größen und Abstände beziehen sich auf diese kurze Fensterseite.
SCREEN_REFERENCE = 720
# Anteil der kürzeren Fensterseite.
SHIP_SCREEN_FRACTION = 0.09
# Länge des hochformatigen Laserschusses.
BULLET_SCREEN_FRACTION = 0.06
ASTEROID_SCREEN_FRACTION = {
    3: 0.185,
    2: 0.112,
    1: 0.06,
}

# Level 1 entspricht der bisherigen Startwelle.
LEVEL_ASTEROID_BASE = 6
LEVEL_ASTEROID_STEP = 2
LEVEL_ASTEROID_CAP = 16
LEVEL_SPEED_MIN = 1
LEVEL_SPEED_MAX = 3
LEVEL_SPEED_STEP = 0.4
LEVEL_SPEED_CAP = 7.5
# Kurze Pause nach einer geräumten Welle, in Frames bei 60 FPS.
WAVE_CLEAR_FRAMES = 90