class Step:
    def __init__(self, x: int, y: int, wall: str | None) -> None:
        assert wall in {"W", "S", "E", "N", None}, \
            "wall should be {W, S, E, N}"
        self.x = x
        self.y = y
        self.wall = wall
