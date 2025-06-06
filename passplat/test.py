import pandas as pd
import itertools

data = {
    "eid": ["emile", "cat", "peter"],
    "p1": [None, None, [1]],
    "p2": [None, [-18, 14], None],
    "p3": [[-18, 14], [-18, 13], [-8, -5]]
}
df = pd.DataFrame.from_dict(data)
print(df)
print(type(df.p1[2][0]))

#df['illnesses_of_father'] = df.filter(regex=('^p')).apply(lambda x: list(set(eval(x.any() or "[]"))), axis=1)
#df['illnesses_of_father'] = df.filter(regex=('^p')).apply(lambda x: list(set(eval(str([str(i )for i in x if i is not None]) if x is list else "[]"))), axis=1)
df['illnesses_of_father'] = df.filter(regex=('^p')).apply(lambda x: x.any(), axis=1)
print(df)
# print(type(df.illnesses_of_father[0][0]))


# data2 = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35], 'City': ['NY', 'LA', 'SF']}
# df = pd.DataFrame(data2)
# # Select rows where Age is greater than 25
# #filtered_rows = df.loc[df['Age'] > 25]
# filtered_rows = df['Age'].loc[df['Age'] > 25]
# a=df[df['Age'] > 25]
# print(filtered_rows)

