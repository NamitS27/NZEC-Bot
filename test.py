# import matplotlib.pyplot as plt

# x = [2,4,6,2,2,2,2,2,2,2,2,2,8,10]
# y = [1,2,3,4,6,8,10,5,7,9,1,1,1,1]

# themes = ['Solarize_Light2', '_classic_test_patch', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-dark', 'seaborn-dark-palette', 'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'tableau-colorblind10']

# class foo:
#     def __init__(self,s):
#         self.string = s
#     def __str__(self):
#         return self.string


# x1 = [1,3,5,7,9]
# y2 = [2,4,6,8,10]
# # cnt  = 0
# # for theme in themes:
# #     plt.style.use(theme)
# #     plt.hist([x, y])
# #     plt.legend(["hi","bye"])
# #     plt.title(f"{theme}")
# #     plt.savefig(f"test{cnt}.png")
# #     cnt += 1

# under_score = u"\u005F"
# print(under_score)
# plt.plot(x,y)
# plt.legend([foo('_abs')])
# plt.savefig("a.png")

import psycopg2

global conn

try:
    conn = psycopg2.connect("dbname='nzec-bot' user='postgres' host='127.0.0.1' password='postgres'")
except:
    print("ERROR :(")

cur = conn.cursor()
import datetime as dt

time = dt.datetime.now()
print(time)

query = f"INSERT INTO server_det(server_id,user_id,cf_username,last_updated_time) VALUES('123','456','namit27','{time}')"
cur.execute(query)
conn.commit()


