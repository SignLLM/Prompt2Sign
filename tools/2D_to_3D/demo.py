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

  

if __name__ == "__main__":
  
  dtype = "float32"
  randomNubersGenerator = numpy.random.RandomState(1234)

  # This demo shows converting a result of 2D pose estimation into a 3D pose.
  
  # Getting our structure of skeletal model.
  # For customizing the structure see a definition of getSkeletalModelStructure.  
  structure = skeletalModel.getSkeletalModelStructure()
  
  # Getting 2D data
  # The sequence is an N-tuple of
  #   (1sf point - x, 1st point - y, 1st point - likelihood, 2nd point - x, ...)
  # a missing point should have x=0, y=0, likelihood=0 
  # f = h5py.File("data/demo-sequence.h5", "r")
  f = h5py.File("S:/how2sign-pre/2Dto3D/input_data/dev.h5", "r")
  keys = list(f.keys())
  print(keys)
  for key in keys:
    print("Now is processing the "+ key)
    inputSequence_2D = numpy.array(f.get(key))
    
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
    save(f"out_data/dev/{key}/demo1.txt", [Xx, Xy, Xw])

    # Delete all skeletal models which have a lot of missing parts.
    Xx, Xy, Xw = pose2D.prune(Xx, Xy, Xw, (0, 1, 2, 3, 4, 5, 6, 7), 0.3, dtype)
    save(f"out_data/dev/{key}/demo2.txt", [Xx, Xy, Xw])
    
    # Preliminary filtering: weighted linear interpolation of missing points.
    Xx, Xy, Xw = pose2D.interpolation(Xx, Xy, Xw, 0.99, dtype)
    save(f"out_data/dev/{key}/demo3.txt", [Xx, Xy, Xw])
    
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
    save(f"out_data/dev/{key}/demo4.txt", [Yx0, Yy0, Yz0])
      
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
    save(f"out_data/dev/{key}/demo5.txt", [Yx, Yy, Yz])
  
  f.close()

  
