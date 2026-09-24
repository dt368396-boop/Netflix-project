import pandas as pd
import streamlit as st
import plotly.express as px
@st.cache_data
def load_data():
    df=pd.read_csv(r"C:\Users\Diksha Thakur\Downloads\netflix_titles.csv")
    df["date_added"]=pd.to_datetime(df["date_added"],errors="coerce")
    df["year_added"]=df["date_added"].dt.year
    return df

st.set_page_config(page_title="Netflix Dashboard",layout="wide")
st.title("Netflix DashBoard")
df=load_data()
st.sidebar.header("Dashboard Filter")
type_filter=st.sidebar.multiselect("Select Content Type",
                options=df["type"].dropna().unique(),
                default=df["type"].dropna().unique())
country_filter=st.sidebar.multiselect("Select Country",
            options=df["country"].dropna().unique())
rating_filter=st.sidebar.multiselect("Select Rating",
          options=df["rating"].dropna().unique())
year_filter=st.sidebar.slider("Select Release Year",(int)
    (df["release_year"].min()),(int)(df["release_year"].max()),(2000,2021))

fil_df=df[df["type"].isin(type_filter)]
if country_filter:
    fil_df=fil_df[fil_df["country"].isin(country_filter)]
if rating_filter:
    fil_df=fil_df[fil_df["rating"].isin(rating_filter)]
if year_filter:
    fil_df=fil_df[(fil_df["release_year"]>=year_filter[0]) &
                  (fil_df["release_year"]<=year_filter[1])]
st.write(fil_df)
st.subheader("Key Metrics")
col1,col2,col3,col4=st.columns(4)
total=len(fil_df)
movies=len(fil_df[fil_df["type"]=="Movie"])
tvshows=len(fil_df[fil_df["type"]=="TV Show"])
countries=fil_df["country"].nunique()
col1.metric("Total Titles",total)
col2.metric("Movies",movies)
col3.metric("Tv Shows",tvshows)
col4.metric("Countries",countries)
st.divider()
col1,col2=st.columns(2)
with col1:
    st.subheader("Movies Vs TV Shows")
    res=fil_df["type"].value_counts()
    fig=px.pie(names=res.index,values=res.values,
               color_discrete_sequence=px.colors.sequential.Reds)
    st.plotly_chart(fig,width="stretch")
with col2:
    st.subheader("Content over years")
    res1=fil_df["year_added"].value_counts().sort_index()
    fig=px.line(x=res1.index,y=res1.values,markers=True)
    fig.update_layout(xaxis_title="Year added",yaxis_title="Count")
    st.plotly_chart(fig,width="stretch")
st.divider()
col1,col2=st.columns(2)
with col1:
    st.subheader("Top Countries Producing Content")
    data=fil_df["country"].str.split(",").explode().str.strip().value_counts().head(10)
    fig=px.bar(data,x=data.values,y=data.index,color=data.values,color_continuous_scale="Reds",orientation="h")
    fig.update_layout(xaxis_title="Content Count",yaxis_title="Country")
    st.plotly_chart(fig,width="stretch")
with col2:
    st.subheader("Ratings Distribution")
    data=fil_df["rating"].value_counts()
    fig=px.bar(data,x=data.index,y=data.values,color=data.values,color_continuous_scale="Reds")
    fig.update_layout(xaxis_title="Rating",yaxis_title="Count")
    st.plotly_chart(fig,width="stretch")
st.divider()
st.subheader("Top Genres")
genres=fil_df["listed_in"].str.split(",").explode()
data=genres.value_counts().head(10)
fig=px.bar(data,x=data.index,y=data.values,color=data.values,color_continuous_scale="Reds")
fig.update_layout(xaxis_title="Genres",yaxis_title="Count")
st.plotly_chart(fig,width="stretch")
st.divider()
st.subheader("Global Distribution")
data=fil_df["country"].str.split(",").explode().str.strip().value_counts().reset_index()
data.columns=["Country","Count"]
fig=px.choropleth(data,locations="Country",locationmode="country names",color="Count",color_continuous_scale="Reds")
st.plotly_chart(fig,width="stretch")
st.divider()
st.subheader("Dataset Preview")
txtsrc=st.text_input("Enter Title to Search")
if txtsrc:
    data=fil_df[fil_df["title"].str.contains(txtsrc,case=False)]
    st.write(data)