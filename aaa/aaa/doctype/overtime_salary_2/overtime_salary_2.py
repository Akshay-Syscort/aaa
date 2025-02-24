# Copyright (c) 2025, a and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class OvertimeSalary2(Document):
    def before_save(self):
        employee_name=self.employee_name
        latest_salary_assignment = frappe.db.get_list(
			"Salary Structure Assignment",
			filters={"employee_name": employee_name},  # Replace with actual employee ID
			fields=["base"],
			order_by="creation DESC",
			limit_page_length=1  # Fetch only the latest record
		)
        latest_salary = latest_salary_assignment[0]["base"]
        # frappe.msgprint(f"Latest Base Salary: {latest_salary}")
        self.base_salary=latest_salary
        
        normal_ot=float(self.normal_ot)
        temp_normal_overtime=(float(self.base_salary)/30/8)
        temp_normal_overtime1=temp_normal_overtime*1.2
        temp_normal_overtime2=temp_normal_overtime1* normal_ot
        self.normal_overtime_amount=temp_normal_overtime2
        
        holiday_ot=float(self.holiday_ot)
        temp_normal_overtime3=temp_normal_overtime*1.5
        temp_normal_overtime4=temp_normal_overtime3 * holiday_ot
        self.holiday_overtime_amount=temp_normal_overtime4
    
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
    
    
    # def before_submit(self):
    #     # print("HIIIIIIIIIIIIIIIIIIIIIi")
    #     additional_salary_normal_overtime= frappe.get_doc({"doctype":"Additional Salary",
	# 	"employee":self.employee,
	# 	"salary_component":"Normal overtime",
	# 	"amount":self.normal_overtime_amount,"payroll_date": self.posting_date
	# 	})
    #     additional_salary_normal_overtime.save()
    #     additional_salary_normal_overtime.submit()
    #     # print("BYYYYYYYYYYYYYYYYYYYYY")
        
    #     additional_salary_holiday_overtime= frappe.get_doc({
	# 	"doctype":"Additional Salary",
	# 	"employee":self.employee,
	# 	"salary_component":"Holiday overtime",
	# 	"amount":self.holiday_overtime_amount,
	# 	"payroll_date": self.posting_date

	# 	})
    #     additional_salary_holiday_overtime.save()
    #     additional_salary_holiday_overtime.submit()
    #     # print("HIIIIIIIIIIIIIIIIIIIIIi")
		
		
		
        
    
