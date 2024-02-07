import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the datasets
activities = pd.read_csv('activities.csv')
activities_summary = pd.read_csv('activities_summary.csv')
distances = pd.read_csv('distances.csv')
heartRateZones = pd.read_csv('heartRateZones.csv') 
import streamlit as st

#class for creating the contents:
class Toc:

    def __init__(self):
        self._items = []
        self._placeholder = None
    
    def header(self, text):
        self._markdown(text, "h2", " " * 2)

    def subheader(self, text):
        self._markdown(text, "h3", " " * 4)

    def placeholder(self, sidebar=False):
        self._placeholder = st.sidebar.empty() if sidebar else st.empty()

    def generate(self):
        if self._placeholder:
            self._placeholder.markdown("\n".join(self._items), unsafe_allow_html=True)
    
    def _markdown(self, text, level, space=""):
        key = "".join(filter(str.isalnum, text)).lower()

        st.markdown(f"<{level} id='{key}'>{text}</{level}>", unsafe_allow_html=True)
        self._items.append(f"{space}* <a href='#{key}'>{text}</a>")


toc = Toc()
st.title('Web Data Mining - Project 2')
st.markdown(' ##### Stoikopoulou Eleonora | Gerochristou Margarita | Prokopiou Ioannis ')
st.divider()
heartRateZones = pd.read_csv('heartRateZones.csv')
distances = pd.read_csv('distances.csv')
activities_summary = pd.read_csv('activities_summary.csv')
activities = pd.read_csv('activities.csv')
heartRate = pd.read_csv('heartRate.csv')

caloriesOut_pivoted = heartRateZones.pivot(index=['date'], columns='name', values='caloriesOut')
caloriesOut_pivoted.columns = [col for col in caloriesOut_pivoted.columns.values]
caloriesOut_pivoted.reset_index(inplace=True)

with st.container():
  col1, col2, col3, col4 = st.columns(4)
  
  steps_avg = round(activities_summary['steps'].mean(),2)
  col1.metric(label="Daily Avg Steps Taken", value=steps_avg)

  distances_total = distances[distances['activity']=='total']
  distances_avg = round(distances_total['distance'].mean(),2)
  col2.metric(label="Daily Avg Km Traveled", value=distances_avg)

  caloriesOut_pivoted['Total'] = caloriesOut_pivoted[['Cardio', 'Fat Burn', 'Out of Range', 'Peak']].sum(axis=1)
  caloriesOut_avg = round(caloriesOut_pivoted['Total'].mean(),2)
  col3.metric(label="Daily Avg Calories Burned", value=caloriesOut_avg)

  floors_avg = round(activities_summary['floors'].mean(),2)
  col4.metric(label="Daily Avg Floors Climbed", value=floors_avg)

st.divider()

st.text( "Welcome to this step of our data app development project!" )
st.text("In this step, we will be sharing some interesting visualizations")
st.markdown("For more detailed information look our [medium article](https://medium.com/@stoikopoyloyeleonwra/dac2ab8beaf9).")
toc.placeholder()

toc.header("Activities visualizations")

# Active Minutes Per Day
toc.subheader("Active Minutes Per Day")
activities_max = activities_summary.groupby('date').agg({'lightlyActiveMinutes': 'max', 'fairlyActiveMinutes': 'max', 'veryActiveMinutes': 'max'})
activities_max.reset_index(inplace=True)
activities_max = pd.melt(activities_max, id_vars=["date"], var_name="Intensity", value_name="Active Minutes")

# Create the line chart
fig = px.line(activities_max, x='date', y='Active Minutes', color='Intensity', height=400)

# Customize the chart
fig.update_layout(xaxis_title='Date', yaxis_title='Active Minutes', legend_title='Intensity',
                  xaxis_tickangle=-45, xaxis_tickfont_size=10, yaxis_tickfont_size=10)

# Show the chart in Streamlit
st.plotly_chart(fig)

toc.subheader("Total Time Spent in Each Activity Type")

# Assume activities_summary is a pandas DataFrame with the activity data
activity_totals = pd.Series([3000, 500, 50, 120, 60, 30], 
                            index=["Steps", "Floors", "Elevation", "Lightly Active", "Fairly Active", "Very Active"])

