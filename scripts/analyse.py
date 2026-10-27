#Visualising the spread of articles by year
df["year"].value_counts().sort_index().plot(kind="bar", figsize=(12, 4)),
  
#Visualising the spread of articles by section
df["section"].value_counts().head(10)