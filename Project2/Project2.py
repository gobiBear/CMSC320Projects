import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

sqlite_file = 'lahman2014.sqlite.nosync'
conn = sqlite3.connect(sqlite_file)
cursor = conn.cursor()

payroll_query = "SELECT yearID, teamID, sum(salary) as total_payroll FROM Salaries GROUP BY teamID, yearID ORDER BY teamID"
wins_query = "SELECT yearID, teamID, W, G, 100.0*W/G as winning_percentage, franchID from Teams GROUP by teamID, yearID ORDER BY teamID"

payroll_df = pd.read_sql(payroll_query, conn)
wins_df = pd.read_sql(wins_query, conn)

conn.close()

df = pd.merge(payroll_df, wins_df, how="inner", on=["yearID", "teamID"]) #inner join, this causes missing data since data 
                                                                         #is only taken where both df's have entries for
                                                                         #that specific team in that year
                                                                         #can tell there is missing data by running
                                                                         #df.isnull().values.any()
print(df.head())

df.loc[df["teamID"] >= "ANA"].plot(x="yearID", y="total_payroll")
plt.xlabel("Year")
plt.ylabel("Payroll ($ in millions)")
plt.show()

