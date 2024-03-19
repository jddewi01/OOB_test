# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 15:28:05 2024

@author: 240126034
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
#import io

st.sidebar.title('Upload CSV File') #title of the sidebar in the app
csv_file = st.sidebar.file_uploader("Choose a CSV file", type="csv") #next 2 lines prompt a user input of a file
csv_file2 = st.sidebar.file_uploader("Choose another CSV file", type="csv")

if csv_file and csv_file2:
    df = pd.read_csv(csv_file) # setting a variable that reads the inputed csv files
    df2 = pd.read_csv(csv_file2)
    
    # Convert the 'timestamp' column into time
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df2['timestamp'] = pd.to_datetime(df['timestamp'])
    df['Time'] = (df['timestamp'] - df['timestamp'].iloc[0]).dt.total_seconds()
    df2['Time'] = (df['timestamp'] - df['timestamp'].iloc[0]).dt.total_seconds()

    df = df.rename(columns={'TL28_DD::Erd_Drive_SpeedSensorBasket' : 'Basket Speed', 'TL28_DD::Erd_AccelerometerVirtualPoint1XDisplacement': 'VP1X',
                       'TL28_DD::Erd_AccelerometerVirtualPoint1YDisplacement': 'VP1Y', 'TL28_DD::Erd_AccelerometerVirtualPoint1ZDisplacement' : 'VP1Z',
                       'TL28_DD::Erd_AccelerometerVirtualPoint2XDisplacement' : 'VP2X', 'TL28_DD::Erd_AccelerometerVirtualPoint2YDisplacement' : 'VP2Y',
                       'TL28_DD::Erd_AccelerometerVirtualPoint2ZDisplacement' : 'VP2Z', 'TL28_DD::Erd_AccelerometerVirtualPoint3XDisplacement' : 'VP3X',
                       'TL28_DD::Erd_AccelerometerVirtualPoint3YDisplacement' : 'VP3Y', 'TL28_DD::Erd_AccelerometerVirtualPoint3ZDisplacement' : 'VP3Z',
                       'TL28_DD::Erd_AccelerometerReportedRotationAmplitude' : 'Wobble Angle'})
    #renaming some of the columns of data we want to make it easier on the user experience 
    df2 = df2.rename(columns={'TL28_DD::Erd_Drive_SpeedSensorBasket' : 'Basket Speed File 2', 'TL28_DD::Erd_AccelerometerVirtualPoint1XDisplacement': 'VP1X File 2',
                       'TL28_DD::Erd_AccelerometerVirtualPoint1YDisplacement': 'VP1Y File 2', 'TL28_DD::Erd_AccelerometerVirtualPoint1ZDisplacement' : 'VP1Z File 2',
                       'TL28_DD::Erd_AccelerometerVirtualPoint2XDisplacement' : 'VP2X File 2', 'TL28_DD::Erd_AccelerometerVirtualPoint2YDisplacement' : 'VP2Y File 2',
                       'TL28_DD::Erd_AccelerometerVirtualPoint2ZDisplacement' : 'VP2Z File 2', 'TL28_DD::Erd_AccelerometerVirtualPoint3XDisplacement' : 'VP3X File 2',
                       'TL28_DD::Erd_AccelerometerVirtualPoint3YDisplacement' : 'VP3Y File 2', 'TL28_DD::Erd_AccelerometerVirtualPoint3ZDisplacement' : 'VP3Z File 2',
                       'TL28_DD::Erd_AccelerometerReportedRotationAmplitude' : 'Wobble Angle File 2'})
    updated_columns = ['Basket Speed', 'VP1X', 'VP1Y', 'VP1Z', 'VP2X', 'VP2Y', 'VP2Z', 'VP3X', 'VP3Y', 'VP3Z', 'Wobble Angle', 'Time']
    updated_columns2 = ['Basket Speed File 2', 'VP1X File 2', 'VP1Y File 2', 'VP1Z File 2', 'VP2X File 2', 'VP2Y File 2', 'VP2Z File 2', 'VP3X File 2', 'VP3Y File 2', 'VP3Z File 2', 'Wobble Angle File 2', 'Time']
    updated_df = df[updated_columns]
    updated_df2 = df2[updated_columns2]
    columns_to_plot = st.sidebar.multiselect('Select columns to plot', updated_df.columns) #dropdown bar that prompts the user to pick want data they want on the graph
    columns_to_plot2 = st.sidebar.multiselect('Select variables to plot', updated_df2.columns)
    title = st.sidebar.text_input('Enter a title for your chart')
    scale = st.sidebar.number_input('Y axis Scale')
    time = df['Time']
    time2 = df2['Time']
    if st.button('Plot'):
       fig, ax1 = plt.subplots() #creating the primary axis
       ax2 = ax1.twinx()
       for column in columns_to_plot: #looking into both variables of user selected columns
         if column == 'Basket Speed':
           # Create graph with secondary y-axis
           ax2.plot(time,df['Basket Speed'], label ='Basket Speed', color = 'navy') #plotting basket speed and setting the label
         elif column != 'Basket Speed':
           
           ax1.plot(time, df[column], label = column) #plotting the rest of the columns on the primary axis
           
       for column2 in columns_to_plot2:
          if column2 == 'Basket Speed File 2':
              ax2.plot(time2,df2['Basket Speed File 2'], label = 'Basket Speed File 2', color = 'dimgray')
          elif column2 != 'Basket Speed File 2':
              ax1.plot(time2,df2[column2], label = column2)
    
       ax1.set_ylabel('Displacement(in x 1000) - Wobble Angle (deg x 1000)') #making axis labels 
       ax2.set_ylabel('Basket Speed (RPM)')
       ax1.set_xlabel('Time (sec)')
       ax2.set_ylim(0,1000) # making the limits on the secondary axis 
       ax1.set_xlim(0,350)
       ax1.set_ylim(0, scale) #setting min to 0 but allowing for any max limit based on the data
       ax1.grid() #adds grid lines to the primary axis ONLY
       lines, labels = ax1.get_legend_handles_labels()
       lines2,labels2 = ax2.get_legend_handles_labels() # grabbing the lines and labels and then putting the legend below the graph with a shadow and 5 columns per row
       ax2.legend(lines + lines2, labels + labels2, loc= 'upper center', bbox_to_anchor=(0.5,-.05),fancybox=True, shadow = True, ncol = 5)
       
       #Adjust layout
       #plt.tight_layout()
       #save it to a BytesIO object
       plt.title(title)
       st.pyplot(fig)
       
       #buf = io.BytesIO()
       #plt.savefig(buf, format='png')
       #buf.seek(0)

       # Use st.download_button to download the image file
       #st.download_button(
         #label="Download plot",
         #data=buf,
         #file_name='plot.png',
         #mime='image/png'
         #)

        
