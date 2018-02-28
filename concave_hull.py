import numpy as np
from scipy.spatial import Delaunay
import shapely.geometry as sg
import shapely.ops as so

def alpha_shape(self, points, alpha):
        """
        Compute the alpha shape (concave hull) of a set
        of points.
        @param points: Iterable container of points.
        @param alpha: alpha value to influence the
            gooeyness of the border. Smaller numbers
            don't fall inward as much as larger numbers.
            Too large, and you lose everything!
        """
        if len(points) < 4:
            # When you have a triangle, there is no sense
            # in computing an alpha shape.
            return sg.MultiPoint(list(points)).convex_hull

        def add_edge(edges, edge_points, coords, i, j):
            """
            Add a line between the i-th and j-th points,
            if not in the list already
            """
            if (i, j) in edges or (j, i) in edges:
                # already added
                return
            edges.add((i, j))
            edge_points.append(coords[[i, j]])

        # coords = np.array([point.coords[0] for point in points])
        coords = points
        tri = Delaunay(coords)
        edges = set()
        edge_points = []
        # loop over triangles:
        # ia, ib, ic = indices of corner points of the
        # triangle
        for ia, ib, ic in tri.vertices:
            pa = coords[ia]
            pb = coords[ib]
            pc = coords[ic]
            # Lengths of sides of triangle
            a = np.sqrt((pa[0] - pb[0])**2 + (pa[1] - pb[1])**2)
            b = np.sqrt((pb[0] - pc[0])**2 + (pb[1] - pc[1])**2)
            c = np.sqrt((pc[0] - pa[0])**2 + (pc[1] - pa[1])**2)
            # Semiperimeter of triangle
            s = (a + b + c) / 2.0
            # Area of triangle by Heron's formula
            area = np.sqrt(s * (s - a) * (s - b) * (s - c))
            circum_r = a * b * c / (4.0 * area)

            if self.init_run:
                self.all_circum_r.append(circum_r)

            # Here's the radius filter.
            #print(circum_r, 1.0 / alpha)
            if circum_r < 1.0 / alpha:
                add_edge(edges, edge_points, coords, ia, ib)
                add_edge(edges, edge_points, coords, ib, ic)
                add_edge(edges, edge_points, coords, ic, ia)
        m = sg.MultiLineString(edge_points)
        triangles = list(so.polygonize(m))
        return so.cascaded_union(triangles), edge_points