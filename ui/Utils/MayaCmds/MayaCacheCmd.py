#import maya.cmds as cmds

class MayaCacheCmdString(object):

    def __init__(self):

        self.fluidCacheTimeRange = ""
        self.fluidCacheStartTime = ""
        self.fluidCacheEndTime = ""
        self.fluidCacheDistribMode = ""
        self.fluidRefresh = ""
        self.fluidCacheDirName = ""
        self.fluidCachePerGeometry = ""
        self.fluidCacheName = ""
        self.fluidCacheUsePrefix = ""
        self.fluidCacheAction = ""
        self.fluidCacheForceOverwrite = ""
        self.fluidCacheSimulationRate = ""
        self.fluidCacheSampleMultiplier = ""
        self.fluidCacheInheritModifications = ""
        self.fluidCacheStoreFloats = ""
        self.fluidCacheFormat = ""
        self.fluidCachePBDensity = ""
        self.fluidCachePBVelocity = ""
        self.fluidCachePBTemperature = ""
        self.fluidCachePBFuel = ""
        self.fluidCachePBColor = ""
        self.fluidCachePBTextureCoords = ""
        self.fluidCachePBFalloff = ""

    def setRenderSettingsFromMaya(self, startTime, endTime, cacheDir, chacheName):

        self.fluidCacheTimeRange = "0"
        self.fluidCacheStartTime = str(startTime)
        self.fluidCacheEndTime = str(endTime)

        self.fluidCacheDistribMode = "OneFilePerFrame"
        tmp = cmds.optionVar(q='fluidCacheDistrib')
        if tmp == 2:
            self.fluidCacheDistribMode = "OneFile"

        self.fluidRefresh = cmds.optionVar(q='fluidRefresh')
        self.fluidCacheDirName = cacheDir
        self.fluidCachePerGeometry = "0"
        self.fluidCacheName = chacheName
        self.fluidCacheUsePrefix = cmds.optionVar(q='fluidCacheUsePrefix')
        self.fluidCacheAction = "replace"
        self.fluidCacheForceOverwrite = "1"
        self.fluidCacheSimulationRate = cmds.optionVar(q='fluidCacheSimulationRate')
        self.fluidCacheSampleMultiplier = cmds.optionVar(q='fluidCacheSampleMultiplier')
        self.fluidCacheInheritModifications = cmds.optionVar(q='fluidCacheInheritModifications')
        self.fluidCacheStoreFloats = cmds.optionVar(q='fluidCacheStoreFloats')
        self.fluidCacheFormat = cmds.optionVar(q='fluidCacheFormat')
        self.fluidCacheFormat = 'mcc'
        self.fluidCachePBDensity = cmds.optionVar(q='fluidCachePBDensity')
        self.fluidCachePBVelocity = cmds.optionVar(q='fluidCachePBVelocity')
        self.fluidCachePBTemperature = cmds.optionVar(q='fluidCachePBTemperature')
        self.fluidCachePBFuel = cmds.optionVar(q='fluidCachePBFuel')
        self.fluidCachePBColor = cmds.optionVar(q='fluidCachePBColor')
        self.fluidCachePBTextureCoords = cmds.optionVar(q='fluidCachePBTextureCoords')
        self.fluidCachePBFalloff = cmds.optionVar(q='fluidCachePBFalloff')

    def getCacheCommandString(self):

        command = "doCreateFluidCache 5 { " \
            + "\"" + str(self.fluidCacheTimeRange) + "\", " \
            + "\"" + str(self.fluidCacheStartTime) + "\", " \
            + "\"" + str(self.fluidCacheEndTime) + "\", " \
            + "\"" + str(self.fluidCacheDistribMode) + "\", " \
            + "\"" + str(self.fluidRefresh) + "\", " \
            + "\"" + str(self.fluidCacheDirName) + "\"," \
            + "\"" + str(self.fluidCachePerGeometry) + "\", " \
            + "\"" + str(self.fluidCacheName) + "\"," \
            + "\"" + str(self.fluidCacheUsePrefix) + "\", " \
            + "\"" + str(self.fluidCacheAction) + "\", " \
            + "\"" + str(self.fluidCacheForceOverwrite) + "\", " \
            + "\"" + str(self.fluidCacheSimulationRate) + "\", " \
            + "\"" + str(self.fluidCacheSampleMultiplier) + "\", " \
            + "\"" + str(self.fluidCacheInheritModifications) + "\", " \
            + "\"" + str(self.fluidCacheStoreFloats) + "\", " \
            + "\"" + str(self.fluidCacheFormat) + "\", " \
            + "\"" + str(self.fluidCachePBDensity) + "\", " \
            + "\"" + str(self.fluidCachePBVelocity) + "\", " \
            + "\"" + str(self.fluidCachePBTemperature) + "\", " \
            + "\"" + str(self.fluidCachePBFuel) + "\", " \
            + "\"" + str(self.fluidCachePBColor) + "\", " \
            + "\"" + str(self.fluidCachePBTextureCoords) + "\", " \
            + "\"" + str(self.fluidCachePBFalloff) + "\"" \
            + " }"

        return command








