import streamlit as st
import pandas as pd
import json
import ratemyprofessor
from streamlit_echarts import st_echarts
import plotly.express as px

#Load JSON data from file
with open("complete.json", "r") as json_file:
    data = json.load(json_file)

#Load data into dataframe
df = pd.DataFrame(data)

#Bool variables for if statements
compare = 0
title = 0

#Streamlits columns
col1, col2 = st.columns(2)
col3, col4 = st.columns([0.6, 0.4])

#Variables for ratings
rating = 0.0
formattedRating = "N/A"

#Variables for difficulty
difficulty = 0.0
formattedDifficulty = "N/A"

#Variables for would take again
again = 0.0
formattedAgain = "N/A"

#Styles for titles and headers
title_style = 'text-align: center;'
header_style = 'text-align: center; color: #00853E;'
subheader_style = 'color: #00853E;'

#Function to create colored box
def colored_box(value, color):
    return f'<div style="background-color:{color}; padding:10px; border-radius:10px; max-width: 80px; text-align: center;">{value}</div>'

#Function to check for blank fields or matching fields
def checkFields(name1, name2):
    return name1.strip().lower() == name2.strip().lower() if name1 and name2 else False

########Function to get Rate My Professors Data########
def rateMyProfessor(professor_name):
    professor = ratemyprofessor.get_professor_by_school_and_name(ratemyprofessor.get_school_by_name("University of North Texas"), professor_name)
    if professor is None:
        st.write("Professor Not Found!")
    else: 
        if compare == 1:
            st.title(f"Professor {professor_name}")
        else:    
            st.title(f"Professor {professor_name} of the %s Department." % (professor.department))
        #Get rating
        if professor.rating == -1:
            rating = float(-1)
            formattedRating = f"N/A"
        else:          
            rating = float(professor.rating)
            formattedRating = "%.1f / 5.0" % professor.rating
        #Get difficulty
        if professor.difficulty == -1:
            difficulty = float(-1)
            formattedDifficulty = f"N/A"
        else:    
            difficulty = float(professor.difficulty)
            formattedDifficulty = "%.1f / 5.0" % professor.difficulty
        #Get would take again
        if professor.would_take_again is None:
            again = float(0)
            formattedAgain = f"0%"
        elif professor.would_take_again == -1:
            again = float(-1)
            formattedAgain = f"N/A"    
        else:    
            again = float(professor.would_take_again)
            formattedAgain = f"{round(professor.would_take_again, 1)}%"
        #Colored box cases for rating
        st.header("Rating")
        if 0 <= rating <= 2.0:
            st.markdown(colored_box(formattedRating, '#eb2d3a'), unsafe_allow_html=True)
        elif 2.0 < rating < 4.0:
            st.markdown(colored_box(formattedRating, '#ffec00'), unsafe_allow_html=True)
        elif rating >= 4.0:
            st.markdown(colored_box(formattedRating, '#50b458'), unsafe_allow_html=True)
        elif rating < 0:
            st.markdown(colored_box(formattedRating, '#808588'), unsafe_allow_html=True)     
        #Colored box cases for difficulty
        st.header("Difficulty")
        if 0 <= difficulty <= 2.0:
            st.markdown(colored_box(formattedDifficulty, '#50b458'), unsafe_allow_html=True)
        elif 2.0 < difficulty < 4.0:
            st.markdown(colored_box(formattedDifficulty, '#ffec00'), unsafe_allow_html=True)
        elif difficulty >= 4.0:
            st.markdown(colored_box(formattedDifficulty, '#eb2d3a'), unsafe_allow_html=True)
        elif difficulty < 0:
            st.markdown(colored_box(formattedDifficulty, '#808588'), unsafe_allow_html=True)     
        #Colored box cases for would take again
        st.header("Would Take Again")
        if 0 <= again <= 50:
            st.markdown(colored_box(formattedAgain, '#eb2d3a'), unsafe_allow_html=True)
        elif 50 < again < 70:
            st.markdown(colored_box(formattedAgain, '#ffec00'), unsafe_allow_html=True)
        elif again >= 70:
            st.markdown(colored_box(formattedAgain, '#50b458'), unsafe_allow_html=True)
        elif again < 0:
            st.markdown(colored_box(formattedAgain, '#808588'), unsafe_allow_html=True)    

#Function to display Grades in Bar Graph
def gradeJSON(professor_name, class_name):
    # Filter the DataFrame for the specific professor and class
    filtered_data = df[(df["prof"].str.contains(professor_name, case=False)) & (df["desc"].str.contains(class_name, case=False))]

    if not filtered_data.empty:
        # Combine grades for all terms
        combined_grades = {
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 0,
            "F": 0,
            "W": 0
        }

        #Adds up grades from all the terms
        for index, row in filtered_data.iterrows():
            term_grades = row["grades"]
            for grade, count in term_grades.items():
                # Convert grades to integers before addition
                if grade in combined_grades:
                    combined_grades[grade] += int(count)

        # Create a bar chart for combined grades using Plotly
        df_combined = pd.DataFrame({
            'Grade': list(combined_grades.keys()),
            'Count': list(combined_grades.values())
        })
        #Color for each bar
        fig = px.bar(
            df_combined, x='Grade', y='Count',
            color='Grade',
            labels={'Count': 'Count', 'Grade': 'Grades'},
            color_discrete_map={'A': '#50b458', 'B': '#ffec00', 'C': 'orange', 'D': 'maroon', 'F': '#eb2d3a', 'W': 'grey'},
        )
        if compare == 0:
            fig.update_layout(width=700)
        else:
            fig.update_layout(width=350)        
        st.plotly_chart(fig)

    else:
        st.write("No matching results found for the specified professor and class.")

