f = open("base.txt","r")
img = f.read()
img = img.split(",")[1] # split header, for example: "data:image/jpeg;base64,"
f.close()
out = open("img.jpg","w")
out.write(img.decode("base64"))
out.close()
