import os
import json
import csv

class DataIngestor:
    def __init__(self, csv_path: str):
        # TODO: Read csv from csv_path
        with open(csv_path, 'r') as file:
            self.data = list(csv.DictReader(file))


        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]

    def get_data(self):
        return self.data
    
    def get_sort_order(self, question: str):
        if question in self.questions_best_is_min:
            return 'asc'
        elif question in self.questions_best_is_max:
            return 'desc'
        else:
            return None

#     # def a function that prints the frist 3 rows of the data
#     def print_first_3_rows(self):
#         print(self.data[:3])

# # create main that calls the function
# if __name__ == "__main__":
#     di = DataIngestor("../nutrition_activity_obesity_usa_subset.csv")
#     di.print_first_3_rows()
