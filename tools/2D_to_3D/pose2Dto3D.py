# standard
import math

# 3rd party
import numpy

# our own
import skeletalModel


# add uniformly distributed noise
def addNoise(x, rng, epsilon):
  e = numpy.asarray(rng.uniform(low=-epsilon, high=epsilon, size=x.shape), dtype="float32")
  return x + e


def norm(x):
  result = 0.0
  for i in x:
    result = result + i * i
  return math.sqrt(result)


# A simple percentile computation.
# Warning: it sorts input list. 
def perc(lst, p):
  lst.sort()
  return lst[int(p * (len(lst) - 1))] 


# some substitution
def computeB(ax, ay, az, tx, ty, L):
  hyps = [
    [tx - ax, ty - ay, 0]
  ]
  foo = L**2 - (tx - ax)**2 - (ty - ay)**2;
  if foo >= 0:
    hyps.append([tx - ax, ty - ay, -math.sqrt(foo)])
    hyps.append([tx - ax, ty - ay, +math.sqrt(foo)])
  foo1 = ax**2 - 2*ax*tx + ay**2 - 2*ay*ty + tx**2 + ty**2
  foo2 = (1/foo1)**(1/2)
  foo3 = ay**3/foo1 + L*ay*foo2 - L*ty*foo2 + (ax**2*ay)/foo1 + (ay*tx**2)/foo1 + (ay*ty**2)/foo1 - (2*ay**2*ty)/foo1 - (2*ax*ay*tx)/foo1
  foo4 = ay**3/foo1 - L*ay*foo2 + L*ty*foo2 + (ax**2*ay)/foo1 + (ay*tx**2)/foo1 + (ay*ty**2)/foo1 - (2*ay**2*ty)/foo1 - (2*ax*ay*tx)/foo1
  xx1 = -(ax*ty - ay*tx - ax*foo3 + tx*foo3)/(ay - ty)
  xx2 = -(ax*ty - ay*tx - ax*foo4 + tx*foo4)/(ay - ty)
  xy1 = ay**3/foo1 + L*ay*foo2 - L*ty*foo2 + (ax**2*ay)/foo1 + (ay*tx**2)/foo1 + (ay*ty**2)/foo1 - (2*ay**2*ty)/foo1 - (2*ax*ay*tx)/foo1
  xy2 = ay**3/foo1 - L*ay*foo2 + L*ty*foo2 + (ax**2*ay)/foo1 + (ay*tx**2)/foo1 + (ay*ty**2)/foo1 - (2*ay**2*ty)/foo1 - (2*ax*ay*tx)/foo1
  if 0 * xx1 * xx2 * xy1 * xy2 == 0:
    hyps.append([xx1 - ax, xy1 - ay, 0])
    hyps.append([xx2 - ax, xy2 - ay, 0])
  angle = [1.0, 1.0, 0.0]
  Lmin = None
  for hypangle in hyps:
    normHypangle = norm(hypangle) + 1e-10
    xi = [
      ax + L * hypangle[0] / normHypangle,
      ay + L * hypangle[1] / normHypangle,
      az + L * hypangle[2] / normHypangle,
    ]
    Li = (xi[0] - tx)**2 + (xi[1] - ty)**2;
    if Lmin is None or Lmin > Li:
      Lmin = Li
      angle = hypangle
  return angle


# The initial 3D eastiamtion. It returns:
#   lines - logarithm of bone lengths
#   rootsx, rootsy, rootsz - 3D coordinates of head (root in the graph) positions 
#   anglesx, anglesy, anglesz - absolute angles of limbs (3D coordinates) 
#   Yx, Yy, Yz - resultant 3D coordinates
def initialization(Xx, Xy, Xw, structure, sigma, randomNubersGenerator, dtype, percentil=0.5):
  T = Xx.shape[0]
  n = Xx.shape[1]
  
  nLines, nPoints = skeletalModel.structureStats(structure)
  
  lines = numpy.zeros((nLines, ), dtype=dtype)

  rootsx = Xx[0:T, 0]
  rootsy = Xy[0:T, 0]
  rootsz = numpy.zeros((T, ), dtype=dtype)

  rootsx = addNoise(rootsx, randomNubersGenerator, sigma)
  rootsy = addNoise(rootsy, randomNubersGenerator, sigma)
  rootsz = addNoise(rootsz, randomNubersGenerator, sigma)

  anglesx = numpy.zeros((T, len(structure)), dtype=dtype)
  anglesy = numpy.zeros((T, len(structure)), dtype=dtype)
  anglesz = numpy.zeros((T, len(structure)), dtype=dtype)
  
  Yx = numpy.zeros((T, n), dtype=dtype)
  Yy = numpy.zeros((T, n), dtype=dtype)
  Yz = numpy.zeros((T, n), dtype=dtype)
  Yx[0:T, 0] = rootsx
  Yy[0:T, 0] = rootsy
  Yz[0:T, 0] = rootsz

  Ls = {}
  for iBone in range(len(structure)):
    a, b, line = structure[iBone]
    if not line in Ls:
      Ls[line] = []
    for t in range(T):
      ax = Xx[t, a]
      ay = Xy[t, a]
      bx = Xx[t, b]
      by = Xy[t, b]
      wa = Xw[t, a]
      wb = Xw[t, b]
      w = min([wa, wb]);
      L = norm([ax - bx, ay - by])
      Ls[line].append(L)
  for i in range(len(lines)):
    #lines[i] = math.log(perc(Ls[i], percentil))
    lines[i] = math.log(max(perc(Ls[i], percentil), 1e-6))
  
  for iBone in range(len(structure)):
    a, b, line = structure[iBone]
    L = math.exp(lines[line]);
    for t in range(T):
      ax = Yx[t, a]
      ay = Yy[t, a]
      az = Yz[t, a]
      
      tx = Xx[t, b]
      ty = Xy[t, b]
      
      anglex, angley, anglez = computeB(ax, ay, az, tx, ty, L)
      if not 0.0 * anglex == 0.0: # no inf or nan
        anglex = 0.0
      if not 0.0 * angley == 0.0: # no inf or nan
        angley = 0.0
      if not 0.0 * anglez == 0.0: # no inf or nan
        anglez = 0.0
      if anglex == 0.0 and angley == 0.0 and anglez == 0.0:
        anglex = 1.0
        angley = 1.0
        anglez = 1.0
      if anglez < 0.0:
        anglez = -anglez
      
      anglez = anglez + 0.001
      
      normAngle = math.sqrt(anglex * anglex + angley * angley + anglez * anglez) + 1e-10
      anglesx[t, iBone] = anglex / normAngle
      anglesy[t, iBone] = angley / normAngle
      anglesz[t, iBone] = anglez / normAngle
    
    for t in range(T):
      Yx[t, b] = Yx[t, a] + L * anglesx[t, iBone]  
      Yy[t, b] = Yy[t, a] + L * anglesy[t, iBone]
      Yz[t, b] = Yz[t, a] + L * anglesz[t, iBone]

  rootsx = rootsx.reshape((rootsx.shape[0], 1))
  rootsy = rootsy.reshape((rootsy.shape[0], 1))
  rootsz = rootsz.reshape((rootsz.shape[0], 1))
  
  return lines, rootsx, rootsy, rootsz, anglesx, anglesy, anglesz, Yx, Yy, Yz
