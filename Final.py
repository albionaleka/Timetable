import customtkinter
from tkinter import END
from CTkListbox import * 
import os
import csv

customtkinter.set_appearance_mode("system")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Timetable")
        self.geometry("800x600")
        self.iconbitmap('./img/logo.ico')
        self.columnconfigure(1, weight=100)
        self.columnconfigure(2, weight=100)
        self.columnconfigure(3, weight=100)

        self.title = customtkinter.CTkLabel(self, text="TIMETABLE 📃", font=('Verdana', 20))
        self.title.grid(row=0, column=0, pady=20, columnspan=4)

        self.file_entry = customtkinter.CTkEntry(self, placeholder_text="Filepath", width=560)
        self.file_entry.grid(row=1, column=1, pady=10, columnspan=3)

        self.button = customtkinter.CTkButton(self, text="File path", command=self.file_path)
        self.button.grid(row=1, column=0, pady=10, padx=10)

        self.year_button = customtkinter.CTkButton(self, text='Year', command=self.year)
        self.year_button.grid(row=2, column=0)

        self.year_box = customtkinter.CTkComboBox(self, values=['Year', '1', '2', '3', '4', '5'])
        self.year_box.grid(row=2, column=1, padx=10, pady=10)

        self.department_button = customtkinter.CTkButton(self, text="Department", command=self.department)
        self.department_button.grid(row=2, column=2, pady=10)

        self.department_box = customtkinter.CTkComboBox(self, values=['Department', 'CHI', 'CS', 'ECE', 'ECON', 'EE', 'EECS', 'ENGR', 'FRE', 'GER', 'IE', 'ISE', 'LIFE', 'MATH', 'MGT', 'UNI'])
        self.department_box.grid(row=2, column=3, padx=20)

        self.display_button = customtkinter.CTkButton(self, text='Display', command=self.display)
        self.display_button.grid(row=3, column=1, pady=30)

        self.clear_button = customtkinter.CTkButton(self, text='Clear', command=self.clear)
        self.clear_button.grid(row=3, column=2, pady=30)

        self.save_button = customtkinter.CTkButton(self, text='Save', command=self.save)
        self.save_button.grid(row=3, column=3, pady=30)

        self.warnings_label = customtkinter.CTkLabel(self, text="Warnings: ", font=('Verdana', 14))
        self.warnings_label.grid(row=4, column=0, pady=10)

        self.warnings_text = customtkinter.CTkLabel(self, text="", width=1000)
        self.warnings_text.grid(row=4, column=1, pady=10, columnspan=3)

        self.courses_list = CTkListbox(self , command=self.add, width=750)
        self.courses_list.grid(row=5, column=0, pady=10, columnspan=4, padx=10, sticky='w')
        self.courses_list.insert(0, 'Courses')

        self.selected_courses_list = CTkListbox(self, width=750, command=self.delete)
        self.selected_courses_list.grid(row=6, column=0, pady=10, padx=10, columnspan=4, sticky='w')
        self.selected_courses_list.insert(0, 'Selected Courses')


    def file_path(self):
        filename = self.file_entry.get()

        if os.path.exists(filename):

            if os.path.isfile(filename):

                if filename.lower().endswith('.csv'):
                    print(filename)

                else:
                    self.warnings_text.configure(text="You picked a unsupported file format. Please pick a .csv file!")

            else:
                self.warnings_text.configure(text="You entered the path to a directory! Please choose a .csv file!")

        else:
            self.warnings_text.configure(text="The path provided doesn't seem to exist! Please check your input.")

    def filepath(self, filename):
        filename = self.file_entry.get()

        if os.path.exists(filename):

            if os.path.isfile(filename):

                if filename.lower().endswith('.csv'):
                    return
                
                else:
                    self.warnings_text.configure(text="You picked a unsupported file format. Please pick a .csv file!")

            else:
                self.warnings_text.configure(text="You entered the path to a directory! Please choose a .csv file!")

        else:
            self.warnings_text.configure(text="The path provided doesn't seem to exist! Please check your input.")


    def department(self):
        if self.department_box.get() != 'Department':
            print(self.department_box.get())

    
    def year(self):
        if self.year_box.get() != 'Year':
            print(self.year_box.get())


    def display(self):
        path = self.file_entry.get()
        self.filepath(path)
        
        with open(path, "r") as file:
            self.reader = csv.DictReader(file)
            data = list(self.reader)
            headers = self.reader.fieldnames

        dep = self.department_box.get()
        year = self.year_box.get()

        if dep == 'Department' and year == 'Year':
            self.warnings_text.configure(text='Please pick your department and/or year.')
            return

        self.courses_list.delete(1, 'end')

        if headers:
            header_dict = dict((header, header) for header in headers)
            data.insert(0, header_dict)

        if dep == 'Department' and year != 'Year':
            self.warnings_text.configure(text='')

            for row in data:
                values = []
                for value in row.values():
                    values.append(str(value))
                row_values = ', '.join(values)
                columns = row_values.split(', ')
                courses = columns[0]

                course_year = int(courses.split()[1][0])

                if course_year == int(year):
                    self.courses_list.insert('end', row_values)

        elif dep != 'Department' and year == 'Year':
            self.warnings_text.configure(text='')

            for row in data:
                values = []
                for value in row.values():
                    values.append(str(value))
                row_values = ', '.join(values)
                if row_values.startswith(dep):
                    self.courses_list.insert('end', row_values)

        else:
            self.warnings_text.configure(text='')
            
            for row in data:
                values = []
                for value in row.values():
                    values.append(str(value))
                row_values = ', '.join(values)
                columns = row_values.split(', ')
                courses = columns[0]

                if row_values.startswith(dep):
                    course_year = int(courses.split()[1][0])
                    if course_year == int(year):
                        self.courses_list.insert('end', row_values)


    def clear(self):
        self.file_entry.delete(0, END)
        self.department_box.set('Department')
        self.year_box.set('Year')
        self.selected_courses_list.delete(1, END)
        self.courses_list.delete(1, END)
        self.warnings_text.configure(text='')
        file = open("timetable.csv", "w")
        file.truncate()
        file.close()


    def save(self):
        try:
            selected_courses = []
            for i in range(1, self.selected_courses_list.size()):
                selected_courses.append(self.selected_courses_list.get(i))

            with open('timetable.csv', 'w') as file:
                writer = csv.writer(file)

                for course in selected_courses:
                    writer.writerow([str(course)])
                
                self.warnings_text.configure(text="Timetable saved.")

        except:
            print("Error occurred.")


    def add(self, *args):
        if self.selected_courses_list.size() >= 7:
            self.warnings_text.configure(text="You cannot add more than 6 courses.")
            return

        self.selected_index = self.courses_list.curselection()
        if self.selected_index:
            self.selected_course = self.courses_list.get(self.selected_index)
            columns = self.selected_course.split(', ')

            for i in range(self.selected_courses_list.size()):
                added_course = self.selected_courses_list.get(i)
                added_columns = added_course.split(', ')

                if len(columns) < 4 or len(added_columns) < 4:
                    continue

                if self.selected_course == added_course:
                    self.warnings_text.configure(text="You have already added this course.")
                    return

                selected_schedules = columns[3].split()
                selected_days = columns[2].split()

                added_schedules = added_columns[3].split()
                added_days = added_columns[2].split()

                for added_day in added_days:
                    if added_day in selected_days:

                        for selected_schedule in selected_schedules:
                            split_schedule = selected_schedule.split('-')
                            if len(split_schedule) != 2:
                                self.warnings_text.configure(text="Invalid time format.")
                                continue

                            selected_start_time = split_schedule[0]
                            selected_end_time = split_schedule[1]
                            
                            for added_schedule in added_schedules:
                                split_schedule = added_schedule.split('-')
                                if len(split_schedule) != 2:
                                    self.warnings_text.configure(text="Invalid time format.")
                                    continue

                                added_start_time = split_schedule[0]
                                added_end_time = split_schedule[1]

                                if (selected_start_time < added_end_time and selected_end_time > added_start_time):
                                    self.warnings_text.configure(text=f"Courses have overlapping schedules. Cannot add {columns[0]}!")
                                    return

            self.selected_courses_list.insert(END, self.selected_course)
            self.warnings_text.configure(text=f'Added {columns[0]}')


    def delete(self, choice):
        choice = self.selected_courses_list.curselection()
        if choice != 0:
            self.selected_courses_list.delete(choice)
            self.warnings_text.configure(text='Removed selected course.')


app = App()
app.mainloop()
