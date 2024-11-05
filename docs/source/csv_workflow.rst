CSV workflow
============

The so called CSV workflow is a pipeline that streamlines and aids the process 
to convert a CAD model into an MCNP input file. It begins with the simplification of the
CAD in SpaceClaim and ends with the generation and pre-processing of the MCNP input file,
including the automatic assignation of materials, densities, density correction factors
and comments to the MCNP cells.

All the scripts in this workflow are centerd around a CSV file that contains all the
information of the model. This CSV file can be updated automatically via scripts and 
also be modified and filled by the user manually.

Pipeline
--------

1. The CAD model is cleaned by removing the clearly out of place components.
2. The :ref:`Prepare CAD` script is run to generate a new SpaceClaim document where all the components are independent of each other and each has a unique ID.
3. The :ref:`CSV generator` script is run to generate the CSV file.
4. The user performs the simplification of the model in SpaceClaim. During the simplification, the scritps :ref:`Detect volumes to adjust` and :ref:`Adjust volume` can be used to highlight and automatically adjust the components that exceed the maximum volume deviation.
5. The user fills in the CSV file with information regarding the materials and densities of the components. The Excel filtering features can be very beneficial in the manipulation and filling of the CSV. The script :ref:`Show by material` is very useful to study in SpaceClaim the material distribution among the components.
6. The :ref:`Save STEP` script is run to save the CAD model as a STEP file in a way that the MCNP cell IDs will match the order of the CAD components.
7. The conversion of the previous STEP file to an MCNP input file is performed with another tool like GEOUNED.
8. The :ref:`MCNP materials from CSV` script is run to update the MCNP file with the materials, densities, density correction factors and component names from the CSV file.

Prepare CAD
-----------

This script is run in SpaceClaim and doesn't require any input from the user.
It prepares the CAD model for the workflow. It makes all the components 
independent of each other. Repeated instances of the same component (e.g. a bolt) will
become unique. In addition, all the bodies of a component will be assigned to a new 
component one level deeper in the assembly hierarchy, the component name will have the 
form **ComponentX** where **X** is a number, a unique identifier.

.. image:: _static/prepare_cad_hierarchy.png
   :alt: Effect of the prepare_cad script on the assembly hierarchy.
   :align: center
   :width: 95%

.. attention::

    This script is meant to be run only once. Running this script is a necessary step 
    to later run the :ref:`CSV generator` script.

.. tip::

    It is recommended to *clean* the model before running this script to remove the 
    clearly wrong or out of place components. This will avoid deleting a lot of components
    later and therefore have a lot of jumps between the component identifiers (the
    **X** in **ComponentX**). 

.. warning::

    By making all the components independent of each other, it may become more difficult
    to apply the same changes to all the instances of a component that appears many times.
    The use of the **Power Selection** features in SpaceClaim can greatly mitigate this
    tradeoff. 

CSV generator
-------------

This script is run in SpaceClaim and doesn't require any input from the user. The first
time it is executed, it generates a new CSV file with the same name as the CAD file and 
located in the same folder. The CSV file will contain information read from the model.  

.. image:: _static/csv_completed.png
   :alt: Example of a filled CSV file.
   :align: center
   :width: 95%

* The columns **Level X** show the component hierarchy.
* **Component ID** show the unique identifier of the component.
* **MATERIAL** shows the name of the component's material (initially empty).
* **MASS [g]** shows the mass of the component (initially empty).
* **DENSITY [g/cm3]** shows the density of the material's component (initially empty).
* **CELL IDs** shows the range of the MCNP cell IDs that will be assigned to the component. More than one indicates multiple bodies in the CAD component.
* **DENSITY CORRECTION FACTOR** shows the density correction factor that will be applied to the density of the material's component (initially empty).
* **ORIGINAL VOLUME [cm3]** shows the volume of the component at the time of the first CSV generation.
* **%dif (ORG-SIM)/ORG*100** shows the percentage difference between the original volume and the current volume (initially empty).
* **SIMPLIFIED VOLUME** shows the current volume of the component (initially empty).
* **STOCHASTIC VOLUME** shows the volume of the component as calculated with an MPNC simulation (initially empty).
* **DCF=ORG/STOCH** shows the density correction factor (if any) to be applied (initially empty).
* **COMMENT** shows any comments that the user wants to add to the component (initially empty).

When the script is executed for the first time, only the **Level X**, **Component ID**, **CELL IDs** and **ORIGINAL VOLUME[cm3]** will be automatically filled.
In subsequent runs of the script the **SIMPLIFIED VOLUME** column will be update as well as the **Level X** columns.
The rest of the columns are meant to be filled by the user, possibly with the help of Excel features.

After running the script for the first time the user may delete components in SpaceClaim,
they will still appear in the CSV file but with a *DELETED* keyword appearing in the 
**CELL IDs** column. The user may also add new components to the model, but they should 
follow the same naming convention of **ComponentX**. Components can be reorderd in the 
hierarchy as long as the Component ID is maintained. It is possible to manually edit values
that are suposed to be automatically filled like the original volume (e.g. it is decided
a posteriori that the correct volume of a component is different).

This CSV will be used in all the other scripts of the workflow proving to be a very 
valuable asset during the development of a MCNP model.

.. attention::

    Before running this script the CAD shoudl have been prepared with the
    :ref:`Prepare CAD` script.

.. warning::

    To run the script for a second time or more, the CSV file should be present in the 
    same folder as the CAD and have the same name. The script will overwrite the CSV
    file and therefore the CSV file should not be open in any other program like Excel.

Detect volumes to adjust
-----------------------

asdfasdf 

Adjust volume
-------------

sdf

Show by material
----------------

asdf

Save STEP
---------

asdf

MCNP materials from CSV
-----------------------

vvvvs

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



