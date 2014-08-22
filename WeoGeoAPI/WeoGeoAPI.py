"""
Copyright (C) 2011-2014 by Trimble Navigation Ltd

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

REPORTING BUGS
    Report bugs to <support@weogeo.com>.

PURPOSE:
A simple python wrapper around the WeoGeo API.
"""
import os
import httplib
import base64
try:
    import json
except ImportError:
    import simplejson as json

try:
    import weoXML
    _DEFINE_USING_WEOXML = True
except ImportError:
    _DEFINE_USING_WEOXML = False

#formats_object###################################################################################################################
class formats(object):
    JSON = 0
    XML  = 1
    WEO  = 2
    KML  = 3
    PDF  = 4
    CSV  = 5

    def __init__(self, newFormat):
        if isinstance(newFormat, formats) == True:
            self.type = newFormat.type
        elif isinstance(newFormat, int) == True:
            if newFormat < self.JSON or newFormat > self.CSV:
                raise Exception('Format error: format "' + str(newFormat) + '" is not supported.')
            self.type = newFormat
        elif isinstance(newFormat, str) == True:
            newFormat_lower = newFormat.lower()
            if newFormat_lower == 'json':
                self.type = self.JSON
            elif newFormat_lower == 'xml':
                self.type = self.XML
            elif newFormat_lower == 'weo':
                self.type = self.WEO
            elif newFormat_lower == 'kml':
                self.type = self.KML
            elif newFormat_lower == 'pdf':
                self.type = self.PDF
            elif newFormat_lower == 'csv':
                self.type = self.CSV
            else:
                raise Exception('Format error: format "' + str(newFormat) + '" is not supported.')
        else:
            raise Exception('Formats error: can not initialize object with parameter provided. Incompatible type.')
        return

    def __str__(self):
        if self.type == self.JSON:
            local = 'json'
        elif self.type == self.XML:
            local = 'xml'
        elif self.type == self.WEO:
            local = 'weo'
        elif self.type == self.KML:
            local = 'kml'
        elif self.type == self.PDF:
            local = 'pdf'
        elif self.type == self.CSV:
            local = 'csv'
        else:
            raise Exception('Format error: format "' + str(self.type) + '" not supported.')
        return local

    def __eq__(self, other):
        if isinstance(other, formats) == True:
            if self.type == other.type:
                return True
            else:
                return False
        elif isinstance(other, int) == True:
            if self.type == other:
                return True
            else:
                return False
        elif isinstance(other, str) == True:
            other_lower = other.lower()
            if self.type == self.JSON and other_lower == 'json':
                return True
            elif self.type == self.XML and other_lower == 'xml':
                return True
            elif self.type == self.WEO and other_lower == 'weo':
                return True
            elif self.type == self.KML and other_lower == 'kml':
                return True
            elif self.type == self.PDF and other_lower == 'pdf':
                return True
            elif self.type == self.CSV and other_lower == 'csv':
                return True
            else:
                return False
        else:
            raise Exception('Cannot compare a "format" object against the type provided.')

    def __ne__(self, other):
        return not self == other
#format_object_end###############################################################################################################

