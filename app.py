import streamlit as st   #app chalta hai  
import pandas as pd      #charts   
import plotly.express as px     #plotting


st.set_page_config(page_title="Sales Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
                   )

@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io = 'supermarket_sales.xlsx',
        engine='openpyxl',
        sheet_name='Sales',
        usecols='B:R',
        skiprows=3,
        nrows= 1000,
    )
    #Date time:
    df['hour'] = pd.to_datetime(df["Time"],format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

#st.dataframe(df)     
#print(df) 

#side bar

st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options= df["City"].unique(),
    default=df["City"].unique(),

)
customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options= df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)
gender = st.sidebar.multiselect(
    "Select the Gender:",
    options= df["Gender"].unique(),
    default=df["Gender"].unique(),
    )

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"

)

#st.dataframe(df_selection)

#---MainPage----

st.title(":bar_chart: Sales Dashboard")

st.markdown("##") #seprate the kpi's

# Total kpi's

total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(),1)
star_rating = ":star:" * int(round(average_rating,0))
average_sale_by_transaction = round(df_selection["Total"].mean(),2)

left_column , middle_column,right_column = st.columns(3)

with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US ${total_sales:,}")


with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")

with right_column:
    st.subheader("Average Sales By Transcation :")
    st.subheader(f"US ${average_sale_by_transaction}")


st.markdown("---")

# sales by product line [bar chart]

sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by = "Total")
)

fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation = "h",
    title = "<b> Sales By Product Lines </b>",
    color_discrete_sequence=["#0083BB"] * len(sales_by_product_line),
    template="plotly_white",
) 

fig_product_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))

)

#st.plotly_chart(fig_product_sales)


sale_by_hour  = df_selection.groupby(by="hour").sum()[["Total"]]
fig_hourly_sales = px.bar(
    sale_by_hour,
    x = sale_by_hour.index,
    y = "Total",
    title = "<b> Sales By Hour </b>",
    color_discrete_sequence=["#0083BB"] * len(sale_by_hour),
    template = "plotly_white"
)

fig_hourly_sales.update_layout(
    xaxis=(dict(tickmode="linear")),
    plot_bgcolor = "rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))

)

#st.plotly_chart(fig_hourly_sales)

left_column_1,right_column_1 = st.columns(2)
left_column_1.plotly_chart(fig_hourly_sales,use_container_width=True)
right_column_1.plotly_chart(fig_product_sales,use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)