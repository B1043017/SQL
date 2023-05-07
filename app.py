import pandas as pd
import streamlit as st

import altair as alt
import duckdb

con = duckdb.connect(database='job.db', read_only=True) 

# Countries
query="""
   SELECT * 
   FROM job
"""
Countries=list(con.execute(query).df().columns)[2:]


st.subheader('Investingation')

col1, col2 = st.columns(2)

with col1:
    query="""
            SELECT 
                 DISTINCT variable
            From job        
            ORDER BY variable       
          """

    kinds=con.execute(query).df()
    kind = st.selectbox('Kind of Statistics',kinds)
with col2: 
    country = st.selectbox('Country',Countries)


result_df = con.execute("""
    SELECT 
        *
    FROM job 
    WHERE variable=?
    """, [kind]).df()

chart = alt.Chart(result_df).mark_circle().encode(
    x = 'date',
    y = country,
    #color = 'carrier'
).interactive()
st.altair_chart(chart, theme="streamlit", use_container_width=True)

# 更改Y軸編碼以顯示多個國家
result_df = result_df.set_index('date')[[country1, country2]].stack().reset_index()
result_df.columns = ['date', 'country', 'value']

# 繪製線圖
import matplotlib.pyplot as plt

plt.plot('date', 'value', data=result_df[result_df['country'] == country1], label=country1)
plt.plot('date', 'value', data=result_df[result_df['country'] == country2], label=country2)

plt.legend()
plt.xlabel('Date')
plt.ylabel(kind)

st.pyplot()
