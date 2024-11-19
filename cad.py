import os
import sys

# Add FreeCAD bin directory to PATH
os.environ["PATH"] = r"C:/ProgramData/Anaconda3/envs/cad/Library/bin" + ";" + os.environ["PATH"]

# Add FreeCAD lib directory to PYTHONPATH
sys.path.append(r"C:/ProgramData/Anaconda3/envs/cad/Library/lib")

# Import geouned (and FreeCAD will also load if needed)
import geouned

