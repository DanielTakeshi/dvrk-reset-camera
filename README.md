# Camera Correction

This will help us reset the camera if (when) people adjust it by mistake or
deliberately. Here are the steps:


## When Starting Out

- First, get an appropriately rigid setup, where we have something like this:

  ![setup](setup/setup.JPG?raw=true)

  The base should not be foamy, since otherwise the location of the things we
  measure can change even if the camera stays constant.

- Second, record images by running `scripts/record.py`. This will record
  starting images and pop them up.  Since this is the 'ground truth' camera
  position, we record precise positions of the two corners of the grid we have,
  top left and bottom right.  Repeatedly adjust the coordinates by changing
  values in `autolab/data_collector.py` until we see that the pop-ups are
  showing the boundary set up correctly.


## Correcting for Adjusting Camera

Suppose we now have egregiously messed up with the camera and need to
re-position it. Here's what to do.

- Again, run `record.py`. This will again pop up the images. However, this time,
  instead of adjusting the *data collector values*, you repeatedly adjust the
  cameras so that they match the fixed reference images (both left and right).
