# Copyright (c) 2025, a and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_to_date, today, date_diff


class EmployeeOvertimeCalculation(Document):
    
    def validate(self):
        
        start_date=self.start_date
        end_date=self.end_date
        employee_name=self.employee_name
        temp_week_hr=0
        total_present=0
        attendace="Present"
        weekend_hr=0
        total_hr=0
        
        
        
        
        
        # Important  Working code
        # overtime_data = frappe.db.sql("""
		# 								SELECT hours, activity_type 
		# 								FROM `tabTimesheet Detail` 
		# 								WHERE activity_type = %s
		# 							""", ("Communication",), as_dict=True)  
        # for row in overtime_data:
        #     self.append("child_table",{
		# 		"name1":row.activity_type,
    	# 		"hr":row.hours
		# 	})      
        # for row in overtime_data:
        #     week_hr =row.hours + week_hr
        
        # self.week_hr=week_hr



        query = """
                SELECT activity_type, hours, custom_week_day,from_time 
                FROM `tabTimesheet Detail` 
                WHERE from_time BETWEEN %s AND %s
            """
            
        overtime_data = frappe.db.sql(query, (start_date, end_date), as_dict=True)
        
        for row in overtime_data:
            self.append("child_table",{
				"activity_type":row.activity_type,
    			"hr":row.hours,
                "date":row.from_time,
                "weekday":row.custom_week_day
             
       
			}) 
        for row in overtime_data:
            total_hr =row.hours + total_hr       
        self.custom_total_hours=total_hr
        
        temp_date_difference=date_diff(end_date, start_date)
        self.date_difference =temp_date_difference +1
        
        for row in overtime_data:
            if row.custom_week_day =="No":           
                weekend_hr +=row.hours
            self.custom_weekend=weekend_hr
        for row in overtime_data:
            if row.custom_week_day =="Yes":           
                temp_week_hr +=row.hours
            self.week_hr=temp_week_hr
            
            
            
            
            
        
        attendace_record=frappe.get_all("Attendance",
                                        filters={
                                            "employee_name":employee_name,
                                            "attendance_date":["between",[start_date,end_date]]     
                                        },
                                        fields=["employee_name","status","attendance_date"]       
        )
        for record in attendace_record:
            # print(record)
            if record["status"]=="Present":
                total_present = total_present + 1
        print(total_present)
        
            
                
    
        
        
        
        
   
        # count_query = """
        #             SELECT COUNT(*) AS count
        #             FROM `tabAttendance` 
        #             WHERE attendance_date BETWEEN %s AND %s 
        #             AND employee_name = %s
        #             AND status= %s
        #         """
        # overtime_data = frappe.db.sql(count_query, (start_date, end_date,employee_name,attendace), as_dict=True)
        # count_value = overtime_data[0]["count"]
        # # frappe.msgprint(f"Total attendance records: {count_value}")
        # self.total_present_days=count_value +1
        
        # # calculation total present days
        # for i in overtime_data:
            


        
        
        # get base salary of employee
        latest_entry = frappe.get_all(
                                        "Salary Structure Assignment",
                                        filters={"employee_name": employee_name},  # Optional filter
                                        fields=["base", "creation"],  # Fetch required fields
                                        order_by="creation DESC",  # Order by creation date (latest first)
                                        limit_page_length=1  # Fetch only the latest entry
                                    )
        if latest_entry:
            latest_doc = latest_entry[0]
          
            self.base_salary=latest_doc["base"]
            # frappe.msgprint(f"Latest Entry: {latest_doc['base']} created on {latest_doc['creation']}")
        else:
            frappe.msgprint("No records found.")
            
        
        
        
        
        # for entry in overtime_data:
        #     frappe.msgprint(f"Activity: {entry['activity_type']}, Hours: {entry['hours']}, Weekday: {entry['custom_week_day']}")





        
        #  not working    
        # overtime_data = frappe.get_list(
        #     "Timesheet Detail",
        #     filters={"from_time": ["between", [start_date, end_date]]},
        #     fields=["activity_type", "hours","custom_week_day"]        
        # )
        # for row in overtime_data:
        #     frappe.msgprint({row['hours']})
        
        
        
#         for row in overtime_data:
#             self.append("child_table",{
# 				"name1":row.activity_type,
#     			"hr":row.hours
# 			}) 
  
        
#         for row in overtime_data:
#             week_hr =row.hours + week_hr
        
#         self.week_hr=week_hr
    

        
        
        
        
        # frappe.msgprint(employee_name)
        # frappe.msgprint(doc)
        
        # list=frappe.get_list("Timesheet", filters={"employee_name": employee_name,"start_date": ["between", [start_date, end_date]]})
        # for emp in list:
        #     frappe.msgprint(f"{emp.name}: abc")
# )
            
        
        

        
        return

