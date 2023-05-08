import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


data = pd.read_csv("gap.tsv", sep='\t')
new = data.groupby('year')['lifeExp'].mean()


print(np.column_stack((new.index,new.values)))

