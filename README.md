![WeoGeoLogo](http://www.weogeo.com/files/data/www/Logo.png)

# WeoGeoAPI

* Version 3.0.0
* August 21, 2014
* Created by WeoGeo
* Original: [http://www.weogeo.com/developer_doc/WeoGeo_API_Wrappers_Python.html](http://www.weogeo.com/developer_doc/WeoGeo_API_Wrappers_Python.html)
* License: MIT

## Introduction ##
The Python WeoGeoAPI is a wrapper that allows users access to the functionality of the [WeoGeo API](/developer_doc/API.html) from within Python. The core API functionality is contained in the main source file, WeoGeoAPI.py. A secondary, and optional, support file called weoXML.py is also provided. Its purpose is to ease working with XML formatted content. Other than these two files, the Python API uses only standard Python packages and is made ready to use in any Python project by simply importing the main source file.

Making WeoGeoAPI.py, and optionally weoXML.py, accessible to a Python project is as simple as making sure that the Python files are in the search path of the current Python project. This is most easily done by having them in the same directory as other Python source files used for the project. There is also the option adding any arbitrary location, where the WeoGeoAPI.py file presumably resides, to the Python search path by adding it to the ‘sys.path’ list from the standard Python module ‘sys’.

## WeoGeoAPI.py basics ##
The WeoGeoAPI module contains two main classes: weoSession and weoJob. The weoSession class is used to interact with the WeoGeo website, get dataset information, and create jobs. The weoJob class abstracts all the details of making a WeoGeo job into an easy to use object that, after being set up through the use of its method, is cleanly passed to the appropriate weoSession method to create and order a job. 

To start using the WeoGeoAPI module, an instance of the weoSession class must be created. The weoSession object takes three parameters: the URL address of the WeoGeo target, the username of the person accessing it, and the password that matches the username. After being instantiated, the [connect](#connect) method must be called to validate the provided parameters and to establish a connection to WeoGeo. Once connected to WeoGeo, all the methods of the weoSession object are made available to use.

__Example:__

    >>> import WeoGeoAPI
    >>> weos = WeoGeoAPI.weoSession( 'market.weogeo.com', 'username', 'password' )
    >>> weos.connect()
    >>> print weos
    Host:      https://market.weogeo.com
    Username:  user@domain.com
    Password:  ************
    Status:    Good

### Job basics ###
Jobs are created and customized using methods from the weoSession and weoJob classes. Methods of the weoSession class are used to create and order jobs, while methods of the weoJob class are used to set the attributes and customizable options of a job.

To set up a WeoGeo job, an instance of the weoJob class must be created with the desired parameters. The job instance encapsulates all of the attributes and spatial customizations of an order. Important attributes include: output format, output coordinate system, desired layers, etc. Attributes can be assigned with the constructor when the object is made, or after construction with the weoJob method, [setParameters](#setparameters-parameters-). Spatial customizations are set separately using [weoJob customization methods](#weojob-methods).

##### Example 1: Set parameters in the constructor #####
    >>> newJob = WeoGeoAPI.weoJob( datasetToken = 'bfc2b36e-3d0d-4a6d-935d-e9ab090aaa3c',
                                   layers = ['Area Hydrography', 'Linear Hydrography'],
                                   outputFormat = 'SHAPE',
                                   note = 'Extract of area around Portland, OR.',
                                   acceptLicense = True )

##### Example 2: Create an empty instance, then use setParameters to set job parameters #####
    >>> newJob = WeoGeoAPI.weoJob()
    >>> newJob.setParameters( datasetToken = 'bfc2b36e-3d0d-4a6d-935d-e9ab090aaa3c',
                              layers = ['Area Hydrography', 'Linear Hydrography'],
                              outputFormat = 'SHAPE', 
                              note = 'Extract of area around Portland, OR.',
                              acceptLicense = True )

Once the job instance and the parameters and customizations of the job have been set, the weoSession method, [createJob](#createjob--createjobraw-newjob-rtype--formatsjson-) must be called to create the job record. The job record will contain the job information, including the job token, which is used for ordering and retrieving information about the job.

### Regular methods and raw methods ###
Most of the methods of the weoSession object have two variations: 

1. Method names that end with the suffix 'Raw.' These methods, referred to a 'Raw' methods, always return the response of the WeoGeo website as a standard Python string object.
2. Method names that __do not__ end with the suffix 'Raw.' These methods, referred to as regular methods, will return a python object, the type of which will depend on the desired format of the request (see [Request Types](#request-types)). Normally these objects will be either standard Python JSON objects, or weoXML objects.

It is typically easier to work with Python objects returned by the regular methods since they have their own methods to handle the data. However, the raw methods are provided for those users who wish to parse the output themselves to create their own custom objects. The distinction between these two series of methods is shown below. Theses examples assume that we already have a valid weoSession object.

__Raw__ [orderJobsInCart](#orderjobsincart--orderjobsincartraw-rtype--formatsjson-) method: the variable 'results' will contain a Python string.

    >>>response, results = weos.orderJobsInCartRaw('JSON')
    >>>print results
    {'status': 'Success', 'purchase_number': 'o1017848', 'jobs': [], 'job_transaction_id': None, 
    'purchaser': {'username': 'user@domain.com', 'rating': None, 'votes': 0, 'id': 3065}, 
    'created_at': '2013/02/05 20:41:24 +0000', 'purchased_at': '2013/02/05 20:41:24 +0000', 
    'updated_at': '2013/02/05 20:41:24 +0000', 'token': '99b17abc-25b6-4e4b-83ba-a1340b19d490'}

__Regular__ [orderJobsInCart](#orderjobsincart--orderjobsincartraw-rtype--formatsjson-) method: the variable 'results' will contain a Python dict object.

    >>>response, results = weos.orderJobsInCart('JSON')
    >>>print results
    {u'status': u'Success', u'purchase_number': u'o1017848', u'jobs': [], u'job_transaction_id': None, 
    u'purchaser': {u'username': u'user@domain.com', u'rating': None, u'votes': 0, u'id': 3065}, 
    u'created_at': u'2013/02/05 20:41:24 +0000', u'purchased_at': u'2013/02/05 20:41:24 +0000', 
    u'updated_at': u'2013/02/05 20:41:24 +0000', u'token': u'99b17abc-25b6-4e4b-83ba-a1340b19d490'}

### Request types ###
Most of the methods of the weoSession object take a request type variable. The request type controls the format of the response from the website, in the case that a response exists. Both the raw methods and the regular methods accept request types.

The request type is set by using the special 'formats' class of the WeoGeoAPI module. The formats class defines easy names for common formats such as JSON and XML. Different methods accept different request types. Most methods only support two request types: formats.XML and formats.JSON. A limited number of methods support an additional request type: formats.WEO. The formats.WEO request type is an XML variant. We recommend using the JSON request type, which is the default request type for most methods. When providing a return type parameter to a method, it may be defined using the 'WeoGeoAPI.format name directly, such as formats.JSON or formats.XML; or alternatively, it can be defined using the common string representation of those names, for example the strings 'JSON' or 'XML'.

The following example explicitly requests the response in JSON format.

    >>> response, results = weos.getDataset( '3a3d32d5-b11a-4623-b42c-966b34c716ad', 'JSON' )
    >>> print results
    {u'hosted': True, u'layers': [u'RailroadLines', u'RailroadStations'], u'market': u'Complete', u'name': 
    u'CTARailroadNetwork-NorthAmerica', u'permalink': u'open-cta-railroad-network-north-america', u'status': 
    u'Approved'}
    
The same request, now requested in XML format.

    >>> response, results = weos.getDataset( '3a3d32d5-b11a-4623-b42c-966b34c716ad', 'XML' )
    >>> print results
    <?xml version="1.0" encoding="UTF-8"?>
    <dataset>
      <hosted type="boolean">true</hosted>
        <layers type="array">
          <layer>Railroad Lines</layer>
          <layer>Railroad Stations</layer>
        </layers>
      <market>Complete</market>
      <name>CTA Railroad Network - North America</name>
      <permalink>open-cta-railroad-network-north-america</permalink>
      <status>Approved</status>
    </dataset>

### Return type ###
Every method that returns a response from the WeoGeo website always returns a standard Python tuple of size two where the first element of the tuple is always the HTTP status code of the response and the second element in the tuple is the content, or body, of the response (see the response and results variables in the [example above](#request-types)). The HTTP code and the body of the response may be used to diagnose problems with the API call performed. This structure will be referred to as __website response__ in the full API documentation below.

---

## Python API Documentation ##
Below is the full API documentation for the weoSession object and the weoJob object. Only methods that directly interface with the WeoGeo API are included.

---

### Connection Methods ###
The following methods deal directly with setting up the weoSession object and establishing a connection with the WeoGeo website.

---

#### weoSession( host, username, password ) ####
The only constructor for the weoSession class. This method is required to connect to the WeoGeo website.

[REST API Equivalent](/developer_doc/API.html#authentication)

##### Inputs: #####
+ __host:__ URL of the WeoGeo target. If no protocol is included it defaults to HTTPS, if a protocol is included then that protocol is used, even if it results in error.
+ __username:__ username(email address) of the user that is establishing the connection.
+ __password:__ password that matches the username above.

##### Returns: #####
A new instance of a weoSession object.

##### Example: #####

    >>> weos = WeoGeoAPI.weoSession('market.weogeo.com', 'username', 'password')
    >>> print weos
    Host:      https://market.weogeo.com
    Username:  user@domain.com
    Password:  **********
    Status:    Good

---

#### clear() ####
Completely clears the weoSession object from any supplied credentials. After this method is called the weoSession object must be repopulated with a host, a username, and a password, and the connect method must be called.

[REST API Equivalent](/developer_doc/API.html#authentication)

##### Inputs: #####
None.

##### Returns: #####
The instanced object itself.

##### Example: #####

    >>> weos = WeoGeoAPI.weoSession( 'market.weogeo.com', 'username', 'password' )
    >>> print weos
    Host:      https://market.weogeo.com
    Username:  user@domain.com
    Password:  **********
    Status:    Good
    >>> weos.clear()
    >>> print weos
    Host:      None
    Username:  None
    Password:  None
    Status:    Disconnected

----

#### connect() ####
Attempts to connect the WeoGeo website using the given username and password supplied from the weoSession object.

[REST API Equivalent](/developer_doc/API.html#authentication)

##### Inputs: #####
None.

##### Returns: #####
`True` if the connection was established. `False` if the connection was not established.

##### Example: #####

    >>> weos = WeoGeoAPI.weoSession( 'market.weogeo.com', 'username', 'password' )
    >>> weos.connect()
    True

----

### Dataset Methods ###
The following methods deals with obtaining information about existing dataset listings.

---

#### getDataset | getDatasetRaw( datasetToken, rtype = formats.JSON ) ####
Retrieves listing information for a single data listing.

[REST API Equivalent](/developer_doc/Datasets_API.html#get-dataset)

##### Inputs: #####
+ __datasetToken:__ token which represents the dataset being requested.
+ __rtype:__ the format of the response by the website. Default is JSON. Only accepts formats.WEO and formats.JSON.

##### Returns: #####

Website response. The body of the request will contain the record of the dataset requested.

##### Example: #####

    >>> response, record = weos.getDataset( '2323d6f5-12cf-4160-adb6-961da747e351', 'JSON' )
    >>> print response    
    200
    >>> print record
    {u'preview_layer_api_url': u'https://market.weogeo.com/datasets/open-ports
    -and-ferries-of-the-united-states/preview_layers.json', u'rating': 0.0, u'suppor
    ted_customizations': {u'layer': True, u'file_format': True, u'projection_datum':
    True, u'geocrop': True, u'any': True, u'spatial_resolution': False}...

----

#### getDatasets | getDatasetsRaw( rtype = formats.JSON, \*filters ) ####
Retrieves the records of multiple datasets from WeoGeo.

[REST API Equivalent](/developer_doc/Datasets_API.html#list-datasets)

##### Inputs: #####
+ __rtype:__ the format of the response by the website. Default is JSON. Only accepts formats.JSON or formats.XML.
+ __filters:__ a string that specifies a filter that will limit the result to only records matching that filter. For example, the string `"data_type=raster"`.

##### Returns: #####

Website response. The body of the response will contain the records of all the datasets that match the given filter, if any.

##### Example: #####

    >>> response, records = weos.getDatasets( 'JSON', 'data_type=vector', 'north=45.39', 'south=45.21', 'east=-122.27', 'west=-122.46' )
    >>> print response
    200
    >>> print records
    {u'number_of_lines': u'10000', u'number_of_samples': u'10000', u'w
    est': -180.0, u'line_pixel_size': u'-0.0052609400', u'sample_pixel_size': u'0.01
    13045260', u'proj4': u'+proj=latlong +datum=WGS84', u'projection_datum': u'geo-w
    gs84', u'north': 71.48254, u'east': -66.95474, u'south': 18.87314}, u'preview':
    {u'projection_datum': u'Unknown-UNKNOWN'}, u'geo': {u'number_of_lines': u'5967',
    u'north': 71.48254, u'west': -180.0, u'line_pixel_size': u'-0.0088167397', u'sa
    mple_pixel_size': u'0.0088167397', u'proj4': u'+proj=longlat +ellps=WGS84 +datum
    =WGS84 +no_defs ', u'projection_datum': u'geo-wgs84', u'number_of_samples': u'12
    822', u'east': -66.9517636054, u'south': 18.8730542282}... 

----

### Job Methods ###

These methods handle job creation and ordering. Before creating a job, job attributes must be defined in weoJob instances. For more information on how to set job attributes, see [Job Basics](#job-basics).

----

#### createJob | createJobRaw( newJob, rtype = formats.JSON ) ####
Creates a new job record. Does not submit the order, just creates the job record.

[REST API Equivalent](/developer_doc/Jobs_API.html#create-a-job)

##### Inputs: #####
+ __newJob:__ a weoJob instance 
+ __rtype:__ the format of the response by the website. Default is JSON. Only accepts formats.JSON or formats.XML.

##### Returns: #####

Website response. The body of the response will contain the record of the new job in the requested format.

##### Example: #####

    >>> response, results = weos.createJob( newJob, 'JSON' )
    >>> print response
    200
    >>> print results
    {u'layers': [u'10m High Res'], u'status': u'Not Processed', u'api_url': 
    u'https://market.weogeo.com/jobs/ab39f7cc-9826-4b9b-8c07-9b0f66680133.json', 
    u'parameters': {u'job_geocrop': u'Clip', u'job_file_format': u'Native', u'job_geometry':
    u'{"type":"Feature","crs":{"type":"name","properties":{"name":"EPSG:4326"}},"geometry":
    {"type":"Polygon","coordinates":[[[-124.33000000000,46.17000000000],[-116.28000000000,46.17000000000],
    [-116.28000000000,42.13000000000],[-124.33000000000,42.13000000000],[-124.33000000000,46.17000000000]]]}}', 
    u'job_token': u'ab39f7cc-9826-4b9b-8c07-9b0f66680133', u'job_datum_projection': u'EPSG:4269', 
    u'dataset_hostname': u'open.weogeo.com', u'job_layers': u'10m High Res', u'dataset_token': 
    u'5dbdb7db-1acf-4f19-b629-04b54f907552', u'job_spatial_resolution': u'1'}...

----

#### getDownloadFile | getDownloadFileRaw( jobToken, rtype = formats.JSON ) ####
Gets download information, including the download URL of a completed job.

[REST API Equivalent](/developer_doc/Jobs_API.html#download-the-files-for-a-job)

##### Inputs: #####
+ __jobToken:__ the token of the job record of interest.
+ __rtype:__ the format of the response by the website. Default is JSON. Only accepts formats.JSON or formats.XML.

##### Returns: #####
Website response. The body of the response will contain the contents of the job.

##### Example: #####
    response, result = weos.getDownloadFile( '69add159-01fa-4d84-8b83-f34692f582ec', 'JSON' )
    >>> print response
    200
    >>> print result
    [{u'name': u'weogeo_69add159-01fa-4d84-8b83-f34692f582ec.zip', u'split_group': 
    u'a47fd4a2-9826-47ac-a7d5-ca5272a7e28b', u'url': u'https://s3.amazonaws.com/
    weojobs.weogeo.com/69add159-01fa-4d84-8b83-f34692f582ec/weogeo_69add159-01fa-4d84-8b83-f34692f582ec.zip?
    AWSAccessKeyId=AKIAIVL2HF3II6R24MYA&Expires=1360788207&Signature=k%2b98N8Ag0EuPfOwtG4AsobVhbzg%3d', 
    u'created_at': u'2013/02/05 20:47:55 +0000', u'job_id': 25006, u'updated_at': u'2013/02/05 20:47:55 +0000', 
    u'compression_method': u'', u'split': False, u'id': 10212, u'md5': u'099f0d1643da46b10c1b32ec59a39635'}]

----

#### getJob | getJobRaw( jobToken, rtype = formats.JSON ) ####
Retrieves the record of a created job.

[REST API Equivalent](/developer_doc/Jobs_API.html#view-job-details)

##### Inputs: #####
+ __jobToken:__ the token of the job being requested.
+ __rtype:__ the format of the response by the website. Default is JSON. Only accepts formats.JSON or formats.XML.

##### Returns: #####
Website response. The body of the response will contain the record of the job requested.

##### Example: #####
    response, result = weos.getJob( 'd1a03a07-c780-4682-9c49-1e33f9af6a8f', 'JSON')
    >>> print response
    200
    >>> print result
    {u'layers': None, u'status': u'In Cart', u'events_api_url': u'https://market.weogeo.com/jobs/d1a03a07-
    c780-4682-9c49-1e33f9af6a8f/events.json', u'order_url': u'https://market.weogeo.com/jobs/order_cart?
    id=d1a03a07-c780-4682-9c49-1e33f9af6a8f', u'job_edit_page_url': u'https://market.weogeo.com/datasets/
    open_gns_world_waterbodies?job_id=d1a03a07-c780-4682-9c49-1e33f9af6a8f', u'api_url': u'https://
    market.weogeo.com/jobs/d1a03a07-c780-4682-9c49-1e33f9af6a8f.json', u'parameters': {u'job_geometry': None, 
    u'job_token': u'd1a03a07-c780-4682-9c49-1e33f9af6a8f', u'dataset_token': u'9dc42e34-cbd0-6952-ad6c-
    fb39eb23fd0a', u'dataset_hostname': u'open.weogeo.com'}...

----

#### getJobsInCart | getJobsInCartRaw( rtype = formats.JSON ) ####
Retrieves the records of all the jobs that are currently in the user's cart.

[REST API Equivalent](/developer_doc/Jobs_API.html#list-jobs-in-the-users-shopping-cart)

##### Inputs: #####
+ __rtype:__ the format of the response by the website. Default is JSON. Only accepts formats.JSON or formats.XML.

##### Returns: #####
Website response. The body of the response will contain all the jobs in the user's cart. 

##### Example: #####
    >>> response, results = weos.getJobInCart( 'JSON' )
    >>> print response
    200
    >>> print results
    {u'display_total': u'$0.00', u'total': 0.0, u'jobs': [{u'api_url': u'https://market.weogeo.com/jobs/
    e733e78c-1c37-4f50-98f2-8ca8603e5d93.json', u'price': 0.0, u'dataset': {u'token': u'9dc42e34-cbd0-6952-ad6c-
    fb39eb23fd0a', u'page_url': u'https://market.weogeo.com/datasets/open_gns_world_waterbodies', u'name': u'GNS 
    World Waterbodies', u'api_url': u'https://market.weogeo.com/datasets/open_gns_world_waterbodies.json'}, 
    u'note': None, u'token': u'e733e78c-1c37-4f50-98f2-8ca8603e5d93', u'job_edit_url': u'https://
    market.weogeo.com/datasets/open_gns_world_waterbodies?job_id=e733e78c-1c37-4f50-98f2-8ca8603e5d93'}, 
    {u'api_url': u'https://market.weogeo.com/jobs/0df47a1d-60bc-4e54-8b51-c15000c29d99.json', u'price': 0.0, 
    u'dataset': {u'token': u'5dbdb7db-1acf-4f19-b629-04b54f907552', u'page_url': u'https://market.weogeo.com/
    datasets/open-natural-earth-shaded-relief', u'name': u'Natural Earth Shaded Relief', u'api_url': u'https://
    market.weogeo.com/datasets/open-natural-earth-shaded-relief.json'}, u'note': u'Extract of area around 
    Oregon.', u'token': u'0df47a1d-60bc-4e54-8b51-c15000c29d99', u'job_edit_url': u'https://market.weogeo.com/
    datasets/open-natural-earth-shaded-relief?job_id=0df47a1d-60bc-4e54-8b51-c15000c29d99'}]}

----

#### getPrice | getPriceRaw( jobToken ) ####
Retrieves the price, estimated size, and other attributes for a job. 

[REST API Equivalent](/developer_doc/Jobs_API.html#get-the-price-for-an-order)

##### Inputs: #####
+ __jobToken:__ the job token

##### Returns: #####
Website response. The body retrieves order information of the job.

##### Example: #####
    >>>response, results = weos.getPrice( 'e733e78c-1c37-4f50-98f2-8ca8603e5d93' )
    >>>print response
    200
    >>>print results
    {u'estimated_data_size': 54228, u'price': u'$0.00', u'no_data': False, u'too_much_data': False, 
    u'requires_offline_fulfillment': False, u'human_estimated_data_size': u'53 KB'}
    
----

#### moveJobToCart( jobToken ) ####
Moves a previously created job that is not in the shopping cart into the shopping cart. If the job is already in the cart then nothing happens.

[REST API Equivalent](/developer_doc/Jobs_API.html#list-jobs-in-the-users-shopping-cart)

##### Inputs: #####
+ __jobToken:__ token that references the job to be moved into the cart.

##### Returns: #####
Website response. The body of the response will be empty on success.

##### Example: #####
    >>>response, results = weos.moveJobToCart( 'e733e78c-1c37-4f50-98f2-8ca8603e5d93' )
    >>>print response
    204
    >>>print results
    ''
    
----

#### removeJobFromCart( jobToken ) ####
Removes a previously created job from the shopping cart. If the job is not in the cart then nothing happens.

[REST API Equivalent](/developer_doc/Jobs_API.html#delete-a-job)

##### Inputs: #####
+ __jobToken:__ token that references the job to be removed from the cart.

##### Returns: #####
Website response. The body of the response will be empty on success.

##### Example: #####
    >>>response, results = weos.removeJobFromCart( 'e733e78c-1c37-4f50-98f2-8ca8603e5d93' )
    >>>print response
    204
    >>>print results
    ''
    
----

#### orderJob | orderJobRaw( jobToken, rtype = formats.JSON ) ####
Submits an order for a previously created job.

[REST API Equivalent](/developer_doc/Jobs_API.html#order-a-job-not-in-a-cart)

##### Inputs: #####
+ __jobToken:__ token of the job record being ordered for processing.
+ __rtype:__ the format of the response by the website. Default is JSON. Only accepts formats.JSON or formats.XML.

##### Returns: #####
Website response. The body of the response will contain the details of the purchase.

##### Example: #####
    >>> response, results = weos.orderJob( 'e733e78c-1c37-4f50-98f2-8ca8603e5d93', 'JSON')
    >>> print response
    200
    >>> print results
    {u'status': u'Success', u'purchase_number': u'o1017832', u'jobs': [{u'events_api_url': 
    u'https://market.weogeo.com/jobs/27d7adec-5e95-45c3-9aca-1d41c724681d/events.json', u'api_url': u'https://
    market.weogeo.com/jobs/27d7adec-5e95-45c3-9aca-1d41c724681d.json', u'token': 
    u'27d7adec-5e95-45c3-9aca-1d41c724681d', u'events_api_url_template': u'https://market.weogeo.com/
    jobs/27d7adec-5e95-45c3-9aca-1d41c724681d/events/${id}.json', u'total': 0.0, u'job_edit_page_url': 
    u'https://market.weogeo.com/datasets/open_gns_world_waterbodies?
    job_id=27d7adec-5e95-45c3-9aca-1d41c724681d'}], u'job_transaction_id': None, u'purchaser': {u'username': 
    u'user@domain.com', u'rating': None, u'votes': 0, u'id': 3065}, u'created_at': u'2013/02/05 18:16:31 +0000', 
    u'purchased_at': u'2013/02/05 18:16:31 +0000', u'updated_at': u'2013/02/05 18:16:31 +0000', u'token': 
    u'c7ed6cc3-4e32-4edd-b60a-58de1719797f'}

----

#### orderJobsInCart | orderJobsInCartRaw( rtype = formats.JSON ) ####
Submits an order for all the jobs in the user's cart.

[REST API Equivalent](/developer_doc/Jobs_API.html#order-the-users-shopping-cart)

##### Inputs: #####
+ __rtype:__ the format of the response by the website. Default is JSON. Only accepts formats.JSON or formats.XML.

##### Returns: #####
Website response. The body of the response will contain the details of the purchase.

##### Example: #####
    >>> response, results = weos.orderJobsInCart( 'JSON')
    >>> print response
    200
    >>> print results
    {u'status': u'Success', u'purchase_number': u'o1017848', u'jobs': [], u'job_transaction_id': None, 
    u'purchaser': {u'username': u'user@domain.com', u'rating': None, u'votes': 0, u'id': 3065}, u'created_at': 
    u'2013/02/05 20:41:24 +0000', u'purchased_at': u'2013/02/05 20:41:24 +0000', u'updated_at': u'2013/02/05 
    20:41:24 +0000', u'token': u'99b17abc-25b6-4e4b-83ba-a1340b19d490'})

----

### weoJob Methods ###
These are the methods of the weoJob class. [Job instances](#job-basics) must be created before these methods can be used.

----

#### setParameters( \*\*parameters ) ####
Set parameters for job instance. Parameters that can be used are specific to the dataset. Not all parameters can be used on all datasets.

[REST API Equivalent](/developer_doc/Jobs_API.html#create-a-job)

##### Inputs: #####
+ __inCart__ = True/False                  
+ __acceptLicense__ = True/False                  
+ __datasetToken__ = token of the listing being ordered
+ __cropAction__ = 'On'/'Off' - This is enabled by default. Specify as 'Off' if you want the full geometry of the dataset
+ __note__ = an arbitrary string. Used for any arbitrary purpose
+ __coordinateSystem__ = used to reproject data from source. Uses an EPSG code such 'EPSG:4269' (LatLong/NAD83).
+ __layers__ = list, tuple, or semicolon separated string of layer names. At least one must be specified. Must exactly match the listing's layer names.
+ __spatialResolution__ = for raster data only - this represents the desired quality of the raster with '1' being original (and thus best) detail, and '4' being about 16 times less detailed. (example values: '1', '2', '3', or '4')
+ __outputFormat__ = typical options for vector: SHAPE, CSV, ACAD, FFS, GML, IEPS, OGC, KML, MITAB. Typical options for raster: ENVIHDR, ERDAS, GEOTIFF, JPEG.

##### Returns: #####
Nothing.

##### Example: #####
    >>> newJob.setParameters( datasetToken = 'bfc2b36e-3d0d-4a6d-935d-e9ab090aaa3c',
                              layers = ['Area Hydrography', 'Linear Hydrography'],
                              outputFormat = 'SHAPE', 
                              cropAction = 'Off',
                              coordinateSystem = 'EPSG:4269',
                              note = 'Oregon Hydrography data.',
                              acceptLicense = True )
                            
----

#### setClipAreaCoordinates( newCYCS ) ####
Set the coordinate system when using the [addClipAreaPoints](#addclipareapoints-listofpoints-) method. 

[REST API Equivalent](/developer_doc/Jobs_API.html#the-geometry-parameter)

##### Inputs: #####
+ __newCYCS:__ the coordinate system of the polygon used to define the area of interest of the job. The only acceptable values are 'EPSG:4326', or WeoGeoAPI.weoJob.GEO, for the LatLong/WGS84 coordinate system; or 'EPSG:3857', or constant WeoGeoAPI.weoJob.SMERC, for the Spherical Mercator coordinate system.

##### Returns: #####
Nothing.

##### Example: #####
    >>> newJob.setClipAreaCoordinateSystem( 'EPSG:3857' )
    or
    >>> newJob.setClipAreaCoordinateSystem( newJob.GEO )
    or
    >>> newJob.setClipAreaCoordinateSystem( WeoGEOAPI.weoJob.SMERC )
    >>> newJob.addClipAreaPoints( [(-13953999.90, 6414019.90), (-12846538.81,6414019.90), (-13953999.90,2782346.66)] )
   
----

#### addClipAreaPoints( listOfPoints ) ####
Add a list of X,Y points to create a custom polygon selection area. Requires at least 3 points. Points are used in sequence and line segments cannot intersect. Coordinate system of the points must be set by [setClipAreaCoordinates](#setclipareacoordinates-newcycs-).

[REST API Equivalent](/developer_doc/Jobs_API.html#the-geometry-parameter)

##### Inputs: #####
+ __points:__ a list of X,Y tuples or lists where X and Y are coordinates

##### Returns: #####
Nothing.

##### Example: #####
    >>> newJob.addClipAreaPoints( [(-122.55,45.43), (-122.46,45.43), (-122.14,45.32), [-122.14,45.27], (-122.55,45.27)] )    

----

#### setBoxCropArea( coordinateSystem, north, south, east, west ) ####
Creates a bounding box using north, south, east, and west of the area desired for a job instance.

[REST API Equivalent](/developer_doc/Jobs_API.html#the-geometry-parameter)

##### Inputs: #####
+ __coordinateSystem:__ the coordinate system of the polygon used to define the area of interest of the job. The only acceptable values are 'EPSG:4326', or WeoGeoAPI.weoJob.GEO, for the LatLong/WGS84 coordinate system; or 'EPSG:3857', or constant WeoGeoAPI.weoJob.SMERC, for the Spherical Mercator coordinate system.
+ __north:__ float value of northernmost coordinate in the projection used
+ __south:__ float value of southernmost coordinate in the projection used
+ __east:__ float value of easternmost coordinate in the projection used
+ __west:__ float value of westernmost coordinate in the projection used

##### Returns: #####
Nothing.

##### Example: #####
    >>> newjob.setBoxCropArea('EPSG:4326', 46.17, 42.13, -116.28, -124.33)
    
---