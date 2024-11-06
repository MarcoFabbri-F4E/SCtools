Usage
=====

There are two types of scripts in SCtools: IronPython scripts and CPython scripts. 
IronPython scripts are meant to be imported directly into SpaceClaim. CPython scripts
are meant to be run typically in a command prompt with Python3 installed. This page
explains how to run the scripts in a general way, please refer to the documentation of 
each specific script to understand how to use it. 

IronPython scripts
------------------

These scripts run in SpaceClaim. To import them into SpaceClaim, they
can be simply dragged and dropped into the SpaceClaim window. The script will appear
on a new panel to the right.

.. raw:: html

   <div style="text-align: center;">
     <video style="width: 95%; max-width: 1080px;" controls autoplay loop muted>
       <source src="_static/SpaceClaim_drag_file_and_run.mp4" type="video/mp4">
       Your browser does not support the video tag.
     </video>
   </div>

Drop and run 
~~~~~~~~~~~~

The simplest way to run the script is to drag and drop the file into the SpaceClaim window
and click on the run button. The script will not be saved in the SpaceClaim session, so
this process will need to be repeated everytime the script is needed again. It is 
recommended to run the script in **Run** mode instead of **Debug** mode for increased performance.

1. Drag and drop the script file into the SpaceClaim window.
2. Click on the little arrow attached to the run button and select **Run** instead of **Debug**.
3. Click on the **Run** button.

Publish as a tool
~~~~~~~~~~~~~~~~~

The most convenient way to run IronPython scripts is to publish them as tools. This way,
the script will appear as a new button in the SpaceClaim **Tools** tab. The script will
be saved and can be run anytime in multiple sessions without the need to locate and drop
the file again.

1. Drag and drop the script file into the SpaceClaim window.
2. Click on the little arrow attached to the run button and select **Run** instead of **Debug**.
3. Click on the little arrow atatched to the chain button and select **Publish as tool**.
4. Click on the chain button (this will avoid that the script window opens up again when the script is executed).
5. Fill in the box with a name for the tool and click **OK**.
6. Click again on the chain button and close the script window (click **No**, no need to save the script).

Now the script will be always available:

7. Click on the **Tools** tab.
8. Click on the new button that appears with the name of the tool to execute it.

.. raw:: html

   <div style="text-align: center;">
     <video style="width: 95%; max-width: 1080px;" controls autoplay loop muted>
       <source src="_static/SpaceClaim_publish_as_tool.mp4" type="video/mp4">
       Your browser does not support the video tag.
     </video>
   </div>

Edit the parameter of a published tool
--------------------------------------

Some scripts have default parameters in the form of Python constant variables at the 
top of the file. These parameters can be modified by the user by editing the tool. This
change can be done by simply deleting the tool and publishing it again after applying a 
modification to the file. Alternatively, the tool can be edited directly in SpaceClaim
following these steps:

1. Click on the little arrow below the tool button.
2. Click on **Edit script**, this will open the script panel to the right.
3. Modify the parameters in the script.
4. Click on the chain button (this will avoid that the script window opens up again when the script is executed).
5. Close the script window (click **No**, no need to save the script).

.. raw:: html

   <div style="text-align: center;">
     <video style="width: 95%; max-width: 1080px;" controls autoplay loop muted>
       <source src="_static/SpaceClaim_edit_a_published_tool.mp4" type="video/mp4">
       Your browser does not support the video tag.
     </video>
   </div>

CPython scripts
---------------

These scripts are run in a command prompt with Python3 installed. There is nothing 
inherently special about the way these scripts are executed. If you are unsure on how to run 
Python scripts please refer to the Python documentation or look up a tutorial.

