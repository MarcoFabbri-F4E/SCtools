.. SCtools documentation master file, created by
   sphinx-quickstart on Mon Nov  4 14:51:01 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SCtools documentation
=====================

This is the documentation for SCtools, a repository to manipulate and analyze CAD files 
in SpaceClaim and their related MCNP input files.

SCtools is a collection of several scripts. Many of them are written in IronPython and can 
be imported directly into SpaceClaim. Other scripts are meant to be run with CPython. 
Please refer to the documentation of each tool to understand how to use it.

The source code is hosted on `GitHub <https://github.com/Fusion4Energy/SCtools>`_.

.. raw:: html

   <div style="text-align: center;">
     <video style="width: 60%; max-width: 1080px;" controls autoplay loop muted>
       <source src="_static/SpaceClaim_adjust_volume.mp4" type="video/mp4">
       Your browser does not support the video tag.
     </video>
   </div>

List of tools
-------------

* :ref:`CSV workflow`. A set of scripts that greatly streamline and 
  facilitate the CAD to MCNP process.

  * :ref:`Prepare CAD`. Prepares the CAD model for the 
    workflow. It makes all the components independent of each other and assigns a to 
    each a unique ID.
  * :ref:`CSV generator`. Generates or updates the CSV file
    that contains all the information of the model as read by SpaceClaim.
  * :ref:`Detect volumes to adjust`. Highlights 
    the components that exceed the maximum volume deviation after simplification.
  * :ref:`Adjust volume`. Automatically extrudes the
    selected faces of a component to match the original volume of the component.
  * :ref:`Show by material`. Display only the components
    made of a selected list of materials.
  * :ref:`Save STEP`. Saves the CAD model as a STEP file
    in a way that the MCNP cell IDs will match the order of the CAD components.
  * :ref:`MCNP materials from CSV`. Updates the
    MCNP file with the materials, densities, density correction factors and component 
    names from the CSV file.

* :ref:`CAD to MCNP comparison`. This tool compares the 
  geometry of a CAD file in SpaceClaim with the geometry of the MCNP input file 
  generated from it. It can be used to check that the geometry in the CAD file is
  correctly translated to the MCNP input file.

* :ref:`Miscellaneous`. Set of one-off scripts that perform an 
  independent task.

  * :ref:`Elbow to cylinder`. Converts the toroidal elbows typically
    found in pipes in a set of cylinders.
  * :ref:`Detect torus`. Highlights all the bodies that 
    contain a toroidal surface.
  * :ref:`FMESH tally generator`. Generates a 
    FMESH tally card for MCNP from an arbitrarily sized and place SpaceClaim prismatic 
    body.
  * :ref:`Load CSV points`. Generates a set of points 
    in SpaceClaim from a CSV file. Synergizes with F4Enix lost particles features.
  * :ref:`Simplify toroidal profiles`. Simplifies the toroidal profile of a body 
    substituing the curves of its section with straight lines with a given angle between
    them.

* :ref:`Legacy`. Set of scripts that are either obsolete or outdated but may be useful
  in an future update.

  * :ref:`Report generation`. Automatically generates a 
    report with images and information of each component.
  * :ref:`Piping from CSV`. Generates a set of pipes from information read from a CSV 
    file. 

.. note::

   This project is under active development.

.. raw:: html

   <div class="video-popup">
       <a href="Adjust volume">Hover over me</a>
       <div class="video-content">
           <video controls autoplay loop muted>
               <source src="_static/Media1.mp4" type="video/mp4">
               Your browser does not support the video tag.
           </video>
       </div>
   </div>


.. toctree::
  :maxdepth: 3
  :hidden:

  usage
  csv_workflow
  cad_to_mcnp_comparison
  miscellaneous
  legacy
