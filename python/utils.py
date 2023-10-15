## Imports
import pandas as pd
import numpy as np
from google.colab import files
import regex as re
from typing import List

class ExpertiseDoc:
    def __init__(self, name, doc_type, doc_text):
        self.name = name
        self.doc_type = doc_type
        self.doc_text = doc_text
        self.words = self.doc_text_to_vect()

    def get_level(self):
        return self._level

    def set_level(self, x):
        self._level = x

    def get_job(self):
        return self._job

    def set_job(self, x):
        self._job = x

    def doc_text_to_vect(self):
        doc_text = re.sub('[^0-9a-zA-Z]+', ' ', self.doc_text)
        doc_text = doc_text.lower()
        words = doc_text.split()
        return words

    def doc_text_to_clean(self):
        d_text = re.sub('[^0-9a-zA-Z]+', ' ', self.doc_text)
        d_text = d_text.lower()
        return d_text


def swap_columns(df, col1, col2):
    col_list = list(df.columns)
    x, y = col_list.index(col1), col_list.index(col2)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    df = df[col_list]
    return df

def find_exp_doc(exp_text,exp_docs):
  for expd in exp_docs:
    if exp_text[:100] in expd.doc_text_to_clean():
      return expd
  return None

def pre_process_resumes(raw_data) -> List[ExpertiseDoc]:
    exp_docs = []
    with open(raw_data, 'r') as file:
        exp_name = None
        exp_txt = ''
        for line in file:
            if len(line.strip()) == 0:
              continue
            if exp_name is None:
              exp_name = line.strip()
            elif '====' in line or '*****' in line :
              exp_docs += [ExpertiseDoc(exp_name,'Resume',exp_txt)]
              exp_name = None
              exp_txt = ''
            else:
              exp_txt += line


      ## Get levels
    level_map = {}
    with open(raw_data, 'r') as file:
      level_section = False

      job_type = ''
      for line in file:
        if '****' in line:
          level_section = True

        if level_section and line.strip() == 'Data Scientist:':
          job_type = 'Data Scientist'
        elif level_section and line.strip() == 'Data Engineer:':
          job_type = 'Data Engineer'
        elif level_section and line.strip() == 'Business Analyst:':
          job_type = 'Business Analyst'
        elif level_section and line.strip() == 'Software Developer:':
          job_type = 'Software Developer'

        if level_section and '-' in line:
          name = line.strip().split('-')[0].strip()
          level = line.strip().split('-')[1].strip()
          level_map[name] = (job_type,level)



    for exp_doc in exp_docs:
      lvl = level_map[exp_doc.name]
      exp_doc.set_job(lvl[0])
      exp_doc.set_level(lvl[1])

    return exp_docs, level_map


def pre_process_qa_docs(qa_doc_file) -> List:
    qa_docs = []
    with open(qa_doc_file, 'r') as file:
        for line in file:
            if len(line.strip()) == 0:
              continue
            qa_docs+= [line.split('|')]

    return qa_docs

def get_qa_text(qa_name,job,file_path):
  qa_docs = pre_process_qa_docs(file_path)
  for qa_doc in qa_docs:
    if qa_doc[0] == qa_name and qa_doc[1] == job:
      return qa_doc[2]

  return None
