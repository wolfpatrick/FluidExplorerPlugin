_author__ = 'Patrick'

import os

class FluidExplorerUtils():

    @staticmethod
    def dirExists(path):
        exists = False
        exists = os.path.exists(path)
        return exists