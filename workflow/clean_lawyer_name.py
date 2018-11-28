# -*- coding: utf-8 -*-

"""clean_lawyer_name.py: Clean lawyer names to prepare for gender coding."""

import MySQLdb
import string

ALLOWABLE_CHARACTERS = string.ascii_letters + "-'"

def main():

  conn = MySQLdb.connect (host = "localhost",
                                user = "root",
                                passwd = "",
                                db = "patentsview",
                                charset = "utf8",
                                use_unicode = True)
  cursor = conn.cursor()

  cursor.execute(""" select name_first_id, 
                            name_first
                     from phd_patentsview.laywer_gender_coding;""")
                     
  raw_names = cursor.fetchall()
  
  for raw_name in raw_names:
    
    name_first_id = raw_name[0]
    name_first = raw_name[1]
    name_first_clean = name_first
    
    # replace '"'
    name_first_clean = name_first_clean.replace('"', " ")
    
    # replace ","
    name_first_clean = name_first_clean.replace(",", " ")

    # replace ";"
    name_first_clean = name_first_clean.replace(";", " ")
        
    # replace ":"
    name_first_clean = name_first_clean.replace(":", " ")
    
    # replace "."
    name_first_clean = name_first_clean.replace(".", " ")
    
    # replace "("
    name_first_clean = name_first_clean.replace("(", " ")

    # replace ")"
    name_first_clean = name_first_clean.replace(")", " ")

    # replace "/"
    name_first_clean = name_first_clean.replace("/", " ")

    # replace "\"
    name_first_clean = name_first_clean.replace("\\", " ")

    # replace "-"
    name_first_clean = name_first_clean.replace("-", " ")

    # split on whitespace
    name_first_clean = name_first_clean.split()
    
    # get rid of extra spaces and isolated letters
    name_first_clean = [n for n in name_first_clean if len(n) > 1]
        
    # remove remaining words with punctuation
    name_first_clean_final = []
    for token in name_first_clean:
      if any(c not in ALLOWABLE_CHARACTERS for c in token):
        continue
      else:
        name_first_clean_final.append(token)

    # join back together
    name_first_clean = " ".join(name_first_clean)
    name_first_clean_final = " ".join(name_first_clean_final)
    
    if name_first_clean_final == '':
      name_first_clean_final = None
      
    print(name_first, name_first_clean, name_first_clean_final)
    
    # add the data to the database
    cursor.execute(""" update phd_patentsview.lawyer_gender_coding
                       set name_first_clean = %s
                       where name_first_id = %s;""", (name_first_clean_final, 
                                                      name_first_id,))

  cursor.close()
  conn.commit()
  conn.close()

if __name__ == '__main__':
  main()