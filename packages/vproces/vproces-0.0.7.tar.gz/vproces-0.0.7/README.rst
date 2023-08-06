Example Project
===============
This is an example project that is used to demonstrate how to publish
Python packages on PyPI. 

Installing
============

.. code-block:: bash

    pip install vproces

Usage
=====

.. code-block:: bash

    >>> from vproces.imgproc import vstack
    >>>	img_paths = ['example.png', 'example2.png']
    >>> imgs = [cv2.imread(p) for p in img_paths]

    >>> stacked = vstack(imgs)

    >>> cv2.imshow('stacked', stacked)
    >>> cv2.waitKey(0)
