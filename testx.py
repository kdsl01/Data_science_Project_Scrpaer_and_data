import sqlalchemy
from sqlalchemy import create_engine,and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import xlrd
import numpy as np
import pandas as pd
import pyodbc
import random

from test import Tag,Base,engine, Movie,drop_tables,create_tables,Session

# Base.metadata.create_all(engine)

DF = pd.read_excel('data2500_v2.xlsx')
DF.columns =DF.columns.str.replace(' ', '')
drop_tables()
create_tables()
s = Session()
test2 = DF['Genre'].value_counts().rename_axis('Genre').reset_index(name='amount')
genrelist = []
for index, row in test2.iterrows():
    genrelist.append(row['Genre'])
for g in genrelist:
    d = Tag(
        Genre=g,
    )
    s.add(d)
    s.commit()
genreid = []
for instance in s.query(Tag).order_by(Tag.id):
    genreid.append([instance.Genre, instance.id])
# pd.set_option('display.max_columns', None)
# print(DF.head())
for i in range(2500):
    xcc = DF.loc[i, 'Genre']
    icx = 0
    for tg in genreid:
        if xcc == tg[0]:
            icx = tg[1]
    f = Movie(
        Genre_id=icx,
        name = DF.loc[i,'Name'],
        director=DF.loc[i,'Director'],
        IMDb_score = float(DF.loc[i,'IMDBscore']),
        MC_score = float(DF.loc[i,'MCScore']),
        year = float(DF.loc[i,'Year']),
        second_Genre =DF.loc[i,'Genre1']
    )
    s.add(f)
    s.commit()

# inputx = "Biography"
# idd = 0
# for tg in genreid:
#     if inputx == tg[0]:
#         idd = tg[1]
# res = s.query(Movie).filter(and_(Movie.Genre_id==idd, Movie.IMDb_score >= 8)).all()



while True:
    idd = 0
    print("What Genre do you want?\n")
    print("['Action', 1], ['Drama', 2], ['Comedy', 3], ['Adventure', 4], ['Animation', 5], ['Crime', 6], ['Biography', 7], ['Comedy ', 8], ['Horror', 9], ['Drama ', 10], ['Mystery', 11], ['Horror ', 12], ['Fantasy', 13], ['Western ', 14], ['Family', 15], ['Sci-Fi', 16], ['Romance', 17], ['Musical', 18]]")
    print("\nExit by enter end\n")
    inputx = input("Enter Genre: ")
    if inputx == "end" or inputx == "End":
        break;
    else:
        for tg in genreid:
            if inputx == tg[0]:
                idd = tg[1]
        inputx2 = input("second Genre?(Genre/N)")
        if inputx2 == "N":
            res = s.query(Movie).filter(Movie.Genre_id == idd).all()
        else:
            res = s.query(Movie).filter(and_(Movie.Genre_id == idd,Movie.second_Genre==inputx2)).all()
        if len(res) == 0:
            print("nothing found")
            continue
        if len(res)<20:
            for i in res:
                print(i.name,i.IMDb_score, i.year)
        else:
            while True:
                tkt = random.randint(0,len(res)-10)
                for i in range(tkt,tkt+10):
                    print(res[i].name,res[i].IMDb_score,"("+str(int(res[i].year))+")")
                inputtkt = input("Whant a new list? (Y) Go back and pick new genre(N):")
                if inputtkt == "Y":
                    continue
                elif inputtkt == "N":
                    break;
        # inputy = input("Want more specific? (Y/N):")
        # if inputy == 'Y':
        #     while True:
        #         ry = input("Release year(Enter end to finish):")
        #         if ry == "end":
        #             break;
        #         res = s.query(Movie).filter(and_(Movie.Genre_id == idd,Movie.year == float(ry))).all()
        #         if len(res) == 0:
        #             print("Sorry, nothing found this year")
        #         for i in res:
        #             print(i.name,i.IMDb_score)

