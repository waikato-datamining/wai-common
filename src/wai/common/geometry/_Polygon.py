from typing import List

from ._Point import Point


class Polygon:
    """
    Represents a polygon in 2D integer Cartesian space.
    """
    def __init__(self, *points: Point):
        self.points: List[Point] = list(points)

    def __iter__(self):
        return iter(self.points)

    def area(self) -> float:
        """
        Calculates the area of the polygon using Greene's theorem.
        Assumes the polygon is not self-intersecting.

        Based on: https://stackoverflow.com/a/451482

        :return:    The area of the polygon.
        """
        return abs(
            sum(
                p1.x * p2.y - p2.x * p1.y
                for p1, p2 in zip(self.points, self.points[1:] + self.points[:1])
            )
        ) / 2
