import h5py

# 3rd party
import numpy

# our own 
import skeletalModel
import pose2D
import pose2Dto3D
import pose3D
import numpy
# from numba import njit
import cProfile
import multiprocessing
import tensorflow as tf

tf.config.experimental.list_physical_devices('GPU')
tf.test.is_gpu_available()
# Check if TensorFlow is built with CUDA
print("CUDA available: ", tf.test.is_built_with_cuda())

