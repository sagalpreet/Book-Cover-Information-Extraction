import sqlite3
from tabnanny import verbose
import pytesseract
from PIL import Image, ImageFilter
import numpy as np
import cv2
from io import StringIO
import pandas as pd

path = '/media/sagalpreet/Data/Sagal/Coursework/IIT-Ropar/Sem-6/CS305/2019/assignments/Book-Information-Extraction/Sin-Eater-by-Megan-Campisi.jpg'
path = '/media/sagalpreet/Data/Sagal/Coursework/IIT-Ropar/Sem-6/CS305/2019/assignments/Book-Information-Extraction/xyz.jpg'
# path = '/media/sagalpreet/Data/Sagal/Coursework/IIT-Ropar/Sem-6/CS305/2019/assignments/Book-Information-Extraction/dataset/book-covers/Computing/0000001.jpg'
# path = '/home/sagalpreet/Pictures/MS.jpeg'

img = Image.open(path)

img = img.convert('L')

w_ = img.width
w = min(img.width, 2000)
h = img.height * (w / w_)
# img = img.resize((w, h))

# img = img.filter(ImageFilter.UnsharpMask(radius = 6.8, threshold = 0))

# img = np.array(img)

# img = (img > np.uint8(128)) * np.uint8(256)

x = StringIO(pytesseract.image_to_data(img))

df = pd.read_csv(x, sep='\t')

# print(df)


# NER = spacy.load("en_core_web_sm")

# print(NER('MEGAN CAMPISI').ents)

# for y in x.split('\n'):
#     t = NER(y)
#     for word in t.ents:
#         print(word.text, word.label_, sep = '\t\t')
#     print()

"""
con = sqlite3.connect('names.db')

cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE LN
               (first_name text)''')

# Insert a row of data
path = '/media/sagalpreet/Data/Sagal/Coursework/IIT-Ropar/Sem-6/CS305/2019/assignments/Book-Information-Extraction/NameDatabases/NamesDatabases/surnames/all.txt'
with open(path, 'r') as f:
    x = f.readline()
    while(x):
        print(x[:-1])
        cur.execute("INSERT INTO LN VALUES (?)", (x[:-1],))
        x = f.readline()

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()
"""