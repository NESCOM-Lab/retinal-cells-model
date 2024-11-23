# -*- coding: utf-8 -*-
"""
Created on Nov 22 16:53:28 2024

*** FUNCTIONAL ***
Program that generates an equivalent OBJ file (using navis library to avoid imperfections)
Information on this dependency available here: https://navis-org.github.io/navis/

        Note: Line 222 from plot_utils.py had to be changed from:
            v = np.arange(tube_points, dtype=np.float_) / tube_points * 2 * np.pi
        to:
            v = np.arange(tube_points, dtype=np.float64) / tube_points * 2 * np.pi


@author: Kakolla, jmbouteiller
"""


# import numpy as np
# import trimesh
# import math
# import argparse
# import pandas as pd
import navis
# import matplotlib



def convert_to_obj_navis (input_filename, output_filename):

    # Example 
    # input_filename = 'retinal_cells/output1.swc'
    # obj_output_file = 'output_navis.obj'
    
    # Read and convert to TreeNeuron skeleton
    skeleton = navis.read_swc(input_filename)
    
    
    # Convert to a mesh 
    mymesh = navis.conversion.tree2meshneuron(skeleton)
    
    # Write the mesh to OBJ file
    navis.write_mesh(mymesh, output_filename)
    
    # fig, ax = skeleton.plot2d(
    #     method="3d_complex", view=("x", "-z"), non_view_axes3d="show", radius=True
    # )
    # # Change view to see the neurons from a different angle
    # ax.elev = -20
    # ax.azim = 45
    # ax.roll = 180
    # matplotlib.plt.tight_layout()
    
convert_to_obj_navis('./retinal_cells.swc', './output_navis.obj')

