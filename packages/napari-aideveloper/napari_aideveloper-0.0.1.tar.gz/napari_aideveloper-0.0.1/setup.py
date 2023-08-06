#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools 

setuptools.setup(
      packages=setuptools.find_namespace_packages(
                     include=["napari_aideveloper", "napari_aideveloper.*"], ),
                 include_package_data=True
                 )