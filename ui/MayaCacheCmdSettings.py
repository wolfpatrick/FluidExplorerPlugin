_author__ = 'Patrick'

class MayaCacheCmdSettings(object):

    def __init__(self):
        self._outputPath = ""
        self._numberSamples = 128
        self._prjName = ""
        self._cam_perspective = False
        self._cam_viewcube = False
        self._cam_sphere = False
        self._cam_rotation = 0

    @property
    def outputPath(self):
        return self._outputPath

    @outputPath.setter
    def outputPath(self, value):
        self._outputPath = value

    @property
    def numberSamples(self):
        return self._numberSamples

    @numberSamples.setter
    def numberSamples(self, value):
        self._numberSamples = value

    @property
    def prjName(self):
        return self._prjName

    @prjName.setter
    def prjName(self, value):
        self._prjName = value

    @property
    def cam_perspective(self):
        return self._cam_perspective

    @cam_perspective.setter
    def cam_perspective(self, value):
        self._cam_perspective = value

    @property
    def cam_viewcube(self):
        return self._cam_viewcube

    @cam_viewcube.setter
    def cam_viewcube(self, value):
        self._cam_viewcube = value

    @property
    def cam_sphere(self):
        return self._cam_sphere

    @cam_sphere.setter
    def cam_sphere(self, value):
        self._cam_sphere = value

    @property
    def cam_rotation(self):
        return self._cam_rotation

    @cam_rotation.setter
    def cam_rotation(self, value):
        self._cam_rotation = value

    @staticmethod
    def printValues(valuesGeneral):
        print "-- General Parameters  --"

        print "\tNum. Samples: " + str(valuesGeneral.numberSamples)
        print "\tOutput Path : " + str(valuesGeneral.outputPath)
        print "\tProj. Name  : " + str(valuesGeneral.prjName)

        print "\tCamera Perspective : " + str(valuesGeneral.cam_perspective)
        print "\tCamera ViewCube    : " + str(valuesGeneral.cam_viewcube)
        print "\tCamera Sphere      : " + str(valuesGeneral.cam_sphere)
        print "\tCamera Rotation    : " + str(valuesGeneral.cam_rotation)