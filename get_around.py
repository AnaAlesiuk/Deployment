import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from statistics import mean
from statistics import median
#%%
header = st.container()
dataset = st.container()
features = st.container()
predictions = st.container()
#%%
data = pd.read_csv("data.csv")
back_late = pd.read_csv("back_late.csv")
count = pd.read_csv('count.csv')
back_late_connect = pd.read_csv('back_late_connect')
back_late_mobile = pd.read_csv('back_late_mobile')
checkin = pd.read_csv('checkin.csv')
checkin_late = pd.read_csv('checkin_late.csv')
connect_data = pd.read_csv('connect_data.csv')
count_days = pd.read_csv('count_days.csv')
mobile_data = pd.read_csv('mobile_data.csv')
count_checkin = pd.read_csv('count_checkin.csv')

with header:
    st.title("Get Around Analysis")
    st.markdown("Late returns at checkout can generate high friction for the next driver if the car was supposed to be "
            "rented again on the same day : Customer service often reports users unsatisfied because they had to wait "
            "for the car to come back from the previous rental or users that even had to cancel their rental because "
            "the car wasn’t returned on time.")
    st.markdown("**_The Goal of the analysis_**: implement a minimum delay between two rentals.")
#%%
with dataset:
    st.header("Data")
    st.markdown("This dataset includes such an important information as _checkin type_, _delay at checkout_, "
                "_time delta with previous rental_, _delay hours_ ,_delay minutes_,_delay_.")

    st.dataframe(data.style.format(precision=0))

with features:
    st.header("Is there a trend to give a car back on time or not?")
    back_on_time_fig = plt.figure(figsize=(10,4))
    sns.countplot(x="delay", data=data)
    st.pyplot(back_on_time_fig)
    st.markdown("**_As we see most of the time people postpone to bring a car back_**")

with features:
    st.header("How long should the minimum delay be?")
    st.subheader("_Back late_")
    st.write(back_late)
    avg_hours = round(mean(back_late['delay_hours']))
    st.write(f"_On average the delay is {avg_hours} hours. So now, we can assume that_ "
             f"_we need to make delay time for {avg_hours} hours_")

    st.caption("Delay = 3 hours")

    def check_avg(df, avg, max_val):
        less = avg + 1
        less_than_avg = df.loc[df['delay_hours'] < less]
        more_than_avg = df.loc[(df['delay_hours'] > avg) & (df['delay_hours'] < max_val)]
        x1 = less_than_avg['delay_hours']
        x2 = more_than_avg['delay_hours']
        y1 = sum(x1)
        y2 = sum(x2)
        fig = px.pie(values=[y1, y2], names=[f"<{less}", f">{avg} & <{max_val}"])
        return fig

    st.plotly_chart(check_avg(back_late,3,24))
    st.write("_So now we can take a look only at the delays that are higher than 3 hours_")

    def define_new_avg(df, avg, max_val):
        new_avg = df.loc[(df['delay_hours'] > avg) & (df['delay_hours'] <max_val)]
        high_avg_hours = round(mean(new_avg['delay_hours']))
        return (f"The average between {avg} and {max_val} hours is {high_avg_hours}")

    st.write(define_new_avg(back_late,3,24))

    st.caption("Delay = 9 hours")
    st.plotly_chart(check_avg(back_late,9,24))
    st.write("_Now we can say that the delay for 9 hours sounds good, but it sounds a lot,_ "
             "_so we can see if we can find better delay time that is more than 3 hours but less than 9_")

    st.write(define_new_avg(back_late,3,9))
    st.caption("Delay = 5 hours")
    st.plotly_chart(check_avg(back_late,5,24))
    st.write("_The percentage looks almost the same, just to try out if we can find something better than 5_")

    st.caption("Delay = 6 hours")
    st.plotly_chart(check_avg(back_late,6,24))
    st.write("**_According to this pie chart we see that 6 hours as a delay is enough_**")

    st.write("Let's check if there are delays for days")

    delay = px.pie(count, values='quantity', names='days')
    st.plotly_chart(delay)
    st.write("_As there's not that much cases of delays in days, we don't need to take into consideration option_ "
             "_of postponing for days_")

    st.write("It is still interesting to know what is the percentage of such big delays")
    st.caption("Delay for days")
    days_delay = px.pie(count_days, values='quantity', names='days')
    st.plotly_chart(days_delay)

    delay_days = back_late.loc[back_late["delay_days"] != 0.0]
    med_days = median(delay_days['delay_days'])
    st.write(f"The average delay in days is {med_days} day")

