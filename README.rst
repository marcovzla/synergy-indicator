=================
synergy-indicator
=================

An indicator for ubuntu, useful for starting and stopping
``synergys`` with different configurations.

configurations
--------------

You can store configuration files with extension ``.conf`` in the
``~/.synergy-indicator`` directory and they will be available in the
Profiles submenu.

installation
------------

To make a deb package run::

  $ dpkg-deb --build synergy-indicator

To install run::

 $ dpkg -i ./synergy-indicator.deb