labels = ["Steps", "Floors", "Elevation", "Lightly Active", "Fairly Active", "Very Active"]
colors = ["#F1A208", "#F26A08", "#F2A0A5", "#00AEEF", "#0072C6", "#F05A5A"]

# Create a Plotly pie chart with Streamlit
fig = go.Figure(data=[go.Pie(labels=labels, values=activity_totals, hole=.5,  
                             marker=dict(colors=colors))])

# Set the layout of the pie chart
fig.update_layout(
    width=300,
    height=500,
    margin=dict(l=2, r=2, b=2, t=2),
    showlegend=False,
)

# Add labels to the pie chart
fig.update_traces(textposition='outside', textinfo='label+percent')

# Display the Plotly pie chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

toc.subheader('Distance traveled per day by activity type')

st.caption("*Distance in kilometers")
distances_pivot = distances.pivot(index='date', columns='activity', values='distance')
distances_pivot.reset_index(inplace=True)
distances_pivot = distances_pivot.drop(['loggedActivities','sedentaryActive','tracker'], axis=1)
distances_pivot = distances_pivot[['date','total','lightlyActive','moderatelyActive','veryActive']]
distances_pivot = distances_pivot.rename(columns={'date':'Date','total':'Total','lightlyActive':'Lightly Active',
                                                    'moderatelyActive':'Moderately Active','veryActive':'Very Active'})

st.bar_chart(distances_pivot, x = 'Date',y=['Lightly Active','Moderately Active','Very Active'])

toc.subheader('Walk session information')

st.markdown('**Select walk session to preview data**')
activities = activities[activities['activityParentName'] == 'Walk']
activities = activities[['calories', 'duration', 'steps', 'date', 'startTime' ]]
activities['dateTime'] = activities.apply(lambda x: x['date'] + ' ' + x['startTime'], axis=1)
session = st.selectbox(
  'session',
  options=activities['dateTime'],
  label_visibility = 'collapsed')

session_selected = activities[activities['dateTime'] == session]
with st.container():
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Duration", value= session_selected['duration'])
    col2.metric(label="Steps", value= session_selected['steps'] )
    col3.metric(label="Calories", value= session_selected['calories'])
activities = pd.read_csv('activities.csv')

toc.subheader('Activities summary')

walks = activities[activities['name']=='Walk']
walks_grouped_activity = walks.groupby('name').agg({'activityId': 'count', 'steps': 'sum'})
walks_grouped_activity.reset_index(inplace=True)
walks_grouped_activity = walks_grouped_activity.rename(columns={'activityId':'Activity count','name':'Activity','steps':'Steps'})

walks = activities[activities['name']=='Walk']
walks_grouped_day = walks.groupby('date').agg({'activityId': 'count', 'steps': 'sum'})
walks_grouped_day.sort_values(by='activityId',inplace=True, ascending=False)
walks_grouped_day.reset_index(inplace=True)
walks_grouped_day = walks_grouped_day.rename(columns={'date':'Date','activityId':'Activity count','steps':'Steps'})

with st.container():
  col1, col2 = st.columns(2)
  col1.text('Total activites and their steps')
  with col1.container():
    col1a, col1b = st.columns(2)
    col1a.bar_chart(walks_grouped_activity, x='Activity',y='Activity count')
    col1b.bar_chart(walks_grouped_activity, x='Activity',y='Steps')
  col2.text('Daily number of activities')
  col2.table(walks_grouped_day)

toc.header("Heart rate visualizations")

toc.subheader('Heart Rate daily trend')

heartRate_max = heartRate.groupby('date').agg({'value': 'max'})
heartRate_max.reset_index(inplace=True)
heartRate_max = heartRate_max.rename(columns={'value':'Max','date':'Date'})
heartRate_min = heartRate.groupby('date').agg({'value': 'min'})
heartRate_min = heartRate_min.rename(columns={'value':'Min'})
heartRate_min.reset_index(inplace=True,drop=True)
heartRate_mean = round(heartRate.groupby('date').agg({'value': 'mean'}),1)
heartRate_mean = heartRate_mean.rename(columns={'value':'Mean'})
heartRate_mean.reset_index(inplace=True,drop=True)
heartRate_trend = pd.concat([heartRate_max,heartRate_min,heartRate_mean], axis=1)

st.line_chart(heartRate_trend, x = 'Date',height=300)

toc.subheader('Calories burned per day by heart rate zone')

