import numpy 
import math

class electron:

    def __init__ (self):
        self.__x__ = []
        self.__y__ = []
        self.__z__ = []

        self.__npid__ = []
        self.__trapid__ = []
        self.__stateid__ = []

    def clear(self):
        self.__x__.clear()
        self.__y__.clear()
        self.__z__.clear()

        self.__npid__.clear()
        self.__trapid__.clear()
        self.__trapid__.clear()

    def append_xyz(self, x, y, z):
        self.__x__.append(x)
        self.__y__.append(y)
        self.__z__.append(z)

    def append_npid(self, id):
        self.__npid__.append(id)

    def append_trapid(self, id):
        self.__trapid__.append(id)

    def append_stateid(self, id):
        self.__stateid__.append(id)

    def get_npid(self):
        return self.__npid__

    def get_trapid(self):
        return self.__trapid__

    def get_stateid(self):
        return self.__stateid__

    def get_xyz(self):
        return self.__x__, self.__y__, self.__z__

    def get_allxyz(self):

        return numpy.transpose([self.__x__, \
                self.__y__, self.__z__])
    
    def get_distance_from_start(self):
        dist = 0.0

        if (len(self.__x__) > 1 and len(self.__y__) > 1 
                and len(self.__y__) > 1 ):
            xdiff = (self.__x__[0] - self.__x__[-1])**2
            ydiff = (self.__y__[0] - self.__y__[-1])**2
            zdiff = (self.__z__[0] - self.__z__[-1])**2

            dist = math.sqrt(xdiff + ydiff + zdiff)

        return dist

class trap:

    def __init__ (self, x = 0.0, y = 0.0, z = 0.0, \
            id = 0, energy = 0.0):
        
        self.__x__ = x
        self.__y__ = y
        self.__z__ = z

        self.__id__ = id
        self.__energy__ = energy
        self.__alpha__ = 0.0

        self.__electron__ = 0
        self.__electron_cont__ = None

        self.__npid__ = 0
        self.__atomid__ = 0

        self.release_time = 0.0
        self.__idxtojump__ = -1

    def __lt__(self, other):
        if type(other) is float:
            return self.release_time < other
        else:
            return self.release_time < other.release_time

    def __gt__(self, other):
        if type(other) is float:
            return self.release_time > other
        else:
            return self.release_time > other.release_time

    def __repr__(self):
        return 'R Time({})'.format(self.release_time)

    def get_idxtojump(self):
        return self.__idxtojump__

    def set_idxtojump(self, i):
        self.__idxtojump__ = i

    def get_energy(self):
        return self.__energy__

    def set_energy(self, e):
        self.__energy__ = e

    def get_alpha(self):
        return self.__alpha__

    def set_alpha(self, a):
        self.__alpha__ = a

    def get_npid(self):
        return self.__npid__

    def set_npid(self, i):
        self.__npid__ = i

    def get_atomid(self):
        return self.__atomid__

    def set_atomid(self, i):
        self.__atomid__ = i

    def get_id(self):
        return self.__id__

    def set_id(self, v):
        self.__id__ = v
        return True

    def get_x(self):
        return self.__x__

    def get_y(self):
        return self.__y__

    def get_z(self):
        return self.__z__

    def x(self):
        return self.__x__

    def y(self):
        return self.__y__

    def z(self):
        return self.__z__

    def get_position(self):
        return numpy.array([self.__x__, self.__y__, self.__z__])

    def electron(self):
        return self.__electron__

    def set_electron(self, i, e = None):
        self.__electron__ = i
        
        if e != None:
            e.append_xyz(self.__x__, self.__y__, self.__z__)
            e.append_npid(self.__npid__)
            e.append_stateid(self.__id__)

        self.__electron_cont__ = e

    def get_electron_cont(self):
        return self.__electron_cont__