#job_object######################################################################################################################
class weoJob(object):
    # valid coordinate system constants
    COORDSYS = {0:'EPSG:4326', 1:'EPSG:3857'}
    GEO = 0
    SMERC = 1

    def __init__(self, **parameters):
        self.geometryPoints = []
        self.clipCSYS = 'EPSG:4326'
        self.content = dict()
        self.content['job'] = dict()
        self.content['job']['parameters'] = dict()
        self.setConfigurationOptions(**parameters)
        return 

    def setConfigurationOptions(self, **parameters):
        for param in parameters:
            self.content['job'][param.lower()] = parameters[param]
        return

    def setParameterOptions(self, **parameters):
        for param in parameters:
            self.content['job']['parameters'][param.lower()] = parameters[param]
        return

    def setBoxCropArea(self, proj, north, south, east, west):
        self.geometryPoints[:] = []
        self.setClipAreaCoordinateSystem(proj)
        geometryString = '{\"type\":\"Feature\",\"crs\":{\"type\":\"name\",\"properties\":{\"name\":\"%s\"}},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[%.11f,%.11f],[%.11f,%.11f],[%.11f,%.11f],[%.11f,%.11f],[%.11f,%.11f]]]}}'
        geometryString = geometryString % (self.clipCSYS, float(west), float(north), float(east), float(north), float(east), float(south), float(west), float(south), float(west), float(north))
        self.content['job']['geometry'] = geometryString
        return 

    def _addClipAreaPoint(self, x, y):
        x = float(x)
        y = float(y)
        self.geometryPoints.append('[%.11f,%.11f]'%(x,y))
        return 

    def addClipAreaPoints(self, points):
        for apoint in points:
            if (isinstance(apoint, tuple) is not True and isinstance(apoint, list) is not True) or len(apoint) != 2:
                raise Exception('Points must be tuples or list of length two')
            self._addClipAreaPoint(apoint[0], apoint[1])
        return

    def setClipAreaCoordinateSystem(self, newCSYS):
        if isinstance(newCSYS, str) is True:
            self.clipCSYS = newCSYS
        elif isinstance(newCSYS, int) is True:
            try:
                self.clipCSYS = self.COORDSYS[newCSYS]
            except:
                raise Exception('Invalid coordinate system entered')
        else:
            raise Exception('Invalid coordinate system entered')
        return 

    def getContent(self):
        if len(self.geometryPoints) > 0:
            points = ','.join(self.geometryPoints)
            geometryString = '{\"type\":\"Feature\",\"crs\":{\"type\":\"name\",\"properties\":{\"name\":\"%s\"}},\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[%s]]}}'
            geometryString = geometryString % (self.clipCSYS, points)
            self.content['job']['geometry'] = geometryString
        return self.content

    def toXML(self, exDict = None):
        if exDict is None:
            tContent = self.getContent()
        else:
            tContent = exDict

        request = ['<job>']
        for akey in tContent['job']:
            if akey != 'parameters':
                request.append('<%s>%s</%s>' % (akey, tContent['job'][akey], akey))
        request.append('<parameters>')
        for akey in tContent['job']['parameters']:
            request.append('<%s>%s</%s>' % (akey, tContent['job']['parameters'][akey], akey))
        request.append('</parameters>')
        request.append('</job>')
        return ''.join(request)

    def __str__(self):
        tContent = self.getContent()
        return json.dumps(tContent, indent = 4)
#job_object_end##################################################################################################################

#weo_Server_Response#############################################################################################################
class weoServerResponse():
    def __init__(self, classicResponse):
        self.status = classicResponse.status
        self.__rawContent = None
        self.content = classicResponse.read()
        self.reason = classicResponse.reason
        self.version = classicResponse.version
        self.msg = classicResponse.msg
        # make the headers easier to access
        rawHeaders = classicResponse.getheaders()
        self.headers = dict()
        for aheader in rawHeaders:
            self.headers[aheader[0]] = aheader[-1]
        return

    def __str__(self):
        tostr = 'Status: %d\nHeaders: %s\nContent: %s\nVersion: %s'
        return tostr % (self.status, self.headers, self.content, self.version)
#weo_Server_Response_end#########################################################################################################

