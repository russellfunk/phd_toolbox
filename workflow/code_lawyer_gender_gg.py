# -*- coding: utf-8 -*-

"""code_lawyer_gender_gg.py: Code lawyer gender based on names with the gender guesser
package."""

import MySQLdb
import gender_guesser.detector as gender

def main():

  # initialize classifiers
  
  d = gender.Detector(case_sensitive=False)
  
  # connect to the database
  conn = MySQLdb.connect (host = "localhost",
                                user = "root",
                                passwd = "",
                                db = "patentsview",
                                charset = "utf8",
                                use_unicode = True)
  cursor = conn.cursor()

  # pull the data
  cursor.execute(""" select name_first_id, 
                            name_first_clean
                     from phd_patentsview.lawyer_gender_coding;""")
                     
  raw_names = cursor.fetchall()
  
  # classify names 
  for raw_name in raw_names:
  
    name_first_id = raw_name[0]
    name_first_clean = raw_name[1]

    # first, try the whole raw name
    candidate_gender = d.get_gender(name_first_clean)

    # second, try any component of the raw name
    if candidate_gender == "unknown":
      name_first_components = name_first_clean.split()
      for name_first_clean_component in name_first_clean_components:
        candidate_gender = d.get_gender(name_first_clean_component)
        if candidate_gender != "unknown":
          break
    
    # print the record
    print(name_first_id, name_first_clean, candidate_gender)  
    
    # add the record to the database
    cursor.execute(""" update phd_patentsview.lawyer_gender_coding
                       set gender_gg = %s
                       where name_first_id = %s;""", (candidate_gender,
                                                      name_first_id))
 
  cursor.close()
  conn.commit()
  conn.close()

if __name__ == '__main__':
  main()