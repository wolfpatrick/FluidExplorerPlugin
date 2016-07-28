import os
import subprocess


class GifCreator():

    def __init__(self):
        pass

    def createGifFromImages(self, ffmpegPath, directoryImages, outputGifFileDir, outputGifFileName, start_number, fps=25, gifOptimization=True):

        imageNames = 'image_%05d.jpg'

        # inputDirFile = os.path.abspath(directoryImages + '/' + imageNames)
        # outputFileName = os.path.abspath(outputGifFileDir + '/' + outputGifFileName)

        if not directoryImages.endswith('/'):
            directoryImages = directoryImages + '/'
        if not outputGifFileDir.endswith('/'):
            outputGifFileDir = directoryImages + '/'

        inputDirFile = os.path.abspath(directoryImages + imageNames)
        outputFileName = os.path.abspath(outputGifFileDir + outputGifFileName)

        if os.name == 'nt':
            pathToFfmpeg = ffmpegPath + "/ffmpeg.exe"
            isFfmpegExecutable = self.is_exe(pathToFfmpeg)
            returnCode = False
        else:
            # TODO: Unix path
            pass

        if isFfmpegExecutable:
            start_number = str(start_number)
            subprocess_args = [pathToFfmpeg, '-thread_queue_size', '512', '-start_number', start_number]
            subprocess_args.extend(['-i', inputDirFile])

            filters = 'fps=' + str(fps)

            palettegen_options = 'palettegen'
            paletteuse_options = 'paletteuse'

            if gifOptimization:
                palettegen_options = 'palettegen=stats_mode=diff'
                paletteuse_options = 'paletteuse=dither=floyd_steinberg'

            # Call the ffmpeg functions
            if os.name == 'nt':     # Windows = 'nt' / UNIX = 'posix'
                # Hide output terminal window in windows os
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

                palette = outputGifFileDir + '/palette.png'
                palette = os.path.abspath(palette)
                try:
                    subprocess.call(subprocess_args + ['-vf', filters + ',' + palettegen_options, '-y', palette], shell=False, startupinfo=startupinfo)
                    subprocess.call(subprocess_args + ['-i', palette, '-lavfi', filters + ' [x]; [x][1:v] ' + paletteuse_options, '-y', outputFileName], shell=False, startupinfo=startupinfo)
                except Exception as er:
                    print("Error: " "Could not create the GIF animations! Details: ", er.message)
                    returnCode = False
                    return returnCode

                finally:
                    if os.path.exists(palette):
                        os.remove(palette)

            else:
                palette = outputGifFileDir + '/palette.png'
                palette = os.path.abspath(palette)
                try:
                    subprocess.call(subprocess_args + ['-vf', filters + ',' + palettegen_options, '-y', palette])
                    subprocess.call(subprocess_args + ['-i', palette, '-lavfi', filters + ' [x]; [x][1:v] ' + paletteuse_options, '-y', outputFileName])
                except Exception as er:
                    print("Error: " "Could not create the GIF animations! Details: ", er.message)
                    returnCode = False
                    return returnCode

                finally:
                    if os.path.exists(palette):
                        os.remove(palette)


            returnCode = True

            return returnCode

        else:
            return returnCode

    def is_exe(self, fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
