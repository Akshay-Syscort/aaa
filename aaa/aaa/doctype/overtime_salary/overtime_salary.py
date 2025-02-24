# Copyright (c) 2025, a and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document



class overtimesalary(Document):
    
    
    # def validate(self):
    #     total_working_days=float(self.total_working_days)
    #     absent_days=float(self.absent_days)
        
        
    #     temp_total_present_days = total_working_days - absent_days
    #     frappe.msgprint(temp_total_present_days)
        
        
    def validate(self):
        employee_name=self.employee_name
       
        
    
        
        
        
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
            # print(self.base_salary)
        
        
        
    def before_save(self):
            print(self.total_working_days)
            print(self.absent_days)
            float_total_working_days=float(self.total_working_days)
            float_absent_days=float(self.absent_days)
            print(float_total_working_days)
            print(float_absent_days)

            
            
          
            
            
            # Attendance Calculation
            float_present_day=float_total_working_days - float_absent_days
            print(float_present_day)
            self.total_present_days=float_present_day
            
            #Normal Overtime Calculation
            normal_ot=float(self.normal_ot)  
            temp_normal_overtime=(float(self.base_salary)/30/8)
            #mul 1.2
            temp_normal_overtime1=temp_normal_overtime*1.2
            #mul* normal ot
            temp_normal_overtime2=temp_normal_overtime1* normal_ot
            self.normal_overtime_amount=temp_normal_overtime2
          
            
      
            #holiday Overtime
            holiday_ot=float(self.holiday_ot)
            # mul *1.5
            temp_normal_overtime3=temp_normal_overtime*1.5
            temp_normal_overtime4=temp_normal_overtime3 * holiday_ot
            self.holiday_overtime_amount=temp_normal_overtime4
            
            
            
          
            
            
            #Holiday Overtime
            # holiday_ot=float(self.holiday_ot)
            # print(holiday_ot)
            
            
            
            
            
            
            
            
            
        # Calculate present_days
        # present_days = self.total_working_days - self.absent_days
        # self.total_present_days=present_days
        
        
        # if latest_entry:
        #     latest_doc = latest_entry[0]
        #     self.base_salary=latest_doc["base"]
        #     frappe.msgprint(latest_doc)
            
        #     self.base_Salary=temp_base_salary
            
        # frappe.msgprint(total_working_days)
        # frappe.msgprint(absent_days)

        
        # total_present_days = self.total_working_days - self.absent_days
        # frappe.msgprint(total_present_days)
        
        
        
        # #Overtime Calculation
    
        
        # temp_value=float_base_salary/30/8
        # frappe.msgprint(temp_value)
        
        # frappe.msgprint(temp1)
        # temp= (int_base_salary/30)/8
        # var=float(temp)
        
        # temp_normal_overtime =(var * 1.2)* float(normal_ot)
        # # print(temp_normal_overtime)
        # self.normal_overtime_amount=temp_normal_overtime
        
        # temp_holiday_overtime=(var * 1.2)* float(holiday_ot)
        # self.holiday_overtime_amount=temp_holiday_overtime
    
    
        
        
    def before_submit(self):
        additional_salary_normal_overtime= frappe.get_doc({
            "doctype":"Additional Salary",
            "employee":self.employee,
            "salary_component":"Normal overtime",
            "amount":self.normal_overtime_amount,
            "payroll_date": self.posting_date
            
        })
        additional_salary_normal_overtime.save()
        additional_salary_normal_overtime.submit()
        
        additional_salary_holiday_overtime= frappe.get_doc({
            "doctype":"Additional Salary",
            "employee":self.employee,
            "salary_component":"Holiday overtime",
            "amount":self.holiday_overtime_amount,
            "payroll_date": self.posting_date
            
        })
        additional_salary_holiday_overtime.save()
        additional_salary_holiday_overtime.submit()
        
        
        
        