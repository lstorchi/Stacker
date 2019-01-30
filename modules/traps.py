class trap:

    def __init__ (self, x = 0.0, y = 0.0, z = 0.0, \
            id = 0, energy = 0.0):
        
        self.__x = x
        self.__y = y
        self.__z = z

        self.__id = 0
        self.__energy = energy


    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_z(self):
        return self.__z