#HTTP_controller#################################################################################################################
class httpController(object):
    def __init__(self, sslenabled = False):
        if sslenabled is False:
            self.WEOConnection = httplib.HTTPConnection
        else:
            self.WEOConnection = httplib.HTTPSConnection
        return

    def getGTLD(self, string):
        sepOne = string.find('.')
        if sepOne != -1:
            sepTwo = string[sepOne+1:].find('.')
            if sepTwo != -1:
                sepl = string[sepOne+sepTwo+1:].find('/')
                if sepl != -1:
                    return string[sepOne+sepTwo+2:sepOne+sepTwo+1+sepl]
                else:
                    return string[sepOne+sepTwo+2:]
            else:
                return ''
        else:
            return ''

    def success(self, code):
        if code >= 200 and code <= 206:
            return True
        else:
            return False
     
    def getRequestType(self, string):
        sep = string.rfind('.')
        if sep == -1:
            return 'application/xml'
        else:
            rtype = string[sep+1:].lower()
            if rtype == 'weo' or rtype == 'kml' or rtype == 'xml':
                return 'application/xml'
            elif rtype == 'jpe' or rtype == 'jpeg' or rtype == 'jpg':
                return 'image/jpeg'
            elif rtype == 'png':
                return 'image/png'
            else:
                return 'application/' + str(rtype)
     
    def normalizeDomain(self, string):
        if string.startswith('http://'):
            string = string[7:]
        elif string.startswith('https://'):
            string = string[8:]
            
        if string.endswith('/'):
            return string[:-1]
        else:
            return string
     
    def normalizePath(self, string):
        if len(string) == 0:
            return ''
        elif string[0] != '/':
            return '/' + string
        else:
            return string    
     
    def Get(self, domain, path, username, password):
        path = self.normalizePath(path)
        requestType = self.getRequestType(path)
        credentials = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
     
        headers = dict()
        headers['Content-Type']  = requestType
        headers['Authorization'] = 'Basic %s' % credentials
     
        connection = self.WEOConnection(self.normalizeDomain(domain))
        connection.request('GET', path, None, headers)
        response = weoServerResponse(connection.getresponse())
        connection.close()
        return response

    def Post(self, domain, path, username, password, content):
        path = self.normalizePath(path)
        requestType = self.getRequestType(path)
        credentials = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
     
        headers = dict()
        headers['Content-Type']  = requestType
        headers['Authorization'] = 'Basic %s' % credentials
     
        connection = self.WEOConnection(self.normalizeDomain(domain))
        connection.request('POST', path, content, headers)
        response = weoServerResponse(connection.getresponse())
        connection.close()
        return response

    def PostSession(self, domain, content):
        path = self.normalizePath('session.json')
        requestType = self.getRequestType(path)

        headers = dict()
        headers['Content-Type']  = requestType
     
        connection = self.WEOConnection(self.normalizeDomain(domain))
        connection.request('POST', path, content, headers)
        response = weoServerResponse(connection.getresponse())
        connection.close()
        return response
     
    def Put(self, domain, path, username, password, content):
        path = self.normalizePath(path)
        requestType = self.getRequestType(path)
        credentials = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
     
        headers = dict()
        headers['Content-Type']  = requestType
        headers['Authorization'] = 'Basic %s' % credentials

        connection = self.WEOConnection(self.normalizeDomain(domain))
        connection.request('PUT', path, content, headers)
        response = weoServerResponse(connection.getresponse())
        connection.close()
        return response

    def Put_http(self, domain, path, username, password, content, *inHeaders):
        path = self.normalizePath(path)
        requestType = self.getRequestType(path)
        credentials = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
     
        headers = dict()
        headers['Content-Type']  = requestType
        headers['Authorization'] = 'Basic %s' % credentials
        for aheader in inHeaders:
            sects = aheader.split(':')
            headers[sects[0].strip()] = sects[1].strip()

        connection = httplib.HTTPConnection(self.normalizeDomain(domain))
        connection.request('PUT', path, content, headers)
        response = weoServerResponse(connection.getresponse())
        connection.close()
        return response

    def MultiPost(self, domain, path, username, password, content, contentType):
        path = self.normalizePath(path)
        requestType = self.getRequestType(path)
        credentials = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
     
        headers = dict()
        headers['Content-Type']  = contentType
        headers['Authorization'] = 'Basic %s' % credentials
        headers['Content-Length'] = str(len(content))
     
        connection = self.WEOConnection(self.normalizeDomain(domain))
        connection.request('POST', path, content, headers)
        response = weoServerResponse(connection.getresponse())
        connection.close()
        return response

    def Delete(self, domain, path, username, password, content = ''):
        path = self.normalizePath(path)
        requestType = self.getRequestType(path)
        credentials = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
     
        headers = dict()
        headers['Content-Type']  = requestType
        headers['Authorization'] = 'Basic %s' % credentials
     
        connection = self.WEOConnection(self.normalizeDomain(domain))
        connection.request('DELETE', path, content, headers)
        response = weoServerResponse(connection.getresponse())
        connection.close()
        return response
#HTTP_controller_end#############################################################################################################

