filename = "img.jpg"

tag = {"jpg":"jpeg", "png":"png", "tif":"tiff", "bmp":"bmp"}

prefix = ""
ext = filename.split(".")[1]
if (ext in tag):
    prefix = tag[ext]

f = open("img.jpg","r")
img = f.read()
f.close()
out = open("base.txt","w")
data = "data:image/"+prefix+";base64,"
data += img.encode("base64")
out.write(data)
out.close()
