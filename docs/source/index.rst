.. SCtools documentation master file, created by
   sphinx-quickstart on Mon Nov  4 14:51:01 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SCtools documentation
=====================

This is the documentation for SCtools, a repository to manipulate and analyze CAD files 
in SpaceClaim and their related MCNP input files.

SCtools is a collection of several scripts many of them written in IronPython that can 
be imported directly into SpaceClaim. Other scripts are meant to be run with CPython. 
Please refer to the documentation of each tool to understand how to use it.

The source code is hosted on `GitHub <https://github.com/Fusion4Energy/SCtools>`_.

.. raw:: html

   <div style="text-align: center;">
     <video style="width: 70%; max-width: 1000px;" controls autoplay loop muted>
       <source src="_static/Media1.mp4" type="video/mp4">
       Your browser does not support the video tag.
     </video>
   </div>

List of tools
-------------

* :doc:`CSV workflow <csv_workflow>`. A set of scripts that greatly streamline and 
  facilitate the CAD to MCNP process.

  * :doc:`Prepare CAD <csv_workflow/prepare_cad>`. Prepares the CAD model for the 
    workflow. It makes all the components independent of each other and assigns a to 
    each a unique ID.
  * :doc:`CSV generator <csv_workflow/csv_generator>`. Generates or updates the CSV file
    that contains all the information of the model as read by SpaceClaim.
  * :doc:`Detec volumes to adjust <csv_workflow/detect_volumes_to_adjust>`. Highlights 
    the components that exceed the maximum volume deviation after simplification.
  * :doc:`Adjust volume <csv_workflow/adjust_volume>`. Automatically extrudes the
    selected faces of a component to match the original volume of the component.
  * :doc:`Show by material <csv_workflow/show_by_material>`. Display only the components
    made of a selected list of materials.
  * :doc:`Save STEP <csv_workflow/save_step>`. Saves the CAD model as a STEP file
    in a way that the MCNP cell IDs will match the order of the CAD components.
  * :doc:`MCNP materials from CSV <csv_workflow/mcnp_materials_from_csv>`. Updates the
    MCNP file with the materials, densities, density correction factors and component 
    names from the CSV file.

* :doc:`CAD to MCNP comparison <cad_to_mcnp_comparison>`. This tool compares the 
  geometry of a CAD file in SpaceClaim with the geometry of the MCNP input file 
  generated from it. It can be used to check that the geometry in the CAD file is
  correctly translated to the MCNP input file.

* :doc:`Miscellaneous <miscellaneous>`. Set of one-off scripts that perform an 
  independent task.

  * :doc:`Detect torus <miscellaneous/detect_torus>`. Highlights all the bodies that 
    contain a toroidal surface.
  * :doc:`FMESH tally generator <miscellaneous/fmesh_tally_generator>`. Generates a 
    FMESH tally card for MCNP from an arbitrarily sized and place SpaceClaim prismatic 
    body.
  * :doc:`Load CSV points <miscellaneous/load_csv_points>`. Generates a set of points 
    in SpaceClaim from a CSV file. Synergizes with F4Enix lost particles features.
  * :doc:`Simplify toroidal profiles`. Simplifies the toroidal profile of a body 
    substituing the curves of its section with straight lines with a given angle between
    them.

* :doc:`Elbow to cylinder <elbow_to_cylinder>`. Converts the toroidal elbows typically
  found in pipes in a set of cylinders.

* :doc:`Legacy`. Set of scripts that are either obsolete or outdated but may be useful
  in an future update.

  * :doc:`Report generation <legacy/report_generation>`. Automatically generates a 
    report with images and information of each component.
  * :doc:`Piping from CSV`. Generates a set of pipes from information read from a CSV 
    file. 

.. note::

   This project is under active development.


.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Contents:
   
   csv_workflow
   csv_workflow/prepare_cad
   csv_workflow/csv_generator
   cad_to_mcnp_comparison