with features:
    st.header("Should we enable the feature for all cars or only Connect cars?")
    connect_mobile_fig = plt.figure(figsize=(10,4))
    sns.countplot(x="checkin_type", data=data, palette='husl')
    st.pyplot(connect_mobile_fig)

    st.write("**1. We can check which one of the check-in types has more tendency to be late for check-in**")
    st.caption("Mobile - check in ")
    mobile_checkin = plt.figure(figsize=(10,4))
    sns.countplot(x="delay", data=mobile_data)
    st.pyplot(mobile_checkin)
    st.caption("Connect - check in")
    connect_checkin = plt.figure(figsize=(10,4))
    sns.countplot(x="delay", data=connect_data)
    st.pyplot(connect_checkin)
    st.write("_As we see, both of them have tendency to be late. So, now we ned to detect if we should make the_ "
             "_same time of delay for Connect and Mobile-assigned cars_")

    st.write("**2. Is the average delay time is the same for Connect and mobile cars?**")
    avg_hours_connect = round(mean(back_late_connect['delay_hours']))
    st.write(f"On average the delay for Connect cars is {avg_hours} hours. So now, we can assume that we need to make delay time for "
                f"Connect cars {avg_hours} hours")
    st.caption("Delay connect = 3 hours")
    st.plotly_chart(check_avg(back_late_connect,3,24))
    st.write("**_According to this pie chart taking a delay time in 3 hours will be more than enough_**")

    avg_hours_mobile = round(mean(back_late_mobile['delay_hours']))
    st.write(f"On average the delay for Mobile cars is {avg_hours} hours. So now, we can assume that we need to make delay time for "
            f"Mobile cars - {avg_hours} hours")
    st.caption("Delay mobile = 3 hours")
    st.plotly_chart(check_avg(back_late_mobile,3,24))
    st.write("_According to this pie chart delay in 3 hours is not enough, so we can try the delay of 7 hours,_ "
             "_according to the calculation in the second part_ ")

    st.caption("Delay mobile = 7 hours")
    st.plotly_chart(check_avg(back_late_mobile,7,24))
    st.write("**_According to this pie chart we should make 7 hours delay for cars which rental_ "
             "_agreement was signed on the owner's smartphone_**")

with features:
    st.header("How often are drivers late for checkin?")
    checkin_time = plt.figure(figsize=(10,4))
    sns.countplot(x="checkin_time", data=checkin,palette='husl')
    st.pyplot(checkin_time)
    st.write("**_According to this plot it's pretty rare for drivers to be late for checkin_ "
             "_if there's another car waiting_**")
    st.subheader("_Checkin late_")
    st.dataframe(checkin_late)
    avg_hours_late = round(mean(checkin_late['checkin_late_hours']))
    st.write(f"Average late check-in hours {avg_hours_late}")
    st.caption("Late check in = 4 hours")
    st.plotly_chart(check_avg(checkin_late,4,24))

    st.caption("Check-in late - hours description")
    checkin_late_fig = px.pie(count_checkin, values='quantity', names='hours')
    st.plotly_chart(checkin_late_fig)
    st.write("**_If it still happens that drivers are late for check-in when another drivers are waiting on average "
             "the delay takes 4 hours_**")

    st.subheader("Conclusion: _According to all the delay buffers that we can use there could be less canceled rentals,_ "
                 "_thus more revenue_")

with predictions:
    st.header("The price prediction")
    st.write("Using this form you can easily detect the price for car according to all her features")

