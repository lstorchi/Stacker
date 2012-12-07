import point

###############################################################################

class line2d:

  # y = m x + q

  def __init__(self, m = 0.0, q = 0.0):
    self.m = m
    self.q = q

    self.p1 = [0.0, 0.0]
    self.p2 = [0.0, 0.0]

  def set_q (self, q = 0.0):
    self.q = q

  def set_m (self, m = 0.0):
    self.m = m

  def get_q (self):
    return self.q

  def get_m (self):
    return self.m

  def set_two_point (self, p1 = [0.0, 0.0], p2 = [0.0, 0.0]):

    self.p1 = p1
    self.p2 = p2

    self.m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    self.q = p1[1] - self.m * p1[0]

  def get_p1(self):
    return self.p1

  def get_p2(self):
    return self.p2

###############################################################################

# http://www.youtube.com/watch?v=r24zBidwago
# equazione vettoriale della retta da idea di come poi 
# posso pensare di fare la generazione fatta qui sotto

class line3d:

  # (x,y,z) = (a1, a2, a3) + t * (b1, b2, b3)

  def __init__(self):
    self._a = point.point(0.0, 0.0, 0.0)
    self._b = point.point(0.0, 0.0, 0.0) 


  def set_two_point (self, p1, p2):

    # cosi' parto da p1 a seguire se genero punti con delta fisso
    self._b = p2-p1
    self._a = p1


  def set_a(self, p):
    self._a = p

  
  def set_b(self, p):
    self._b = p


  def generate_equi_point (self, n):
 
    # genero n punti con delta d da p1 a p2 
    plist = []

    step = 1.0/(float(n))
    for i in range(n):
      t = point.point (
          self._b.get_x(), 
          self._b.get_y(), 
          self._b.get_z())

      a = point.point (
          self._a.get_x(), 
          self._a.get_y(), 
          self._a.get_z())

      t.by_scalar(step*float(i+1))
      p = a + t
      plist.append(p)

    return plist

###############################################################################