st.line_chart(caloriesOut_pivoted, x = 'date')

toc.subheader('Heart rate zone minutes total percentage by day')

with st.container():
  col1, col2 = st.columns([1.8,1])

  minutes_pivoted = heartRateZones.pivot(index=['date'], columns='name', values='minutes')
  minutes_pivoted.columns = [col for col in minutes_pivoted.columns.values]
  minutes_pivoted.reset_index(inplace=True)
  minutes_pivoted.iloc[:,1:] = round(minutes_pivoted.iloc[:,1:].div(1440) * 100,2)
  
  
  col1.bar_chart(minutes_pivoted, x = 'date')

  heartRateZones_table = heartRateZones.groupby('name').agg({'min': 'min', 'max': 'max'})
  heartRateZones_table.sort_values(by='min',inplace=True)
  heartRateZones_table.reset_index(inplace=True)
  new_names = {
    'name': 'Heart rate zone',
  }
  heartRateZones_table = heartRateZones_table.rename(columns=new_names)

  col2.markdown('**Heart rate ranges per zone**')
  col2.table(heartRateZones_table)
  col2.caption("The values displayed are monthly min and max. \
    Daily values varied over the period causing an overlapping in the final table.")

toc.subheader('Heart rate zone minutes total percentage by day for Each Category')

with st.container():
  col1, col2 = st.columns([1,2],gap='large')
  col1.markdown('**Select category to preview data**')
  # category = col1.select_slider(
  #   'category',
  #   options=heartRateZones['name'].unique(),
  #   label_visibility = 'collapsed')
  category = col1.radio(
    "Select category to preview dat",options=heartRateZones['name'].unique(),label_visibility = 'collapsed')
  minutes_pivoted_selected = minutes_pivoted[['date',category]]
  col2.markdown('**Heart Rate Zone Minutes by Day**')
  col2.bar_chart(minutes_pivoted_selected, x = 'date', )

toc.subheader("Detailed heart rate Data View for each day")

with st.container():
  col1, col2 = st.columns([1,2],gap='large')
  col1.markdown('**Select date to preview data**')
  date = col1.select_slider(
    'label',
    options=distances_pivot['Date'],
    label_visibility = 'collapsed')

  col2.markdown('**Heart Rate Statistics**')
  heartRate_selected = heartRate[heartRate['date']==date]
  heartRate_min = heartRate_selected['value'].min()
  heartRate_max = heartRate_selected['value'].max()
  heartRate_mean = round(heartRate_selected['value'].mean(),1)
  with col2.container():
    col1, col2, col3 = st.columns(3)

    col1.metric(label="Min Heart Rate", value=heartRate_min)
    col2.metric(label="Max Heart Rate", value=heartRate_max)
    col3.metric(label="Avg Heart Rate", value=heartRate_mean)

  selected_distance = distances[(distances['date']==date)&(distances['activity']=='total')][['date','distance']]
  selected_distance.reset_index(drop=True,inplace=True)
  selected_activities_summary = activities_summary[activities_summary['date']==date][['steps','floors','elevation']]
  selected_activities_summary.reset_index(drop=True,inplace=True)
  selected_heartRateZones = heartRateZones[heartRateZones['date']==date]
  selected_heartRateZones = selected_heartRateZones.groupby('date').agg({'caloriesOut': 'sum'})
  selected_heartRateZones.reset_index(drop=True,inplace=True)

  selection_output = pd.concat([selected_distance, selected_activities_summary,selected_heartRateZones], axis=1)
  selection_output = selection_output.rename(columns={'date':'Date','distance':'Distance','steps':'Steps',
                                                    'floors':'Floors','elevation':'Elevation','caloriesOut':'Calories'})
  st.markdown('**Day totals**')
  st.table(selection_output)

  st.markdown('**Distance traveled by activity type**')
  distances_pivot_selected = distances_pivot[distances_pivot['Date']==date]
  distances_pivot_selected = distances_pivot_selected.rename(columns={'Date':'Date','total':'Total','lightlyActive':'Lightly Active',
                                                    'moderatelyActive':'Moderately Active','veryActive':'Very Active'})
  
  st.table(distances_pivot_selected)

  st.markdown('**Heart Rate trend**')
  st.line_chart(heartRate_selected, x='time',y='value', height=250)

  toc.generate()