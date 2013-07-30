import xml.dom.minidom
import codecs

# the weoXML obejct
class weoXML(object):
    # reads xml from a file or from a string.
    def __init__(self, xmlIn = None):
        if xmlIn == None:
            self.doc  = None
            self.root = None
        elif isinstance(xmlIn, file):
            self.doc = xml.dom.minidom.parse(xmlIn)
            self.root = self.doc.documentElement
        elif isinstance(xmlIn, str):
            self.doc = xml.dom.minidom.parseString(xmlIn)
            self.root = self.doc.documentElement
        return

    def __str__(self):
        return self.root.toxml(encoding='UTF-8')

    # clone the whole document
    def clone(self):
        tempObject = weoXML(str(self))
        return tempObject

    # loads an xml document from a string
    def loadXMLString(self, xmlIn):
        if self.doc is not None:
            self.clear()
        self.doc  = xml.dom.minidom.parseString(xmlIn)
        self.root = self.doc.documentElement
        return True

    # loads an xml document form a file
    def loadXMLFile(self, xmlFileIn):
        if self.doc is not None:
            self.clear()
        self.doc  = xml.dom.minidom.parse(xmlFileIn)
        self.root = self.doc.documentElement
        return True

    # saves the document to a file
    def saveXML(self, outPath):
        if self.doc is not None:
	    try:
                fout = codecs.open(outPath, mode = 'w', encoding = 'utf-8')
                self.doc.writexml(fout)
                fout.close()
                return True
	    except:
		return False
        else:
            return False
    def save(self, outPath):
        return self.saveXML(outPath)

    # finds the first node whose name matches the tag provided. useful when looking for unique tags. will not return multiple tags with the same name
    def _findFirstTag(self, tag, inode = None):
        sections = tag.split('/', 1)
        for node in inode.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                if node.nodeName == sections[0]:
                    if len(sections) == 1:
                        return node
                    else:
                        return self._findFirstTag(sections[1], node)
        return None

    # finds all nodes whose name matches the given tag. the return object is a list of nodes
    def _findAllTags(self, tag, inode, targetNodes):
        sections = tag.split('/', 1)
        partialNodes = []
        for node in inode.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                if node.nodeName == sections[0]:
                    if len(sections) == 1:
                        targetNodes.append(node)
                    else:
                        partialNodes.append(node)

        for pnode in partialNodes:
            self._findAllTags(sections[1], pnode, targetNodes)
        return True

    # completely removes a tag and all its children
    def _removeTagObject(self, tag):
        parent = tag.parentNode
        removed = parent.removeChild(tag)
        removed.unlink()
        return True

    # completely removes a tag and all its children
    def _extractTagObject(self, tag):
        parent = tag.parentNode
        removed = parent.removeChild(tag)
        return tag

    # returns the contents of a tag object. only makes sense if the tag is of type TEXT_NODE
    def _getTagObjectContent(self, tag):
        numberOfChildNodes = len(tag.childNodes)
        if numberOfChildNodes == 0:
            return ''
        elif numberOfChildNodes == 1:
            return str(tag.firstChild.data)
        else:
            for node in tag.childNodes:
                if node.nodeType == node.CDATA_SECTION_NODE:
                    return str(node.data)
        return ''

    # returns the contents of a tag object. only makes sense if the tag is of type TEXT_NODE
    def _getTagObjectContentUnicode(self, tag):
        numberOfChildNodes = len(tag.childNodes)
        if numberOfChildNodes == 0:
            return ''
        elif numberOfChildNodes == 1:
            return unicode(tag.firstChild.data)
        else:
            for node in tag.childNodes:
                if node.nodeType == node.CDATA_SECTION_NODE:
                    return unicode(node.data)
        return ''

    # returns the value of the given attributeName in the node object or empty string if the attribute given does not exist
    def _getTagObjectAttribute(self, node, attributeName):
        if node.attributes.has_key(attributeName) == True:
            return node.attributes[attributeName].value
        else:
            return ''

    # sets the content of the given tag object. only makes sense for TEXT_NODE tags
    def _setTagObjectContent(self, tag, content):
        for node in tag.childNodes:
            if node.nodeType == node.TEXT_NODE:
                node.data = content
                return True
        tag.appendChild(self.doc.createTextNode(content))
        return True

    # sets the content of the given tag object. only makes sense for CDATA_SECTION_NODE tags
    def _setTagObjectCDATAContent(self, tag, content):
        for node in tag.childNodes:
            if node.nodeType == node.CDATA_SECTION_NODE:
                node.data = content
                return True
        tag.appendChild(self.doc.createCDATASection(content))
        return True

    # sets the content of the given tag object. only makes sense for TEXT_NODE tags
    def _setTagObjectAttribute(self, tag, attributeName, attributeValue):
        if tag.attributes.has_key(attributeName) == True:
            tag.attributes[attributeName].value = attributeValue
            return True
        return False

    # makes a new attribute for the give tag object
    def _createAttributeToObject(self, tag, attributeName, attributeValue):
        newAttribute = self.doc.createAttribute(attributeName)
        newAttribute.value = attributeValue
        tag.setAttributeNode(newAttribute)
        return True

    # preprocesses a tag string to make sure it is fit to be used
    def _preprocessTag(self, tag):
        if tag.endswith('/'):
            tag = tag[:-1]
        if tag[0] == '/':
            tag = tag[1:]
        return tag

    # returns the tag of a document
    def getRootTag(self):
        return self.root

    # returns the first node that matches the name of the tag provided
    def getFirstTag(self, tag, inode = None):
        if inode is None:
            inode = self.root
        tag = self._preprocessTag(tag)
        return self._findFirstTag(tag, inode)

    # returns a list of nodes that match the name of the tag provided
    def getAllTags(self, tag, inode = None):
        if inode is None:
            inode = self.root
        tag = self._preprocessTag(tag)
        tagsFound = []
        self._findAllTags(tag, inode, tagsFound)
        if len(tagsFound) == 0:
            return []
        else:
            return tagsFound

    # clears the xml document object 
    def clear(self):
        if self.doc is not None:
            self.doc.unlink()
        self.root = None
        return

    # completely removes the first tag that matches name "tag" and all its children
    def removeTag(self, tag):
        targetTag = self.getFirstTag(tag)
        if targetTag != None:
            return self._removeTagObject(targetTag)
        return False

    # completely removes all the tags that match the name "tag" and all their children
    def removeAllTags(self, tag):
        targetTags = self.getAllTags(tag)
        for aTag in targetTags:
            self._removeTagObject(aTag)
        return True

    # extracts a tag and all its children from the document and returns it
    def extractTag(self, tag):
        targetTag = self.getFirstTag(tag)
        if targetTag != None:
            return self._extractTagObject(targetTag)
        return None
        
    # returns the contents of a tag by tag name. only makes sense if the tag is of type TEXT_NODE
    def getTagContent(self, tag):
        targetTag = self.getFirstTag(tag)
        if targetTag != None:
            return self._getTagObjectContent(targetTag)
        return ''

    # returns the contents of a tag by tag name. only makes sense if the tag is of type TEXT_NODE
    def getTagContentUnicode(self, tag):
        targetTag = self.getFirstTag(tag)
        if targetTag != None:
            return self._getTagObjectContentUnicode(targetTag)
        return ''

    # returns the contents of all tags that match the name "tag". only makes sense for tags of type TEXT_NODE
    def getTagsContent(self, tag):
        targetTagsContents = []
        targetTags = self.getAllTags(tag)
        for aTag in targetTags:
            targetTagsContents.append(self._getTagObjectContent(aTag))
        return targetTagsContents

    # returns the contents of all tags that match the name "tag". only makes sense for tags of type TEXT_NODE
    def getTagsContentUnicode(self, tag):
        targetTagsContents = []
        targetTags = self.getAllTags(tag)
        for aTag in targetTags:
            targetTagsContents.append(self._getTagObjectContentUnicode(aTag))
        return targetTagsContents

    # returns the value of the given attributeName in the tag by name "tag" or the empty string if the attribute given does not exist
    def getTagAttribute(self, tag, attributeName):
        if tag is not None:
            targetTag = self.getFirstTag(tag)
        else:
            targetTag = self.root
        if targetTag != None:
            return self._getTagObjectAttribute(targetTag, attributeName)
        else:
            return ''

    # returns the value of the given attributeName in any tag that matches the name "tag" or the empty string if the attribute given does not exist
    def getTagsAttribute(self, tag, attributeName):
        targetTagsAttributeValue = []
        targetTags = self.getAllTags(tag)
        for aTag in targetTags:
            targetTagsAttributeValue.append(self._getTagObjectAttribute(aTag, attributeName))
        return targetTagsAttributeValue

    # sets the content the first that that matches name "tag"
    def setTagContent(self, tag, content):
        targetTag = self.getFirstTag(tag)
        if targetTag != None:
            return self._setTagObjectContent(targetTag, content)
        return False

    # sets the content the first that that matches name "tag"
    def setTagCDATAContent(self, tag, content):
        targetTag = self.getFirstTag(tag)
        if targetTag != None:
            return self._setTagObjectCDATAContent(targetTag, content)
        return False

    # sets the content the first that that matches name "tag", if tag does not exists then create it
    def setTagContentForcefully(self, tag, content):
        targetTag = self.getFirstTag(tag)
        if targetTag != None:
            return self._setTagObjectContent(targetTag, content)
        else:
            return self.createTag(tag, content)
        return False

    # sets the contents of all tags that match the name "tag" to value "content"
    def setTagsContent(self, tag, content):
        targetTags = self.getAllTags(tag)
        for aTag in targetTags:
            self._setTagObjectContent(aTag, content)
        return True

    # sets the given attribute to "attributeValue" for the first that matches name "tag"
    def setTagAttribute(self, tag, attributeName, attributeValue):
        targetTag = self.getFirstTag(tag)
        if targetTag != None:
            return self._setTagObjectAttribute(targetTag, attributeName, attributeValue)
        return False

    # sets the given attribute to "attributeValue" for all tags that matches name "tag"
    def setTagsAttribute(self, tag, attributeName, attributeValue):
        targetTags = self.getAllTags(tag)
        for aTag in targetTags:
            self._setTagObjectAttribute(aTag, attributeName, attributeValue)
        return True

    # makes a new attribute for the first tag that matches name "tag"
    def createAttributeToTag(self, tag, attributeName, attributeValue):
        targetTag = self.getFirstTag(tag)
        if targetTag != None:
            return self._createAttributeToObject(targetTag, attributeName, attributeValue)
        return False

    # makes a new attribute for all the tags that match name "tag"
    def createAttributeToTags(self, tag, attributeName, attributeValue):
        targetTags = self.getAllTags(tag)
        for aTag in targetTags:
            self._createAttributeToObject(aTag, attributeName, attributeValue)
        return True

    # creates a new tag with name "tag" and value "content"
    def createTag(self, tag, content = None):
        tagDepth    = 0
        node        = self.root
        tagSections = self._preprocessTag(tag).split('/')
        tagSecNum   = len(tagSections)
        for tagSection in tagSections:
            temp = self.getFirstTag(tagSection, node)
            if temp == None:
                break
            tagDepth += 1
            node = temp
        if tagDepth < tagSecNum:
            while tagDepth < tagSecNum:
                newNode = self.doc.createElement(tagSections[tagDepth])
                node.appendChild(newNode)
                node = newNode
                tagDepth += 1
            if content is not None:
                node.appendChild(self.doc.createTextNode(content))
        else:
            newNode = self.doc.createElement(tagSections[-1])
            if content is not None:
                newNode.appendChild(self.doc.createTextNode(content))
            node.parentNode.insertBefore(newNode, None)
        return newNode

    # make a new document and return that object
    @staticmethod
    def makeNewDocument(newRoot):
        newWeoXml = weoXML()
        newWeoXml.doc = xml.dom.minidom.DOMImplementation().createDocument(None, newRoot, None)
        newWeoXml.root = newWeoXml.doc.documentElement
        return newWeoXml
