from tkinter import *
from PIL import ImageTk, Image
import os



class Decorator():
    
    def countExecutionMethod(method):
        def wrapper(*args, **kwargs):
            wrapper.counter += 1
            print(f"{method}Ponavlja se {wrapper.counter}. put")
            return method(*args, **kwargs)
        wrapper.counter = 0
        return wrapper

    def ListAppend(ListX):
        def decorator(method):
            def wrapper(*args, **kwargs):
                result = method(*args, **kwargs)
                ListX.extend(result)
                return result
            return wrapper
        return decorator

class Import():
    ImagesLocation = os.path.join(os.path.dirname(__file__),'Slike')
    TranscriptName=None
    AllImages=[]

    @Decorator.ListAppend(AllImages)
    def ImageImport():
        imageCount = 32
        Images = [] ; Img_wPwS = [] ; Img_wPbS = [] ; Img_bPwS = [] ; Img_bPbS = []
        for i in range(imageCount): # Image upload
            image = ImageTk.PhotoImage(Image.open(os.path.join(Import.ImagesLocation,f"{i}.png")))
            Images.append(image) if i<4 else \
                (Img_wPwS.append(image) if i <11 else \
                (Img_wPbS.append(image) if i < 18 else \
                (Img_bPwS.append(image) if i < 25 else \
                (Img_bPbS.append(image)))))
        return  Images,Img_wPwS,Img_wPbS,Img_bPwS,Img_bPbS