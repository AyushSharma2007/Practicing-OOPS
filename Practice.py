class Employee:

    def __init__(self, f_name, l_name, salary):
        self.f_name = f_name
        self.l_name = l_name
        self.email = f_name + l_name + "@gmail.com"
        self.salary = salary

    @classmethod
    def understand(cls, emp_str):
        f_name, l_name, salary = emp_str.split("-")
        return cls(f_name, l_name, int(salary))
    
    # @classmethod
    def update_salary(self,upd_sal):
        self.salary=upd_sal
        return self.salary
# class Manager(Employee):
    
    # def add_Emp

emp_1=Employee("Ayush","Sharma",50000)
emp_2 = Employee.understand("Aditya-raj-40000")
emp_1.update_salary(80000)
print(emp_1.__dict__)
# print(emp_1.f_name)
# print(emp_1.l_name)
# print(emp_1.email)
# print(emp_1.salary)
# print(emp_2.f_name)
# print(emp_2.l_name)
# print(emp_2.email)
# print(emp_2.salary)
