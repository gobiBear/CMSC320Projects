import pandas as pd
import numpy as np

df1 = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                   columns=['a', 'b', 'c'])

df2 = pd.DataFrame(np.array([[11, 12, 13], [4, 15, 16], [17, 18, 19]]),
                   columns=['a', 'b', 'c'])

merged = pd.merge(df1, df2, how="left", on="a" )

print(merged)