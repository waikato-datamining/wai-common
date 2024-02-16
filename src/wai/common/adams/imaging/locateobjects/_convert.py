from ._LocatedObject import LocatedObject
from ._LocatedObjects import LocatedObjects
from ._NormalizedLocatedObject import NormalizedLocatedObject
from ._NormalizedLocatedObjects import NormalizedLocatedObjects
from wai.common.geometry import NormalizedPoint, NormalizedPolygon, Point, Polygon


def absolute_to_normalized(objects: LocatedObjects, width: int, height: int) -> NormalizedLocatedObjects:
    """
    Converts absolute objects into normalized ones.

    :param objects: the absolute objects to convert
    :type objects: LocatedObjects
    :param width: the width of the image to use for normalization
    :type width: int
    :param height: the height of the image to use for normalization
    :type height: int
    :return: the normalized objects
    :rtype: NormalizedLocatedObjects
    """
    result = NormalizedLocatedObjects()
    for aobj in objects:
        nobj = NormalizedLocatedObject(
            aobj.x / width, aobj.y / height,
            aobj.width / width, aobj.height / height,
            **aobj.metadata)
        if aobj.has_polygon():
            nx = [x / width for x in aobj.get_polygon_x()]
            ny = [y / height for y in aobj.get_polygon_y()]
            npoints = []
            for x, y in zip(nx, ny):
                npoint = NormalizedPoint(x, y)
                npoints.append(npoint)
            poly = NormalizedPolygon(*npoints)
            nobj.set_polygon(poly)
        result.append(nobj)
    return result


def normalized_to_absolute(objects: NormalizedLocatedObjects, width: int, height: int) -> LocatedObjects:
    """
    Converts normalized objects into absolute ones.

    :param objects: the normalized objects to convert
    :type objects: NormalizedLocatedObjects
    :param width: the width of the image to use for denormalization
    :type width: int
    :param height: the height of the image to use for denormalization
    :type height: int
    :return: the absolute objects
    :rtype: LocatedObjects
    """
    result = LocatedObjects()
    for nobj in objects:
        aobj = LocatedObject(
            round(nobj.x * width), round(nobj.y * height),
            round(nobj.width * width), round(nobj.height * height),
            **nobj.metadata)
        if nobj.has_polygon():
            ax = [round(x * width) for x in nobj.get_polygon_x()]
            ay = [round(y * height) for y in nobj.get_polygon_y()]
            apoints = []
            for x, y in zip(ax, ay):
                apoint = Point(x, y)
                apoints.append(apoint)
            apoly = Polygon(*apoints)
            aobj.set_polygon(apoly)
        result.append(aobj)
    return result
