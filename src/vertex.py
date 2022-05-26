import math


class Vertex():
    def __init__(self, cords):
        self.next = None        # Set on calculation - next vertex in order
        self.prev = None        # Set on calculation - previous vertex in order
        self.cords = cords      # Passed - x,y coordinates of vertex point
        self.x = self.cords[0]  # x coordinate in 2-D axial space
        self.y = self.cords[1]  # y coordinate in 2-D axial space
        self.vtype = None       # Vertex type:
        # starting - less than 180, neighs lower
        # ending - less than 180, neighs higher
        # dividing - more than 180, neighs lower
        # merging - more than 180, neighs higher
        # normal - one neigh higher, one lower
        self.angle = None       # Inner-polygon angle
        self.index = None       # Index in vertex list -> creates the order
        self.upedge = None      # Edge object between 'self' and next vertex in order
        self.downedge = None    # Edge object between 'self' and previous vertex in order
        self.helper = None      # Helper vertex for current object

    def setAngle(self):
        """Calculates the angle at 'b' vertex"""
        ang = math.degrees(math.atan2(
            self.next.y-self.y, self.next.x-self.x)
            - math.atan2(self.prev.y-self.y, self.prev.x-self.x))
        self.angle = ang + 360 if ang < 0 else ang

    def setType(self):
        """Determines the type of vertex"""
        # Both neighbors higher
        if (self.next.y > self.y) and (self.prev.y > self.y):
            if self.angle < 180:
                self.vtype = 'ending'
            else:
                self.vtype = 'dividing'
        # Both neighbors lower
        elif (self.next.y < self.y) and (self.prev.y < self.y):
            if self.angle < 180:
                self.vtype = 'starting'
            else:
                self.vtype = 'merging'
        # Mixed height (guess so)
        else:
            self.vtype = 'normal'

    def vprint(self):
        """Prints all of the vertex parameters"""
        print(f'\nNext vertex index: {str(self.next.index)}')
        print(f'Prev vertex index: {str(self.prev.index)}')
        print(f'Vertex index in vlist: {str(self.index)}')
        print(f'Vertex coordinates{str(self.cords)}')
        print(f'Vertex x coordinate: {str(self.x)}')
        print(f'Vertex y coordinate: {str(self.y)}')
        print(f'Vertex type: {self.vtype}')
        print(f'Vertex inner-polygon angle: {str(self.angle)}\n')
        # print(f'{self.upedge}')
        # print(f'{self.downedge}')
        #print(f'Helper vertex index: {self.helper.index}')


class VertexList():
    def __init__(self):
        self.vlist = []         # List of vertexes
        self.last_index = None  # No. of last index in list
        self.how_many = None    # Counts of vertexes in list
        self.pointer = None     # Pointer -> indexing helper for calcs
        self.helper = None      # Helper object for calcs
        self.h_pointer = None   # Helper pointer (not sure if necessary)

    def update(self):
        """Updates last index,
        how many vertexes are in the list parameters"""
        self.last_index = len(self.vlist)-1
        self.how_many = len(self.vlist)

    def vappend(self, vertex):
        """Adds vertex object to list
        if it's first in the list - next and prev to him are set to him,
        if it's second or higher - next,prevs are being updated
        these are kind of pointers from C++"""
        self.vlist.append(vertex)
        vertex.index = self.vlist.index(vertex)

    def calculate_vertex_params(self):
        """While appending vertexes is done
        method sets proper values of next and previous vertex
        in the 'chain' and sets edges - up and down from vertex"""
        self.update()
        for i in range(len(self.vlist)):
            # Define next and previous vertex in order for first vertex
            if i == 0:
                self.vlist[i].next = self.vlist[i+1]
                self.vlist[i].prev = self.vlist[self.last_index]
            # Define next and previous vertex in order for last vertex
            elif i == self.last_index:
                self.vlist[i].next = self.vlist[0]
                self.vlist[i].prev = self.vlist[i-1]
            # Define next and previous vertex in order for a vertex in the middle of the list
            else:
                self.vlist[i].next = self.vlist[i+1]
                self.vlist[i].prev = self.vlist[i-1]
        for vertex in self.vlist:
            # Define edge going up, and the edge going down
            vertex.upedge = Edge(
                vertex, vertex.next)
            vertex.downedge = Edge(
                vertex.prev, vertex)
            # Calculates angle for vertex based on neighbors
            vertex.setAngle()
            # Determines type for a vertex in the list
            vertex.setType()


class Edge():
    def __init__(self, sv, ev):
        self.startvx = sv
        self.endvx = ev
        self.length = math.sqrt(
            (self.startvx.x - self.endvx.x)**2 + (self.startvx.y - self.endvx.y)**2)
