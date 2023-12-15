#  Packing relevant (see variable idxsPose and idxsHand) keypoints stored as json files into a single h5 file. 
#  Format: x, y, likelihood, x, y, likelihood, ....
#  x == 0, y == 0 means missing keypoint 

import codecs
import math
import re
import os
import json
import h5py
import subprocess

import numpy
from walkDir import walkDir


def selectPoints(points, keepThis):
  points2 = []
  for i in keepThis:
    points2.append(points[3 * i + 0])
    points2.append(points[3 * i + 1])
    points2.append(points[3 * i + 2])
  return points2


def noNones(l):
  l2 = []
  for i in l:
    if not i is None:
      l2.append(i)
  return l2


def loadData(dname):
  fnames = walkDir(dname = dname, filt = r"\.json$")
  fnames.sort()
  frames = []
  for fname in fnames:
    p = re.search(r"([^\\/]+)_(\d+)_keypoints\.json$", fname)
    
    with open(fname) as json_data:
      data = json.load(json_data)
    if len(data["people"]) == 0:
      continue
      
    i = int(p.group(2))
    while len(frames) < i + 1:
      frames.append(None)
    
    theTallest = data["people"][0]
    
    idxsPose = [0, 1, 2, 3, 4, 5, 6, 7]
    idxsHand = range(21)    

    if theTallest is None:
      points = 3 * (len(idxsPose) + 2 * len(idxsHand)) * [0.0]
    else:
      pointsP = theTallest["pose_keypoints_2d"]
      pointsLH = theTallest["hand_left_keypoints_2d"]
      pointsRH = theTallest["hand_right_keypoints_2d"]
      pointsP = selectPoints(pointsP, idxsPose)
      pointsLH = selectPoints(pointsLH, idxsHand)
      pointsRH = selectPoints(pointsRH, idxsHand)
      points = pointsP + pointsLH + pointsRH

    if not points[0] == 0.0:
      frames[i] = points
    
  return numpy.asarray(noNones(frames), dtype="float32")


if __name__ == "__main__":

  dnameIn = "S:/how2sign-pre/how2sign原数据/val_2D_keypoints正面开发集/json"
  # dnameIn = "S:/how2sign-pre/how2sign原数据/val_2D_keypoints正面开发集/json"
  # dnameIn = "S:/how2sign-pre/how2sign原数据/val_2D_keypoints正面训练集/json"
  # fnameOut = "data/demo/keypoints/keypoints-01-raw.h5"
  fnameOut = "S:/how2sign-pre/2Dto3D/input_data/dev.h5"
  
  
  recs = {}
  for fname in walkDir(dnameIn, filt=r"\.[jJ][sS][oO][nN]$"):
    dname = re.sub(r"(.*)[/\\].*", r"\1", fname)
    key = re.sub(r".*[/\\]", "", dname)
    recs[key] = dname
  
  hf = h5py.File(fnameOut, "w")
  for key in recs:
    print(key)
    data = loadData(recs[key])
    hf.create_dataset(key, data=data, dtype="float32")    
  hf.close()
