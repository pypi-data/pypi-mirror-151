from PIL import Image
import os

# o = loadAsset("floor.png")
# print(o)

path = "nilslib/joe"
valid_images = [".jpg",".gif",".png",".tga"]

imgs = []

f = "floor.png"
print(f)#to pay respect
imgs.append(Image.open(os.path.join(path,f)))

print(imgs)