#weo_session#####################################################################################################################
class weoSession(object):
    def __init__(self, newHostname, newUsername, newPassword = ''):
        self.setHostname(newHostname)
        self.username  = newUsername
        self.password  = newPassword
        self.connected = False
        self.market    = False
        self.errorMsg  = None
        return

    #_connection_functions#############################
    def setHostname(self, newHostname):
        self.hostname = newHostname.strip()
        if self.hostname.startswith('https://') == True:
            self.httpC = httpController(True)
            self.strippedHostname = self.hostname[8:]
        elif self.hostname.startswith('http://') == True:
            self.httpC = httpController(False)
            self.strippedHostname = self.hostname[7:]
        else:
            self.hostname = 'https://' + self.hostname
            self.httpC = httpController(True)
            self.strippedHostname = self.hostname[8:]
        self.connected = False
        return
    
    def setUsername(self, newUsername):
        self.username = newUsername
        self.connected = False
        return

    def setPassword(self, newPassword):
        self.password = newPassword
        self.connected = False
        return

    def setAPIKey(self, apiKey):
        self.username = apiKey
        self.password = ''
        self.connected = False
        return

    def clear(self):
        self.username  = None
        self.password  = None
        self.hostname  = None
        self.connected = False
        return self

    def connect(self):
        if self.hostname == None:
            raise Exception('Session error: please provide a host address.')
        if self.username == None:
            raise Exception('Session error: please provide a username.')
        if self.password == None:
            raise Exception('Session error: please provide a password.')

        content = '{ "user" : { "username" : "%s", "password" : "%s"}}' % (self.username, self.password)
        response = self.httpC.PostSession(self.hostname, content)
        self.connected = self.httpC.success(response.status)
        if self.connected == False:
            self.errorMsg = response.content
        return self.connected
    #_connection_functions_end#########################

    #_utility_functions################################
    def printable(self, showPassword = False):
        i  = 'Host:      ' + str(self.hostname)  + '\n'
        i += 'Username:  ' + str(self.username)  + '\n'
        if showPassword is True:
            i += 'Password:  ' + str(self.password)  + '\n'
        else:
            i += 'Password:  ***************\n'
        if self.connected == False:
            i += 'Status:    ' + 'Disconnected'
        else:
            i += 'Status:    ' + ('Good' if self.market == False else 'Probably Good\n')
        return i

    def __str__(self):
        return self.printable()

    if _DEFINE_USING_WEOXML == True:
        def _parseOutput(self, rtype, output):
            if rtype is None:
                return output
            rtype = formats(rtype)
            if len(output.strip()) == 0:
                pOutput = output
            elif rtype == 'xml' or rtype == 'weo' or rtype == 'kml':
                pOutput = weoXML.weoXML(output)
            elif rtype == 'json':
                pOutput = json.loads(output)
            else:
                pOutput = output
            return pOutput
    else:
        def _parseOutput(self, rtype, output):
            if rtype is None:
                return output
            rtype = formats(rtype)
            if len(output.strip()) == 0:
                pOutput = output
            elif rtype == 'xml' or rtype == 'weo' or rtype == 'kml':
                pOutput = output
            elif rtype == 'json':
                pOutput = json.loads(output)
            else:
                pOutput = output
            return pOutput
    #_utility_functions_end_############################

    #_tile_server_functions_###################################################################################################
    def getTileSubscriptionsRaw(self, rtype = formats.JSON, clientID = None):
        if self.connected == False:
            raise Exception('Session error: session not connected. Call function "weoSession.connect()" before any API call.')
        rtype = formats(rtype)
        if clientID is None:
            path = 'tile_subscriptions.' + str(rtype)
        else:
            path = 'tile_subscriptions.' + str(rtype) + '?client_id=' + str(clientID)
        return self.httpC.Get(self.hostname, path, self.username, self.password)

    def getTileSubscriptions(self, rtype = formats.JSON, clientID = None):
        rtype = formats(rtype)
        response = self.getTileSubscriptionsRaw(rtype, clientID)
        if self.httpC.success(response.status) == True:
            response.__rawContent = response.content
            response.content = self._parseOutput(rtype, response.content)
        return response
    #_tile_server_functions_end_###############################################################################################

    #_dataset_api_calls_#######################################################################################################
    def getDatasetRaw(self, token, rtype = formats.JSON):
        if self.connected == False:
            raise Exception('Session error: session not connected. Call function "weoSession.connect()" before any API call.')
        rtype = formats(rtype)
        path = 'datasets/' + token + '.' + str(rtype)
        return self.httpC.Get(self.hostname, path, self.username, self.password)

    def getDataset(self, token, rtype = formats.JSON):
        rtype = formats(rtype)
        response = self.getDatasetRaw(token, rtype)
        if self.httpC.success(response.status) == True:
            response.__rawContent = response.content
            response.content = self._parseOutput(rtype, response.content)
        return response

    def getDatasetsRaw(self, rtype = formats.JSON, *filters):
        if self.connected == False:
            raise Exception('Session error: session not connected. Call function "weoSession.connect()" before any API call.')
        rtype = formats(rtype)
        dFilter = ''
        if len(filters) > 0:
            dFilter = '?'
            for f in filters:
                dFilter += f + '&'
            dFilter = dFilter.rstrip('&')
        path = 'datasets.' + str(rtype) + dFilter
        return self.httpC.Get(self.hostname, path, self.username, self.password)

    def getDatasets(self, rtype = formats.JSON, *filters):
        rtype = formats(rtype)
        response = self.getDatasetsRaw(rtype, *filters)
        if self.httpC.success(response.status) == True:
            response.__rawContent = response.content
            response.content = self._parseOutput(rtype, response.content)
        return response
    #_dataset_api_call_end_######################################################################################################

    #_job_api_calls_#############################################################################################################
    def getJobRaw(self, token, rtype = formats.JSON):
        if self.connected == False:
            raise Exception('Session error: session not connected. Call function "weoSession.connect()" before any API call.')
        rtype = formats(rtype)
        path = 'jobs/' + token + '.' + str(rtype)
        return self.httpC.Get(self.hostname, path, self.username, self.password)

    def getJob(self, token, rtype = formats.JSON):
        rtype = formats(rtype)
        response = self.getJobRaw(token, rtype)
        if self.httpC.success(response.status) == True:
            response.__rawContent = response.content
            response.content = self._parseOutput(rtype, response.content)
        return response
     
    def getJobsRaw(self, rtype = formats.JSON, *filters):
        if self.connected == False:
            raise Exception('Session error: session not connected. Call function "weoSession.connect()" before any API call.')
        rtype = formats(rtype)
        jFilter = ''
        if len(filters) > 0:
            jFilter = '?'
            for f in filters:
                jFilter += f + '&'
            jFilter = jFilter.rstrip('&')
        path = 'jobs.' + str(rtype) + jFilter
        return self.httpC.Get(self.hostname, path, self.username, self.password)

    def getJobs(self, rtype = formats.JSON, *filters):
        rtype = formats(rtype)
        response = self.getJobsRaw(rtype, *filters)
        if self.httpC.success(response.status) == True:
            response.__rawContent = response.content
            response.content = self._parseOutput(rtype, response.content)
        return response

    def getJobsInCartRaw(self, rtype = formats.JSON):
        if self.connected == False:
            raise Exception('Session error: session not connected. Call function "weoSession.connect()" before any API call.')
        rtype = formats(rtype)
        path = 'jobs/show_cart.' + str(rtype)
        return self.httpC.Get(self.hostname, path, self.username, self.password)

    def getJobsInCart(self, rtype = formats.JSON):
        rtype = formats(rtype)
        response = self.getJobsInCartRaw(rtype)
        if self.httpC.success(response.status) == True:
            response.__rawContent = response.content
            response.content = self._parseOutput(rtype, response.content)
        return response

    def getDownloadFileRaw(self, token, rtype = formats.JSON):
        if self.connected == False:
            raise Exception('Session error: session not connected. Call function "weoSession.connect()" before any API call.')
        rtype = formats(rtype)
        path = 'jobs/' + token + '/download.' + str(rtype)
        return self.httpC.Get(self.hostname, path, self.username, self.password)

    def getDownloadFile(self, token, rtype = formats.JSON):
        rtype = formats(rtype)
        response = self.getDownloadFileRaw(token, rtype)
        if self.httpC.success(response.status) == True:
            response.__rawContent = response.content
            response.content = self._parseOutput(rtype, response.content)
        return response
     
    def createJobRaw(self, content, rtype = formats.JSON):
        if self.connected == False:
            raise Exception('Session error: session not connected. Call function "weoSession.connect()" before any API call.')
        if isinstance(content, weoJob) == True:
            rContent = content.getContent()
        elif isinstance(content, dict) == True:
            rContent = content
        else:
            raise Exception('Type error: the job object is not a job object or a dictionary object')

        rtype = formats(rtype)
        path = 'jobs.' + str(rtype)

        if rtype == 'json':
            request = json.dumps(rContent, encoding='utf-8')
        else:
            if isinstance(content, weoJob) == True:
                request = content.toXML()
            else:
                tJob = weoJob()
                request = tJob.toXML(rContent)

        return self.httpC.Post(self.hostname, path, self.username, self.password, request)

    def createJob(self, content, rtype = formats.JSON):
        rtype = formats(rtype)
        response = self.createJobRaw(content, rtype)
        if self.httpC.success(response.status) == True:
            response.__rawContent = response.content
            response.content = self._parseOutput(rtype, response.content)
        return response

    def updateJobRaw(self, token, jobObject, rtype = formats.JSON):
        if self.connected == False:
            raise Exception('Session error: session not connected. Call function "weoSession.connect()" before any API call.')
        if isinstance(jobObject, weoJob) == True:
            content = jobObject.getContent()
        elif isinstance(jobObject, dict) == True:
            content = content
        else:
            raise Exception('Type error: the job object is not a job object or a dictionary object')

        rtype = formats(rtype)
        path = 'jobs/' + token + '.' + str(rtype)
        if rtype == 'json':
            request = json.dumps(content)
        else:
            if isinstance(jobObject, weoJob) == True:
                request = jobObject.toXML()
            else:
                tJob = weoJob()
                request = tJob.toXML(content)
        return self.httpC.Put(self.hostname, path, self.username, self.password, request)
        
    def updateJob(self, token, jobObject, rtype = formats.JSON):
        rtype = formats(rtype)
        response = self.updateJobRaw(token, jobObject, rtype)
        if self.httpC.success(response.status) == True:
            response.__rawContent = response.content
            response.content = self._parseOutput(rtype, response.content)
        return response

    def orderJobRaw(self, token, rtype = formats.JSON):
        if self.connected == False:
            raise Exception('Session error: session not connected. Call function "weoSession.connect()" before any API call.')
        rtype = formats(rtype)
        path = 'order/job/' + token + '/process.' + str(rtype)
        content = '{"order": {"payment_method_id": null}}'
        return self.httpC.Post(self.hostname, path, self.username, self.password, content)

    def orderJob(self, token, rtype = formats.JSON):
        rtype = formats(rtype)
        response = self.orderJobRaw(token, rtype)
        if self.httpC.success(response.status) == True:
            response.__rawContent = response.content
            response.content = self._parseOutput(rtype, response.content)
        return response

    def orderJobsInCartRaw(self, rtype = formats.JSON):
        if self.connected == False:
            raise Exception('Session error: session not connected. Call function "weoSession.connect()" before any API call.')
        rtype = formats(rtype)
        path = 'order/cart/process.' + str(rtype)
        content = '{"order": {"payment_method_id": null}}'
        return self.httpC.Post(self.hostname, path, self.username, self.password, content)

    def orderJobsInCart(self, rtype = formats.JSON):
        rtype = formats(rtype)
        response = self.orderJobsInCartRaw(rtype)
        if self.httpC.success(response.status) == True:
            response.__rawContent = response.content
            response.content = self._parseOutput(rtype, response.content)
        return response

    def getPriceRaw(self, request):
        if self.connected == False:
            raise Exception('Session error: session not connected. Call function "weoSession.connect()" before any API call.')
        if isinstance(request, weoJob) == True:
            request = request.getContent()
        path = 'jobs/price.json'
        return self.httpC.Post(self.hostname, path, self.username, self.password, json.dumps(request))

    def getPrice(self, request):
        response = self.getPriceRaw(request)
        if self.httpC.success(response.status) == True:
            response.__rawContent = response.content
            response.content = self._parseOutput('JSON', response.content)
        return response

    def moveJobToCart(self, token):
        if self.connected == False:
            raise Exception('Session error: session not connected. Call function "weoSession.connect()" before any API call.')
        content = '<job><cart>1</cart></job>'
        path = 'jobs/' + token + '.xml'
        return self.httpC.Put(self.hostname, path, self.username, self.password, content)

    def removeJobFromCart(self, token):
        if self.connected == False:
            raise Exception('Session error: session not connected. Call function "weoSession.connect()" before any API call.')
        content = '<job><cart>0</cart></job>'
        path = 'jobs/' + token + '.xml'
        response = self.httpC.Put(self.hostname, path, self.username, self.password, content)
        if self.httpC.success(response.status) == True:
            response.__rawContent = response.content
            response.content = self._parseOutput(rtype, response.content)
        return response
    #_job_api_calls_end_#########################################################################################################
#weo_session_end#################################################################################################################
