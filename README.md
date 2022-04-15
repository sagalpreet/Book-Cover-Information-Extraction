# Book Information Extraction
---
**Submitter name**:  Sagalpreet Singh\
    **Roll No**:  2019csb1113\
    **Course**:  CS305

---
#
### What does this program do ?
The goal is to extract information (Title, Authors, Publishers and ISBN number) from the cover or the initial few pages of any book. Given the diverse nature of books available, the program has been developed in best efforts to give "not so" bad results. The current bottleneck is the OCR (this program uses tesseract for OCR).

The information extracted is then dumped into output.xlsx. This excel file is created in the same location from where the program is executed.

The program needs a compulsary command line argument (exactly one) which specifies the path to be processed. The path could be that of a single document or a directory containing multiple docuements.

Currently the program only supports **.jpg** and **.png** 

#

### A description of how this program works (i.e. its logic)

The program first identifies if the input path is that of a directory or an image.
Accordingly files to be processed are fetched. In case of a directory all the valid files are processed, rest are ignored and an appropriate warning is logged.
The image file is binarized and passed to tesseract for ocr. The data received is converted to a dataframe.
This data consists of the text blocks identified along with their height (font-size, essentially), location etc.
This raw data needs to be pre-procesed before exploiting it to get desired information.
All the nan values are removed from this data. Text which is just a white space is removed from the data. The text which has been recognized with low confidence value is neglected (dropped).

##### Using heuristics below the data obtained is processed to obtain information:
######
**Title**: The largest font size is identified and the block corresponding to that is identified as the title.

**Authors**: The text extracted is searched across the name database to find any match. From all the matches, the most probable ones are recognized as the ones with similar font size and most matches. Any block which has got a match but the percentage of words matched from that block compared to the total number of words in that block is neglected.

**Publishers**: Every block is checked for having an organization name in it. Further the percentage of text identified as organiztion in that block is checked to be larger than a threshod. In case it is not, the words in block are tried to be matched with a given set of 11 most popular publishers.

**ISBN**: This is an exception for the reason that it is extracted after dropping nan values but before any other pre-processing as isbn number is often recognized with low confidence. For all the blocks, the numeric contents are concatenated and the lenght is checked. If the number starts with 979 or 978 and its length is greater than 9, it is identified as ISBN number. There is a some chance, that the number consists of an extra 1 because of the long vertical lines being identified as 1 by the ocr. Also, if an 'o' is recognized by the ocr in a bunch of numeric characters, we treat it as a 'zero'.

Finally the output is dumped into an excel file as well as printed to the console.

| Utility | Library |
| ----------- | ----------- |
| OCR | Tesseract (pytesseract) |
| Database   | Sqlite |
| Image Processing | PIL |
| NLP | Spacy |

### How to compile and run this program

**Running the program**
`sh run.sh pictures`

**Running tests**
`sh run-tests.sh`

*Make sure to run the scripts from the root of the project to avoid any import errors*

### Sample run

---
**(main U:9 ?:7 ✗) Book-Information-Extraction >** *sh run.sh pictures*
```
Saved at output.xlsx
                      title                       authors     publishers            isbn
0                 BOOK ‘MES  JILL GREGORY & KAREN TINTORI                               
1               BONE COULEE                LARRY WARWARUK                               
2      QUENCHED LIKE A WICK                  DREW SIMMONS                 97814751038897
3  MODELLING AND SIMULATION           STANISLAW BACZYNSKI                               
4                Clean Code       Robert C. Martin Series                               
5                Clean Code              Robert C. Martin  Prentice Hall                
6         9" 783161" 484100                                                9783161484100
7             THIRD EDITION                    AMIT GUPTA          Wiley                
```
---
**(main U:9 ?:7 ✗) Book-Information-Extraction >** *sh run-tests.sh*
```
============================ test session starts =============================
platform linux -- Python 3.8.10, pytest-7.1.1, pluggy-1.0.0
rootdir: /
collected 11 items                                                           

test/app/test_app.py ...                                               [ 27%]
test/document/test_document.py .                                       [ 36%]
test/document/test_jpg.py .                                            [ 45%]
test/document/test_png.py .                                            [ 54%]
test/extractor/test_heuristic_extractor.py ....                        [ 90%]
test/path/test_path.py .                                               [100%]

============================= 11 passed in 4.72s =============================
Wrote HTML report to htmlcov/index.html

```
