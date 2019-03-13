import numpy 

class trap:

    def __init__ (self, x = 0.0, y = 0.0, z = 0.0, \
            id = 0, energy = 0.0):
        
        self.__x__ = x
        self.__y__ = y
        self.__z__ = z

        self.__id__ = 0
        self.__energy__ = energy

        self.__electron__ = 0

        self.__npid__ = 0
        self.__atomid__ = 0

        self.release_time = 0.0

    def __lt__(self, other):
        return self.release_time < other.release_time

    def __gt__(self, other):
        return self.release_time > other.release_time

    def __repr__(self):
        return 'R Time({})'.format(self.release_time)

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

    def set_electron(self, i):
        self.__electron__ = i