#Function to display Grades in Pie Graph
def pi(professor_name, class_name):
            ##########################################Pie Chart#################################################
            #Pass/Fail/Drop grades
            filtered_data = df[(df["prof"].str.contains(professor_name, case=False)) & (df["desc"].str.contains(class_name, case=False))]

            if not filtered_data.empty:
                # Combine grades for all terms
                combined_grades = {
                    "A": 0,
                    "B": 0,
                    "C": 0,
                    "D": 0,
                    "F": 0,
                    "W": 0
                }

                for index, row in filtered_data.iterrows():
                    term_grades = row["grades"]
                    for grade, count in term_grades.items():
                        # Convert grades to integers before addition
                        if grade in combined_grades:
                            combined_grades[grade] += int(count)

                pass_fail_drop = {
                    "Pass": ["A", "B", "C"],
                    "Fail": ["D", "F"],
                    "Drop": ["W"]
                }
                pass_count = fail_count = drop_count = 0
                #Combines Pass/Fail/Drop grades
                for grade, count in combined_grades.items():
                    if grade in pass_fail_drop["Pass"]:
                        pass_count += count
                    elif grade in pass_fail_drop["Fail"]:
                        fail_count += count
                    elif grade in pass_fail_drop["Drop"]:
                        drop_count += count
                #Create the pie chart
                options = {
                    "title": {"text": "Pass/Fail/Drop", "left": "center", "top": "37%"},
                    "tooltip": {"trigger": "item", "top": "37%"},
                    "legend": {"orient": "vertical", "left": "left", "top": "37%"},
                    "series": [
                        {
                            "name": "Pass/Fail/Drop",
                            "type": "pie",
                            "radius": "70%",
                            "top": "40%",
                            "data": [
                                {"value": pass_count, "name": "Pass", "itemStyle": {"color": "#50b458"}},
                                {"value": fail_count, "name": "Fail", "itemStyle": {"color": "#eb2d3a"}},
                                {"value": drop_count, "name": "Drop", "itemStyle": {"color": "#ffec00"}},
                            ],
                            "emphasis": {
                                "itemStyle": {
                                    "shadowBlur": 10,
                                    "shadowOffsetX": 0,
                                    "shadowColor": "rgba(0, 0, 0, 0.5)",
                                }
                            },
                        }
                    ],
                }

                # Render the pie chart
                st_echarts(
                    options=options, height="600px"
                )
            else:
                st.write("")

#Sidebar
st.sidebar.title("Scrape My Professors")
st.sidebar.markdown('<h2 style="{}">(UNT Edition)</h2>'.format(subheader_style), unsafe_allow_html=True)
st.sidebar.header("Search for a Professor or Class")
#Case for compare checkbox
if st.sidebar.checkbox("Compare"):
    professor_name = st.sidebar.text_input("Professor Name", placeholder = "First Last")
    class_name = st.sidebar.text_input("Class Name", placeholder = "Class Name")
    professor_name2 = st.sidebar.text_input("(Additional) Professor Name", placeholder = "First Last")
    class_name2 = st.sidebar.text_input("(Additional) Class Name", placeholder = "Class Name")
    if st.sidebar.button("Compare"):
        title = 1
        #Checks for duplicates
        if checkFields(professor_name, professor_name2):
            st.title("Fields are the same!")
        elif checkFields(class_name, class_name2):
            st.title("Fields are the same!")
        else:    
            compare = 1
            with col1:
                if professor_name:
                    #Calls functions for data
                    rateMyProfessor(professor_name)
                    if not class_name:
                        st.subheader(f"Student Grades for Professor {professor_name}")
                    else:
                        st.subheader(f"Student Grades for {class_name} by Professor {professor_name}")    
                    gradeJSON(professor_name, class_name)
                    pi(professor_name, class_name)
                elif class_name:
                    st.subheader(f"Student Grades for {class_name}")
                    gradeJSON(professor_name, class_name)   
                    pi(professor_name, class_name) 
            with col2:         
                if professor_name2:
                    #Calls functions for data
                    rateMyProfessor(professor_name2)
                    if not class_name2:
                        st.subheader(f"Student Grades for Professor {professor_name2}")
                    else:
                        st.subheader(f"Student Grades for {class_name2} by Professor {professor_name2}")    
                    gradeJSON(professor_name2, class_name2)
                    pi(professor_name2, class_name2)
                elif class_name2:
                    st.subheader(f"Student Grades for {class_name2}")
                    gradeJSON(professor_name2, class_name2)  
                    pi(professor_name2, class_name2)   
else:    
    professor_name = st.sidebar.text_input("Professor Name", placeholder = "First Last")
    class_name = st.sidebar.text_input("Class Name", placeholder = "Class Name")
    if st.sidebar.button("Search"):
        title = 1
        if professor_name:
            #Calls functions for data
            with col3:
                rateMyProfessor(professor_name)
            if not class_name:
                st.subheader(f"Student Grades for Professor {professor_name}")
            else:
                st.subheader(f"Student Grades for {class_name} by Professor {professor_name}")    
            gradeJSON(professor_name, class_name)
            #Calls functions for data
            with col4:
                pi(professor_name, class_name)
        elif class_name:
            st.subheader(f"Student Grades for {class_name}")
            gradeJSON(professor_name, class_name)
            with col4:  
                pi(professor_name, class_name)  

#To make title disappear
if title == 0:
    st.markdown('<h1 style="{}">Welcome to Scrape My Professors</h1>'.format(title_style), unsafe_allow_html=True)
    st.markdown('<h2 style="{}">(UNT Edition)</h2>'.format(header_style), unsafe_allow_html=True)
    st.markdown('<h1 style="{}">Enter Professor or Class Name</h1>'.format(title_style), unsafe_allow_html=True)           