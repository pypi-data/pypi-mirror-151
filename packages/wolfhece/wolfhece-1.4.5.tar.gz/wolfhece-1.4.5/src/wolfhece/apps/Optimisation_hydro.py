import os
import wx
import sys
import numpy as np
import matplotlib.pyplot as plt
from numpy.core.shape_base import block
from numpy.testing._private.utils import measure
from wolfhece.hydrology.Optimisation import Optimisation


try:
    from ..PyTranslate import *
    from ..hydrology.PostProcessHydrology import PostProcessHydrology
    from ..hydrology.Catchment import *
    from ..PyParams import*
except:
    from wolfhece.PyTranslate import *
    from wolfhece.hydrology.PostProcessHydrology import PostProcessHydrology
    from wolfhece.hydrology.Catchment import *
    from wolfhece.PyParams import*



def main():
    app = wx.App()
    myOpti = Optimisation()

    # %% Show  graphs
    myOpti.Show()
    app.MainLoop()
    print("That's all folks! ")

if __name__=='__main__':
    main()