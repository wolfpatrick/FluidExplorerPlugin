import xml.etree.ElementTree as xml

class XmlFileWriter:

    path = ""
    elementName = ""

    projectName = ""
    numberOfSamppes = ""

    def __init__(self):
        pass

    def setXmlDocPath(self, path, elementName):
        self.path = path
        self.elementName = elementName

    def addElement_ProjectName(self, value):
        self.projectName = value

    def addElement_NumberOfSamples(self, value):
        self.numberOfSamppes = value

    #
    # This method writes the properties in the xml file
    #
    def writeValuesInFile(self):
        # Add root
        #root = xml.Element("ProjectSettings")
        appt = xml.Element(self.elementName)
        #root.append(appt)

        # Add children (project settings)
        el_projectName = xml.SubElement(appt, "ProjectName")
        el_projectName.text = self.projectName

        el_samples = xml.SubElement(appt, "Samples")
        el_samples.text = self.numberOfSamppes

        # Create file
        tree = xml.ElementTree(appt)
        try:
            with open(self.path, "w") as fh:
                tree.write(fh)
                return True
        except:
            return False

