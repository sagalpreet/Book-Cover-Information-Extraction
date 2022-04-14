from numpy import mean
import pandas as pd
import context
from extractor.extractor import Extractor
from os.path import abspath, dirname, join
import sqlite3
import en_core_web_sm
import re

class Heuristic_Extractor(Extractor):
    def extract(df: pd.DataFrame, confidence = 50):

        # store extracted information in a dictionary
        info = {
            "title": "",
            "authors": [],
            "publishers": [],
            "isbn": ""
        }

        df = Heuristic_Extractor.__clean_dataframe(df, confidence)
        info['title'] = Heuristic_Extractor.__get_title(df)
        info['authors'] = Heuristic_Extractor.__get_authors(df)
        info['publishers'] = Heuristic_Extractor.__get_publishers(df)
        info['isbn'] = Heuristic_Extractor.__get_isbn(df)

        return info


    def __clean_dataframe(df, confidence):
        '''
        clean the dataframe by removing possibly
        wrongly read words
        '''
        
        # removing nan entries
        df = df.dropna()

        # removing all values with confidence less than 50
        df = df[df['conf'] > confidence]

        # removing all whitespaces detected
        df = df[df['text'].str.strip() != '']

        return df

    def __get_title(df):
        '''
        extracting TITLE:
        title in most cases is the one with largest font
        we identify the block with largest text size and
        consider that block as the title
        '''
        try:
            block_num_largest_font = Heuristic_Extractor.__blocks_with_largest_font(df)[0]
        except:
            return ""

        title = ' '.join(df[df['block_num'] == block_num_largest_font]['text'])

        return title

    def __blocks_with_largest_font(df):
        return list(df[df['height'] == max(df['height'])]['block_num'])

    def __get_authors(df, deviation = 2):

        # connect to database containing names
        names_db_path = abspath(join(dirname(__file__), 'database/names.db'))
        try:
            con = sqlite3.connect(names_db_path)
        except:
            raise FileNotFoundError("Database extractor/database/names.db not found")
        cur = con.cursor()

        # function to check if name is valid
        def is_valid_name(name):
            is_str = False
            if type (name) == str:
                name = [name]
                is_str = True
            res = []
                
            for i in name:
                res1 = list(cur.execute("select 1 where exists (select * from FN where first_name = ?)", [i]))
                res2 = list(cur.execute("select 1 where exists (select * from LN where first_name = ?)", [i]))
                res.append(res1 != [] or res2 != [])
            
            if (is_str): res = res[0]
            return res


        # remove block with largest font size as that is probably the title
        try:
            block_num_largest_font = Heuristic_Extractor.__blocks_with_largest_font(df)[0]
            df = df[df['block_num'] != block_num_largest_font]
        except:
            pass

        # extract possible words that are author names
        possible_blocks = df[is_valid_name(df['text'])]

        # check for emptiness
        if (possible_blocks.size  == 0):
            return []

        # calculate probability of each block
        prob_author_block = []
        temp_sum = 0
        for block_num in set(possible_blocks['block_num']):
            pos = possible_blocks[possible_blocks['block_num'] == block_num]
            total = df[df['block_num'] == block_num]
            mean_height = mean(total['height'])
            prob = pos.shape[0]/total.shape[0]

            temp_sum += prob
            prob_author_block.append([prob, block_num, mean_height])
        
        # divide by sum of all probabilites to convert into valid probability distribution
        for i in range(len(prob_author_block)):
            prob_author_block[i][0] /= temp_sum

        prob_author_block.sort(reverse = True)

        authors = []

        '''
        we try to identify blocks having author names by
        using the fact that their font sizes should be
        approximately equal
        '''
        while (True):
            valid_blocks = []
            curr_mean = mean([prob * height for prob, _, height in prob_author_block])
            
            for prob, block_num, mean_height in prob_author_block:
                if (abs(mean_height - curr_mean) < deviation):
                    valid_blocks.append(block_num)
            
            if (not valid_blocks):
                prob_author_block.pop()
                continue

            for block_num in valid_blocks:
                authors.append(
                    ' '.join(df[df['block_num'] == block_num]['text'])
                )

            break

        return authors

    def __get_publishers(df: pd.DataFrame):
        # remove block with largest font size as that is probably the title
        try:
            block_num_largest_font = Heuristic_Extractor.__blocks_with_largest_font(df)[0]
            df = df[df['block_num'] != block_num_largest_font]
        except:
            pass
        
        nlp = en_core_web_sm.load()

        publishers = []

        for block_num in set(df['block_num']):
            phrase = ' '.join(df[df['block_num'] == block_num]['text'])
            labels = [i.label_ for i in nlp(phrase).ents]
            if ('ORG' in labels):
                publishers.append(phrase)

        return publishers

    def __get_isbn(df: pd.DataFrame):
        for block_num in set(df['block_num']):
            phrase = ' '.join(df[df['block_num'] == block_num]['text'])
            isbn_regex = "^(?:ISBN(?:-1[03])?:?●)?(?=[0-9X]{10}$|(?=(?:[0-9]+[-●]){3})[-●0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[-●]){4})[-●0-9]{17}$)(?:97[89][-●]?)?[0-9]{1,5}[-●]?[0-9]+[-●]?[0-9]+[-●]?[0-9X]$"
            
            if (re.search(isbn_regex, phrase)):
                return phrase
            
        return ""