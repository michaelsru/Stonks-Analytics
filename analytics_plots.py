import pandas as pd
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
import json

with open("config.json", "r") as f:
	config = json.load(f)

mydb = mysql.connector.connect(
	host=config.host,
	user=config.user,
	password=config.password,
  	database=config.database
)

df = pd.read_sql('SELECT * FROM command_logs', con=mydb)

# get unique set of command
commands = df['command'].unique()
print(commands)

# command popularity over time
# resample createdAt, sum commands and add column
df = df.set_index('createdAt')
command_df = df.copy()
for command in commands:
	print(command)
	command_df[command] = np.where(df.command == command, 1, 0)

command_df = command_df.resample('1min').sum()
print(command_df)

for command in commands:
    plt.plot(command_df.index, command_df[command], label=command)
plt.legend(loc=3,bbox_to_anchor=(1,0))
plt.show

# unique user activity over time


groups = df.groupby("userid").groups
users = df["userid"].unique()
for user in users:
    print("~~~~~~~~~~~~~~{}~~~~~~~~~~~~~~".format(user))
    for command_time in groups[user]:
        print(df.loc[command_time]['command'])


# command error frequency




# user balance growth over time


