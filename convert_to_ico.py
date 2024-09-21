from PIL import Image

img = Image.open('lock_icon.png')
img.save('lock_icon.ico', format='ICO')