# standard
import h5py
import os
# 3rd party
import numpy

# our own 
import skeletalModel
import pose2D
import pose2Dto3D
import pose3D 
import tensorflow as tf
import multiprocessing
from tensorflow.distribute import experimental as tfexp
import threading

def save(fname, lst):
    dir_name = os.path.dirname(fname)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    T, dim = lst[0].shape
    with open(fname, 'a') as f:
        for t in range(T):
            for i in range(dim):
                for j in range(len(lst)):
                    f.write("%e\t" % lst[j][t, i])
            f.write("\n")

def getTXT(key, fnameIn, i, mode):
  output_file = f"out_data/{mode}/{key}/demo5.txt"
  if os.path.exists(output_file):
            print(f"Skipping {key} as output file already exists.")
            return
  else:
      # Getting our structure of skeletal model.
      # For customizing the structure see a definition of getSkeletalModelStructure. 
      dtype = "float32"
      randomNubersGenerator = numpy.random.RandomState(1234) 
      structure = skeletalModel.getSkeletalModelStructure()
      with h5py.File(fnameIn, "r") as hfIn:
            print("")
            print("Now is processing the "+ key)
            print("")
            inputSequence_2D = numpy.array(hfIn.get(key))

            # Decomposition of the single matrix into three matrices: x, y, w (=likelihood)
            X = inputSequence_2D
            print(X.shape)
            Xx = X[0:X.shape[0], 0:(X.shape[1]):3]
            Xy = X[0:X.shape[0], 1:(X.shape[1]):3]
            Xw = X[0:X.shape[0], 2:(X.shape[1]):3]
            #Xx = X[:, 0:X.shape[1]:3]
            #Xy = X[:, 1:X.shape[1]:3]
            #Xw = X[:, 2:X.shape[1]:3]


            # Normalization of the picture (x and y axis has the same scale)
            Xx, Xy = pose2D.normalization(Xx, Xy)
            save(f"out_data/{mode}/{key}/demo1.txt", [Xx, Xy, Xw])

            # Delete all skeletal models which have a lot of missing parts.
            Xx, Xy, Xw = pose2D.prune(Xx, Xy, Xw, (0, 1, 2, 3, 4, 5, 6, 7), 0.3, dtype)
            save(f"out_data/{mode}/{key}/demo2.txt", [Xx, Xy, Xw])

            # Preliminary filtering: weighted linear interpolation of missing points.
            Xx, Xy, Xw = pose2D.interpolation(Xx, Xy, Xw, 0.99, dtype)
            save(f"out_data/{mode}/{key}/demo3.txt", [Xx, Xy, Xw])

            # Initial 3D pose estimation
            lines0, rootsx0, rootsy0, rootsz0, anglesx0, anglesy0, anglesz0, Yx0, Yy0, Yz0 = pose2Dto3D.initialization(
                Xx,
                Xy,
                Xw,
                structure,
                0.001, # weight for adding noise
                randomNubersGenerator,
                dtype
              )
            save(f"out_data/{mode}/{key}/demo4.txt", [Yx0, Yy0, Yz0])

              # Backpropagation-based filtering
            Yx, Yy, Yz = pose3D.backpropagationBasedFiltering(
                lines0, 
                rootsx0,
                rootsy0, 
                rootsz0,
                anglesx0,
                anglesy0,
                anglesz0,   
                Xx,   
                Xy,
                Xw,
                structure,
                dtype,
              )
            save(f"out_data/{mode}/{key}/demo5.txt", [Yx, Yy, Yz])
            # Called after each folder is processed to release GPU resources
            print(f"Now we're working on folder {i} th, and will be finished")
            i=i+1
            tf.keras.backend.clear_session()


if __name__ == "__main__":
  
  mode = "test"
  
  
  multiprocessing.freeze_support()
  dtype = "float32"
  randomNubersGenerator = numpy.random.RandomState(1234)
  i = 1

  # This demo shows converting a result of 2D pose estimation into a 3D pose.
  
  # Getting 2D data
  # The sequence is an N-tuple of
  #   (1sf point - x, 1st point - y, 1st point - likelihood, 2nd point - x, ...)
  # a missing point should have x=0, y=0, likelihood=0 
  # f = h5py.File("data/demo-sequence.h5", "r")
  fnameIn = f"input_data/{mode}.h5"

  hfIn = h5py.File(fnameIn, "r")

  keys = list(hfIn.keys())
  print(keys)
    
  #with strategy.scope():
  #      for key in keys:
  #          getTXT(key, fnameIn, i)
  #          tf.keras.backend.clear_session()
  # Change the number of processes in the Pool to the number of available Gpus
  
  #with multiprocessing.Pool(processes=2) as pool: #len(gpus)
  #    pool.starmap(getTXT, [(key, fnameIn, i, mode) for key in keys])
    
  for key in keys:
    getTXT(key, fnameIn, i, mode)

  print(f"All file have finished!!!!!")
  
  hfIn.close()
