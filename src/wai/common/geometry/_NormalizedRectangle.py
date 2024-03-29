from typing import Tuple, Optional

from ._NormalizedPoint import NormalizedPoint


class NormalizedRectangle:
    """
    Represents an axis-aligned rectangle in 2D integer Cartesian coordinates.
    """
    def __init__(self, p1: NormalizedPoint, p2: NormalizedPoint):
        self.p1: NormalizedPoint = p1
        self.p2: NormalizedPoint = p2

    def left(self) -> float:
        """
        Gets the x-coordinate of the left-hand side of this rectangle.

        :return:    The x-coordinate.
        """
        return min(self.p1.x, self.p2.x)

    def right(self) -> float:
        """
        Gets the x-coordinate of the right-hand side of this rectangle.

        :return:    The x-coordinate.
        """
        return max(self.p1.x, self.p2.x)

    def top(self) -> float:
        """
        Gets the y-coordinate of the top side of this rectangle.

        :return:    The y-coordinate.
        """
        return min(self.p1.y, self.p2.y)

    def bottom(self) -> float:
        """
        Gets the y-coordinate of the bottom side of this rectangle.

        :return:    The y-coordinate.
        """
        return max(self.p1.y, self.p2.y)

    def width(self) -> float:
        """
        Gets the width of the rectangle.

        :return: The rectangle's width.
        """
        return abs(self.p1.x - self.p2.x)

    def height(self) -> float:
        """
        Gets the height of the rectangle.

        :return:    The rectangle's height.
        """
        return abs(self.p1.y - self.p2.y)

    def area(self) -> float:
        """
        Gets the area of this rectangle.

        :return:    The area.
        """
        return self.width() * self.height()

    @classmethod
    def x_y_w_h(cls, x: float, y: float, w: float, h: float) -> "NormalizedRectangle":
        """
        Instantiates a rectangle from its (x, y) position and width and height.

        :param x:   The x-position of the left side of the rectangle.
        :param y:   The y-position of the top side of the rectangle.
        :param w:   The rectangle's width.
        :param h:   The rectangle's height.
        :return:    The rectangle.
        """
        if w < 0:
            x += w
            w = abs(w)

        if h < 0:
            y += h
            h = abs(h)

        return cls(NormalizedPoint(x, y), NormalizedPoint(x + w, y + h))

    def intersects(self, other: "NormalizedRectangle") -> bool:
        """
        Checks if this rectangle intersects with another rectangle.

        :param other:   The other rectangle.
        :return:        True if they intersect.
        """
        # Check for overlap in the x-dimension
        if not self.contains_x(other.left()) and not other.contains_x(self.left()):
            return False

        # Check for overlap in the y-dimension
        if not self.contains_y(other.top()) and not other.contains_y(self.top()):
            return False

        return True

    def intersection(self, other: "NormalizedRectangle") -> Optional["NormalizedRectangle"]:
        """
        Gets the intersection of this rectangle and another.

        :param other:   The rectangle to intersect with.
        :return:        The rectangle representing the intersection,
                        or None if the two rectangle don't intersect.
        """
        # Check for overlap
        if not self.intersects(other):
            return None

        return NormalizedRectangle(NormalizedPoint(max(self.left(), other.left()), max(self.top(), other.top())),
                                   NormalizedPoint(min(self.right(), other.right()), min(self.bottom(), other.bottom())))

    def contains_x(self, x: float) -> bool:
        """
        Whether the given x-coordinate is inside the range covered
        by the rectangle.

        :param x:   The x-coordinate.
        :return:    True if the x-coordinate overlaps the rectangle.
        """
        return self.left() <= x <= self.right()

    def contains_y(self, y: float) -> bool:
        """
        Whether the given y-coordinate is inside the range covered
        by the rectangle.

        :param y:   The y-coordinate.
        :return:    True if the y-coordinate overlaps the rectangle.
        """
        return self.top() <= y <= self.bottom()

    def __contains__(self, point: NormalizedPoint) -> bool:
        """
        Whether the given point is inside the rectangular bounds.

        :param point:   The point.
        :return:        True if the point is in the rectangle.
        """
        return self.contains_x(point.x) and self.contains_y(point.y)

    def off_diagonal_points(self) -> Tuple[NormalizedPoint, NormalizedPoint]:
        """
        Gets the corner points that are off the main diagonal
        of this rectangle.

        :return:    The two off-diagonal points.
        """
        return NormalizedPoint(self.p1.x, self.p2.y), NormalizedPoint(self.p2.x, self.p1.y)

    def __hash__(self):
        return hash((self.left(), self.top(), self.right(), self.bottom()))

    def __eq__(self, other):
        return (isinstance(other, NormalizedRectangle) and
                self.left() == other.left() and
                self.right() == other.right() and
                self.top() == other.top() and
                self.bottom() == other.bottom())
