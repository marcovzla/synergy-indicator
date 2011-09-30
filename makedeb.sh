#!/bin/bash
dpkg-deb --build debian
echo 'Renaming debian.deb -> synergy-indicator_0.1-1_all.deb'
mv debian.deb synergy-indicator_0.1-1_all.deb
