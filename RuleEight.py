import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Data import data_obj

class RuleEight:
    def __init__(self):
        self.score, self.conflicts_df, self.plot_arr = self.compute()

    def compute (self):
        score = None
        conflicts_df = None
        plot_arr = None

        def specific_examiners():
            df = pd.concat([data_obj.examiner, data_obj.start_date, data_obj.course_name], axis=1)

            # data is exploded by putting each professors into seperate rows
            exploded_df = df.explode('1. & 2. Pruefer')


            grouped_df = exploded_df.groupby('1. & 2. Pruefer').agg(
                {'Lehrveranstaltung': list, 'start_date': list}).reset_index()

            # data is filtered based on the specific examiners
            filtered_df = grouped_df[grouped_df['1. & 2. Pruefer'].isin(data_obj.special_examiners['Professor'])]


            professor_exams = {}
            for row in filtered_df.itertuples(index=False):
                professor = row[0]
                exams = {}
                for date, exam in zip(row[2], row[1]):
                    if date in exams:
                        exams[date].append(exam)
                    else:
                        exams[date] = [exam]
                professor_exams[professor] = exams

            df_final = pd.DataFrame(
                {'Professor': list(professor_exams.keys()), 'Exams': list(professor_exams.values())})

            def count_days_supervised(exams):
                dates = list(exams.keys())
                # Find how many days professors have to visit campus
                num_days = pd.DataFrame({'date': dates})['date'].dt.day.nunique()
                return num_days

            def count_exams_supervised(courses):
                exams = set()
                for course_list in courses.values():
                    exams.update(course_list)
                num_exams = len(exams)
                return num_exams

            def calculate_each_score(days, number_of_exams):
                if number_of_exams == 1:
                    return 1
                else:
                    return 1-((days-1)/(number_of_exams-1))

            # Find how many days professors have to visit campus
            df_final["Days"] = df_final["Exams"].apply(count_days_supervised)
            # Find how many exams professors have to supervise
            df_final["Exam Numbers"] = df_final["Exams"].apply(count_exams_supervised)
            # Calculate score
            df_final["Score"] = df_final.apply(lambda i: calculate_score(i["Days"], i["Exam Numbers"]),axis=1)

            print(df_final)

        specific_examiners()
        return score, conflicts_df, plot_arr


RuleEight = RuleEight()