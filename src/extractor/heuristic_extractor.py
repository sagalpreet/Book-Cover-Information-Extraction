from numpy import mean
import pandas as pd
import context
from extractor.extractor import Extractor
from os.path import abspath, dirname, join
import sqlite3
import en_core_web_sm
import regex

nlp = en_core_web_sm.load()

class Heuristic_Extractor(Extractor):
    def extract(df: pd.DataFrame, confidence = 42):

        # store extracted information in a dictionary
        info = {
            "title": "",
            "authors": [],
            "publishers": [],
            "isbn": ""
        }

        # removing nan entries
        df = df.dropna()

        info['isbn'] = Heuristic_Extractor.__get_isbn(df)
        df = Heuristic_Extractor.__clean_dataframe(df, confidence)

        info['title'] = Heuristic_Extractor.__get_title(df)
        info['authors'] = Heuristic_Extractor.__get_authors(df)
        info['publishers'] = Heuristic_Extractor.__get_publishers(df, info['authors'])

        return info


    def __clean_dataframe(df, confidence):
        '''
        clean the dataframe by removing possibly
        wrongly read words
        '''

        # removing all values with confidence less than 50
        df = df[df['conf'] > confidence]

        # removing all whitespaces detected
        df = df[df['text'].astype(str).str.strip() != '']

        return df

    def __get_title(df):
        '''
        extracting TITLE:
        title in most cases is the one with largest font
        we identify the block with largest text size and
        consider that block as the title
        '''

        # isbn lines might be mistaken as | 1 or I
        df = df[df['text'] != '|']
        df = df[df['text'] != '1']
        df = df[df['text'] != 'I']

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
                res1 = list(cur.execute("select 1 where exists (select * from FN where first_name = ? collate nocase)", [i]))
                res2 = list(cur.execute("select 1 where exists (select * from LN where first_name = ? collate nocase)", [i]))
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
        for block_num in set(possible_blocks['block_num']):
            pos = possible_blocks[possible_blocks['block_num'] == block_num]
            total = df[df['block_num'] == block_num]
            mean_height = mean(total['height'])
            prob = pos.shape[0]/total.shape[0]
            cnt = pos.shape[0]

            if (prob < 0.5 or total.shape[0] - pos.shape[0] > 2):
                continue
            
            prob_author_block.append([cnt, block_num, mean_height])

        prob_author_block.sort(reverse = True)

        if (not prob_author_block):
            return []

        authors = []

        '''
        we try to identify blocks having author names by
        using the fact that their font sizes should be
        approximately equal
        '''
        while (True):

            mx = max([mean_height for prob, block_num, mean_height in prob_author_block])
            mn = min([mean_height for prob, block_num, mean_height in prob_author_block])

            if (mx - mn > deviation):
                prob_author_block.pop()
            else:
                break

        valid_blocks = []

        for prob, block_num, mean_height in prob_author_block:
            valid_blocks.append(block_num)

        for block_num in valid_blocks:
            phrase = ' '.join(df[df['block_num'] == block_num]['text'])
            authors.append(phrase)

        return authors

    def __get_publishers(df: pd.DataFrame, authors: list):

        popular_publishers = [
            'Wiley',
            'Pearson',
            'RELX',
            'Thomson Reuters',
            'Penguin Random House',
            'Hachette Livre',
            'HarperCollins',
            'Macmillan Publishers',
            'Bertelsmann',
            'Scholastic Corporation',
            'McGraw-Hill Education',
            'MIT Press',
            'Prentice Hall'
        ]

        # remove block with largest font size as that is probably the title
        try:
            block_num_largest_font = Heuristic_Extractor.__blocks_with_largest_font(df)[0]
            df = df[df['block_num'] != block_num_largest_font]
        except:
            pass

        publishers = []

        for block_num in set(df['block_num']):
            phrase = ' '.join(df[df['block_num'] == block_num]['text'])
            labels = [i.label_ for i in nlp(phrase).ents]
            if ('ORG' in labels and len(phrase) < 5 and phrase not in authors):
                publishers.append(phrase)

        if publishers:
            return publishers

        for block_num in set(df['block_num']):
            phrase = ' '.join(df[df['block_num'] == block_num]['text']).lower()

            if (phrase in authors):
                continue

            for publisher in popular_publishers:
                words = publisher.split()
                for word in words:
                    if (word.lower() in phrase):
                        return [publisher]

        return publishers

    def __get_isbn(df: pd.DataFrame):

        detected = [(float('inf'), "")]

        for block_num in set(df['block_num']):
            phrase = ''.join(df[df['block_num'] == block_num]['text'])

            num = ''
            for i in phrase:
                if (i >= '0' and i <= '9'):
                    num += i
                if (i == 'o' or i == 'O'):
                    num += '0'

            phrase = num

            if (len(phrase) < 10):
                continue

            if (phrase[:3] in ['978', '979']):
                return phrase

        return ''
