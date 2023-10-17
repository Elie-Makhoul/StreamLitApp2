import pandas as pd
import plotly.express as px
import streamlit as st


# Load the data


df = pd.read_csv("csv/LC_Loan_Modified.csv")


# Set page configuration
st.set_page_config(page_title="LC loan Dashboard",
                   page_icon=":bar_chart:", layout="wide")


# Create a pie chart

# loan_amount_by_term = df.groupby('term')['loan_amnt'].sum().reset_index()
# fig1 = px.pie(
#     loan_amount_by_term,
#     names='term',
#     values='loan_amnt',
#     title='Loan Amount by Term',
#     labels={'term': 'Term (months)', 'loan_amnt': 'Total Loan Amount'}
# )


# create scatter plot 1
fig1 = px.box(
    df,
    x='term',
    y='loan_amnt',
    title='Loan Amount vs Term',
    labels={'loan_amnt': 'Loan Amount', 'term': 'Term'},

)


# Count the occurrences of each loan status
loan_status_counts = df['loan_status'].value_counts().reset_index()
loan_status_counts.columns = ['loan_status', 'count']

# Create a pie chart
fig2 = px.pie(
    loan_status_counts,
    names='loan_status',
    values='count',
    title='Loan Status Distribution',
    color='loan_status',
    color_discrete_map={'Fully Paid': 'green', 'Charged Off': 'red'}
)


emp_length_mapping = {
    '< 1 year': 0,
    '1 year': 1,
    '2 years': 2,
    '3 years': 3,
    '4 years': 4,
    '5 years': 5,
    '6 years': 6,
    '7 years': 7,
    '8 years': 8,
    '9 years': 9,
    '10+ years': 10
}


df['emp_length_order'] = df['emp_length'].map(emp_length_mapping)

# Sort the DataFrame based on the new chronological order


df = df.sort_values(by='emp_length_order', ascending=True)


# create heatmap
fig3 = px.imshow(df.pivot_table(index='emp_length_order', columns='home_ownership',  values='annual_inc'),
                 labels={
    "emp_length_order": "Employment Length (years)", "home_ownership": "Home Ownership"},
    title='Annual Income Heatmap: Employment Length vs Home Ownership')


# create scatter plot 3
fig4 = px.scatter(
    df,
    x='open_acc',  # x-axis: number of open credit lines
    y='delinq_2yrs',  # y-axis: number of delinquencies
    title='Credit and Payment History: Delinquencies vs Open Credit Lines'
)

# create scatter plot 4
fig5 = px.scatter(df, x='dti', y='revol_util', title=' "Revolving Line Utilization vs. Debt-to-Income Ratio',
                  labels={'dti': 'Debt-to-Income Ratio',
                          'revol_util': 'Revolving Line Utilization'},
                  hover_data=['dti', 'revol_util'])

# Group by grade and count the number of clients in each grade
grade_counts = df.groupby('grade').size().reset_index(name='client_count')


loan_amount_by_grade = df.groupby('grade')['loan_amnt'].sum().reset_index()
# Merge the loan_amount_by_grade DataFrame with the grade_counts DataFrame

grade_df = pd.merge(loan_amount_by_grade, grade_counts, on='grade')


fig6 = px.bar(grade_df, x='grade', y='loan_amnt',
              labels={'grade': 'Grade', 'loan_amnt': 'total Loan Amount'},
              hover_data=grade_counts,

              title='total Loan Amount by Grade')


# display KPIs

with st.container():
    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns([1, 1], gap="medium")
    with col3:
        st.plotly_chart(fig3, use_container_width=True)
    with col4:
        st.plotly_chart(fig4, use_container_width=True)

    col5, col6 = st.columns([1, 1], gap="medium")
    with col5:
        st.plotly_chart(fig5, use_container_width=True)
    with col6:
        st.plotly_chart(fig6, use_container_width=True)
