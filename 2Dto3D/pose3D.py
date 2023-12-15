# standard

# 3rd party
import numpy
import tensorflow as tf

# our own 
import skeletalModel



def backpropagationBasedFiltering(
  lines0_values, # initial (logarithm of) bones lenghts
  rootsx0_values, # head position
  rootsy0_values, 
  rootsz0_values,
  anglesx0_values, # angles of limbs
  anglesy0_values,
  anglesz0_values,   
  tarx_values, # target   
  tary_values,
  w_values, # weights of estimated points (likelihood of estimation)   
  structure,
  dtype,
  learningRate=0.1,
  nCycles=1000,
  regulatorRates=[0.001, 0.1],
):

  T = rootsx0_values.shape[0]
  nBones, nPoints = skeletalModel.structureStats(structure)
  nLimbs = len(structure)

  # vector of (logarithm of) bones length
  #   shape: (nLines,)
  lines = tf.Variable(lines0_values, dtype=dtype) 
  # x cooordinates of head
  #   shape: (T, 1)
  rootsx = tf.Variable(rootsx0_values, dtype=dtype)
  # y cooordinates of head
  rootsy = tf.Variable(rootsy0_values, dtype=dtype) 
  # z cooordinates of head
  rootsz = tf.Variable(rootsz0_values, dtype=dtype)
  # x coordinate of angles 
  #   shape: (T, nLimbs)
  anglesx = tf.Variable(anglesx0_values, dtype=dtype)
  # y coordinate of angles 
  anglesy = tf.Variable(anglesy0_values, dtype=dtype)
  # z coordinate of angles 
  anglesz = tf.Variable(anglesz0_values, dtype=dtype)   

  # target
  #   shape: (T, nPoints)
  tarx = tf.placeholder(dtype=dtype)
  tary = tf.placeholder(dtype=dtype)
  # likelihood from previous pose estimator
  #   shape: (T, nPoints)
  w = tf.placeholder(dtype=dtype)
  
  # resultant coordinates. It's a list for now. It will be concatenate into a matrix later
  #   shape: (T, nPoints)
  x = [None for i in range(nPoints)]
  y = [None for i in range(nPoints)]
  z = [None for i in range(nPoints)]
  
  # head first
  x[0] = rootsx
  y[0] = rootsy
  z[0] = rootsz
  
  # now other limbs
  i = 0
  # for numerical stability of angles normalization
  epsilon = 1e-10
  for a, b, l in structure:
    # limb length
    L = tf.exp(lines[l])
    # angle
    Ax = anglesx[0:T, i:(i + 1)]
    Ay = anglesy[0:T, i:(i + 1)]
    Az = anglesz[0:T, i:(i + 1)]
    # angle norm
    normA = tf.sqrt(tf.square(Ax) + tf.square(Ay) + tf.square(Az)) + epsilon
    # new joint position
    x[b] = x[a] + L * Ax / normA
    y[b] = y[a] + L * Ay / normA
    z[b] = z[a] + L * Az / normA
    i = i + 1
  
  # making a matrix from the list
  x = tf.concat(x, axis=1)
  y = tf.concat(y, axis=1)
  z = tf.concat(z, axis=1)

  # weighted MSE
  loss = tf.reduce_sum(w * tf.square(x - tarx) + w * tf.square(y - tary)) / (T * nPoints)
  
  # regularozators
  # reg1 is a sum of bones length
  reg1 = tf.reduce_sum(tf.exp(lines))
  # reg2 is a square of trajectory length
  dx = x[0:(T - 1), 0:nPoints] - x[1:T, 0:nPoints]
  dy = y[0:(T - 1), 0:nPoints] - y[1:T, 0:nPoints]
  dz = z[0:(T - 1), 0:nPoints] - z[1:T, 0:nPoints]
  reg2 = tf.reduce_sum(tf.square(dx) + tf.square(dy) + tf.square(dz)) / ((T - 1) * nPoints)
  
  optimizeThis = loss + regulatorRates[0] * reg1 + regulatorRates[1] * reg2

  # the backpropagation
  optimizer = tf.train.GradientDescentOptimizer(learningRate)
  train = optimizer.minimize(optimizeThis)
  init = tf.variables_initializer(tf.global_variables())
  sess = tf.Session()
  sess.run(init)
  for iCycle in range(nCycles):
    sess.run(train, {tarx: tarx_values, tary: tary_values, w: w_values})
    print("iCycle = %3d, loss = %e" % (iCycle, sess.run([loss], {tarx: tarx_values, tary: tary_values, w: w_values})[0]))
  
  # returning final coordinates
  return sess.run([x, y, z], {})
 


if __name__ == "__main__":
  # debug - don't run it
  
  #
  #             (0)
  #              |
  #              |
  #              0
  #              |
  #              |
  #     (2)--1--(1)--1--(3)
  #
  structure = (
    (0, 1, 0),
    (1, 2, 1),
    (1, 3, 1),
  )

  T = 3
  nBones, nPoints = skeletalModel.structureStats(structure)
  nLimbs = len(structure)
  
  dtype = "float32"

  lines0_values = numpy.zeros((nBones, ), dtype=dtype) 
  rootsx0_values = numpy.ones((T, 1), dtype=dtype)
  rootsy0_values = numpy.ones((T, 1), dtype=dtype) 
  rootsz0_values = numpy.ones((T, 1), dtype=dtype)
  anglesx0_values = numpy.ones((T, nLimbs), dtype=dtype)
  anglesy0_values = numpy.ones((T, nLimbs), dtype=dtype)
  anglesz0_values = numpy.ones((T, nLimbs), dtype=dtype)   
  
  w_values = numpy.ones((T, nPoints), dtype=dtype)
  
  tarx_values = numpy.ones((T, nPoints), dtype=dtype)   
  tary_values = numpy.ones((T, nPoints), dtype=dtype)   

  x_values, y_values, z_values = backpropagationBasedFiltering(
    lines0_values, 
    rootsx0_values,
    rootsy0_values, 
    rootsz0_values,
    anglesx0_values,
    anglesy0_values,
    anglesz0_values,
    tarx_values,   
    tary_values,
    w_values,   
    structure,
    dtype,
  )

