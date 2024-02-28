# Deployment
Industrialization of a machine learning algorithm and automation of decision-making processes

my email: anastasia@phiskills.com

video-explanation: https://youtu.be/EqzPjo5J0fo

## Idea

When using Getaround, drivers book cars for a specific time period, from an hour to a few days long. They are supposed to bring back the car on time, but it happens from time to time that drivers are late for the checkout.

Late returns at checkout can generate high friction for the next driver if the car was supposed to be rented again on the same day: Customer service often reports users unsatisfied because they had to wait for the car to come back from the previous rental or users that even had to cancel their rental because the car wasn’t returned on time.

In order to mitigate those issues we’ve decided to implement a minimum delay between two rentals. A car won’t be displayed in the search results if the requested check-in or checkout times are too close to an already booked rental.

It solves the late checkout issue but also potentially hurts Getaround/owners revenues: we need to find the right trade off.

## Analyzing the file

So, now we can start reading our Excel file with the pandas function. And as we have state "canceled" that doesn't help us with anything, we can drop these rows

In our df we have a column delay_at_checkout_in_minutes that means difference in minutes between the rental end time requested by the driver when booking the car and the actual time the driver completed the checkout. Negative values mean that the driver returned the car in advance.

I already wanted to create new columns in this data frame that will give directly delay hours and delay minutes. For that it’s better to create a function. As we have values in column delay_at_checkout_in_minutes that are written in minutes, I’ll count how much hours of delay it takes to bring a car back.

Almost the same function to define the difference in minutes for bringing back.


## *1. Is there a trend to give a car back on time or not?*

And to answer this question I made a function define_back_on_time where I used if else condition, so if the value of the row is bigger than 0 than we can say that a car was late, if smaller = early, and if a value is NaN- on time.

To visualise the comparison between those 3 categories I used seaboard’s catplot. And we see that most of the time people postponed to bring a car back.

## *2. How long should the maximum delay be?*

For that, I created a new data frame by filtering data df by the column delay that equals late. Then decided to create a function define delay days as I noticed that there were hours in the column delay_hours that are more than 24, so it means that sometimes delays were higher than a day. So, it’s also important to take into consideration if we need to extend delay period for days.

We can save this data to csv for the future.

Then, with the help of module statistics, we can count the average amount of delay hours. That in-hour situation equals 3. 

So, now I was thinking that we can check how big is the difference between the average delay. 

By creating function check_avg and with using plotly we can see that mostly people still bring car back from 3 to 24 hours, so taking a delay period as 3 hours is not enough.

To try to find a new average according to a new condition, I created another function, define_new_avg, that counts the average in between this new condition.

So now we can try the average as 9. Finally, we see that the delay of 9 hours sounds good, but we can try to make it less to keep more profit for the company. That’s how now so we can try a better delay time that is more than 3 hours but less than 9.

Using our created function define_new_avg gave us 5. And the percentage looks almost the same, but just out of curiosity we can check 6 hours too. And 6 hours as a delay looks enough.

## *3. How regular are delays in days?*

Now, let’s analyze delays in days. For that, I created a simple data frame with days and their quantity. Using a pie chart from Plotly Express, we can say that there are not that many delays in days, so we don’t need to take into consideration the option of postponing for days.

It is still interesting to know what is the percentage of such big delays.

By the pie chart, we see that 60% of delays are 1 day, and if we count the average delays with the statistics module, it is 1 day.

## *4. Should we enable the feature for all cars or only Connect cars?*

With seaborn’s catplot we looked at the difference between checkin types. It’s preferable to make a rental agreement signed on the owner's smartphone.

But still, I would prefer to see if the average delay time is the same for Connect and mobile cars. We can save all the mobile and connect data to CSV files. 

By looking at both catplots for mobile and connect check-in, we notice that they both have a tendency to be late, but mobile check-in most of the time is late.
Next, we need to detect if we should make the same time of delay for Connect and Mobile-assigned cars. For that, I created new dfs by filtering the back_late df. This two datasets we can also save to a csv file.

On average, the delay for connect_type cars is 3 hours. By checking this average, taking a delay time of 3 hours is more than enough.

And for mobile_checkin type cars the average is also 3 hours. But as we decided previously a good delay period is 6 hours, here we can directly try to check it out. Looking at the pie chart we can try to make it a bit more.

And yes, 7 hours delay for cars which rental agreement was signed on the owner’s smartphone looks very fair.

## *5. How often are drivers late for check-in?*

For the check-in dataframe, I dropped all the nan values from the column … in the back_late df.

And created new column checkin_late that is the difference between columns delay_at_checkout_minutes and time_delta_with_previous_rental_in_minutes.

I decided to create functions to define late checkin hours and late checkin minutes. And a function to define checkin, so we can categorise if late checkin smaller than 0 it will be early, otherwise it’s late.

So, according to the plot it’s pretty rare for drivers to be late for checkin if there’s another car waiting.

But still, if we try to analyze what’s the average delay for late check-in, we’d see that it’s equal to 4 hours.

But if we look closer to the quantity of each hour for a late checkin, we’d see that 30% is 1 hour.

In conclusion, to all the delay buffers that we can use, there could be fewer canceled rentals, thus more revenue.


## Streamlit

After all the analysis I made a Streamlit app to present my work sufficiently. For that, I used some of the data frames that I saved earlier to the CSV files.


## ML

In addition to the above question, the Data Science team is working on pricing optimization. They have gathered some data to suggest optimum prices for car owners using Machine Learning.

So, I made a Machine Learning model to predict car rental prices according to different values. As it’s a simple linear regression model, I won’t spend a lot of time of going through each line.

Simply saying, we’re pre-processing our data.

Then, we split our df into X and y dfs. So we can normalize numeric and categorical features from X df.

The next step is to train_test_split and create pipelines for numeric and categorical features. Used ColumnTransformer to make a preprocessor object that describes all the treatment to be done. Preprocessing on train and test sets. And then train the model.

By doing regressor.score on train and test we see that the model is just right, as there's no overfitting, and the R2 score is significantly > 0.

Finally, we can make predictions based on training and test sets.

As we've standardized our features, we can use the regression coefficients to estimate each feature's importance for the prediction. Each coefficient can be linked with the name of the corresponding feature by digging into the different pipelines that were used to produce the final version of the X_train/X_test arrays.

The feature importance is related to the absolute values of the coefficients. We can also plot coefficients.

After predicting, we should export the model with the help of the module joblib, then import it to try it out later.

With an API, we also tried out our model, and the results are similar.


## API

As I mentioned API, I’ll tell you a few words about it. I used FastAPI as it’s very easy and quick. When you need to send data from a client (let's say, a browser) to your API, you send it as a request body.

First, I imported BaseModel from pydantic. Then, I declared my data model as a class that inherits from BaseModel. 
To add it to a path operation, declared its type as the model I created, body. Then in the function loaded my joblib file. And then did predict it with an input body.

By checking terminal we see that everything has worked without errors, if we open notebook we see the right output (the one that I showed you earlier). And if we go to the API’s localhost page /docs, we can see the documentation of our API.


