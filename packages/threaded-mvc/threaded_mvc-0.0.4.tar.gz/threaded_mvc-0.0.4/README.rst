============
threaded_mvc
============


.. image:: https://img.shields.io/pypi/v/threaded_mvc.svg
        :target: https://pypi.python.org/pypi/threaded_mvc

.. image:: https://img.shields.io/travis/Galen-dp/threaded_mvc.svg
        :target: https://travis-ci.com/Galen-dp/threaded_mvc

.. image:: https://readthedocs.org/projects/threaded-mvc/badge/?version=latest
        :target: https://threaded-mvc.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Threaded Model-View-Controller Design Pattern package for GUI & TUI programs.


* Free software: BSD license
* Documentation: https://threaded-mvc.readthedocs.io.

What is this repo or project?
-----------------------------
This is a solution to a common problem with MVC architecture: How do we
keep the View responsive when the model is i/o bound.


How does it work?
-----------------
We do this by placing the model in its own thread, and using message
queues between the Controller and Model.

As per the definition of the MVC design pattern:

1) The model knows nothing about the view or the controller.
2) The view knows nothing about the controller or the model.
3) The controller knows everything about both the model and the view.
4) Contoller  - starts or attaches to view & model
5) model      - signals events to controller which updates view
6) controller - sets model states when necessary.


Who will use this repo or project?
----------------------------------
* TODO


What is the goal of this project?
---------------------------------
* TODO


Features
--------
* TODO


How to install
--------------
* TODO


How to use
----------
* TODO


Credits
-------
This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
