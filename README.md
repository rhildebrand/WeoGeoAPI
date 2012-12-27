![WeoGeoLogo](http://www.weogeo.com/files/data/www/Logo.png)

# WeoGeoAPI

* Version 0.0.1
* November 18, 2012
* Created by WeoGeo
* Original: [http://www.weogeo.com/developer_doc/WeoGeo_API_Wrappers_Python.html](http://www.weogeo.com/developer_doc/WeoGeo_API_Wrappers_Python.html)
* License: MIT

The Python WeoGeoAPI is a wrapper that allows users access to the functionality of the [WeoGeo API](http://www.weogeo.com/developer_doc/API.html) from within Python. The code is split into two Python files: the main file, WeoGeoAPI.py, and an optional support file, weoXML.py, which enables WeoGeoAPI.py to return weoXML objects if requested. Other than these two files, WeoGeoAPI.py uses only standard Python packages and is made available by importing into any Python project.

Making WeoGeoAPI.py, and optionally weoXML.py, accessible to a python project is as simple as making sure that the python files are in the search path of the current Python project. This is most easily done by having them in the same directory as other Python source files used for the project. There is also the option adding any arbitrary location, where the WeoGeoAPI.py file presumably resides, to the Python search path by adding it to the ‘sys.path’ list from the standard python module ‘sys’.

User of the [Python Package Index](http://pypi.python.org/pypi) may simply type the following into their terminal windows:

	pip install WeoGeoAPI
	
Check out the [getting started](https://github.com/WeoGeo/WeoGeoAPI/tree/master/examples/getting_started) code samples to see how to find, get information, order and download data from WeoGeo.  Documentation is available on the [WeoGeo Support page](http://www.weogeo.com/developer_doc/WeoGeo_API_Wrappers_Python.html) and questions can be asked on the [WeoGeo Contact page](http://www.weogeo.com/contact.html).
