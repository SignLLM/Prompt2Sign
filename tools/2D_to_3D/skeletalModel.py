# This function gives our structure of skeletal model


def getSkeletalModelStructure():
  # Definition of skeleton model structure:
  #   The structure is an n-tuple of:
  #
  #   (index of a start point, index of an end point, index of a bone) 
  #
  #   E.g., this simple skeletal model
  #
  #             (0)
  #              |
  #              |
  #              0
  #              |
  #              |
  #     (2)--1--(1)--1--(3)
  #      |               |
  #      |               |
  #      2               2
  #      |               |
  #      |               |
  #     (4)             (5)
  #
  #   has this structure:
  #
  #   (
  #     (0, 1, 0),
  #     (1, 2, 1),
  #     (1, 3, 1),
  #     (2, 4, 2),
  #     (3, 5, 2),
  #   )
  #
  #  Warning 1: The structure has to be a tree.  
  #
  #  Warning 2: The order isn't random. The order is from a root to lists.
  #

  return ( 
    # head
    (0, 1, 0),

    # left shoulder
    (1, 2, 1),

    # left arm
    (2, 3, 2),
    (3, 4, 3),

    # right shoulder
    (1, 5, 1), 

    # right arm
    (5, 6, 2),
    (6, 7, 3),
  
    # left hand - wrist
    (7, 8, 4),
  
    # left hand - palm
    (8, 9, 5),
    (8, 13, 9),
    (8, 17, 13),
    (8, 21, 17),
    (8, 25, 21),

    # left hand - 1st finger
    (9, 10, 6),
    (10, 11, 7),
    (11, 12, 8),

    # left hand - 2nd finger
    (13, 14, 10),
    (14, 15, 11),
    (15, 16, 12),
  
    # left hand - 3rd finger
    (17, 18, 14),
    (18, 19, 15),
    (19, 20, 16),
  
    # left hand - 4th finger
    (21, 22, 18),
    (22, 23, 19),
    (23, 24, 20),
  
    # left hand - 5th finger
    (25, 26, 22),
    (26, 27, 23),
    (27, 28, 24),
  
    # right hand - wrist
    (4, 29, 4),
  
    # right hand - palm
    (29, 30, 5), 
    (29, 34, 9),
    (29, 38, 13),
    (29, 42, 17),
    (29, 46, 21),

    # right hand - 1st finger
    (30, 31, 6),
    (31, 32, 7),
    (32, 33, 8),
  
    # right hand - 2nd finger
    (34, 35, 10),
    (35, 36, 11),
    (36, 37, 12),
  
    # right hand - 3rd finger
    (38, 39, 14),
    (39, 40, 15),
    (40, 41, 16),
  
    # right hand - 4th finger
    (42, 43, 18),
    (43, 44, 19),
    (44, 45, 20),
  
    # right hand - 5th finger
    (46, 47, 22),
    (47, 48, 23),
    (48, 49, 24), 
  )


# Computing number of joints and limbs
def structureStats(structure):
  ps = {}
  ls = {}
  for a, b, l in structure:
    ps[a] = "gotcha"
    ps[b] = "gotcha"
    ls[l] = "gotcha"
  return len(ls), len(ps)
