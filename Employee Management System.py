class Person:
    def __init__(self, name, money, mood, healthRate):
        self.name = name 
        self.money = money
        self.mood = mood
        self.healthRate = healthRate 
    
    def sleep(self, hours):
        if hours == 7:
            self.mood = 'Happy'
        elif hours > 7:
            self.mood = 'Lazy'
        else:
            self.mood = 'Tired'

    def eat(self, meals):
        if meals >= 3:
            self.healthRate = '100%'
        elif meals == 2:
            self.healthRate = '75%' 
        elif meals == 1:
            self.healthRate = '50%'

    def buy(self, items):
        if self.money >= items * 10:
            self.money -= items * 10


class Car:  
    def __init__(self, car_name, fuelRate=100, velocity=0):
        self.car_name = car_name
        self.fuelRate = fuelRate
        self.velocity = velocity

    @property
    def velocity(self):
        return self._velocity
    
    @velocity.setter 
    def velocity(self, value):
        if 0 <= value <= 200:
            self._velocity = value
        else:
            raise ValueError('Velocity must be between 0 and 200')
        
    @property
    def fuelRate(self):
        return self._fuelRate
    
    @fuelRate.setter
    def fuelRate(self, value):
        if 0 <= value <= 100:
            self._fuelRate = value
        else:
            raise ValueError('Fuel rate must be between 0 and 100')
        
    def run(self, velocity, distance):
        self.velocity = velocity
        
        if self.fuelRate >= distance:
            self.fuelRate -= distance
            self.stop(0)
        else:
            remaining_distance = distance - self.fuelRate
            self.fuelRate = 0
            self.stop(remaining_distance)
         
    def stop(self, remaining_distance):
        self.velocity = 0


class Employee(Person):   
    def __init__(self, name, money, mood, healthrate, eid, car, email, salary, distance_to_work=20):
        super().__init__(name, money, mood, healthrate)
        self.eid = eid
        self.car = car
        self.email = email
        self.salary = salary
        self.distance_to_work = distance_to_work

    def work(self, hours):
        if hours == 8:
            self.mood = 'Happy'
        elif hours > 8:
            self.mood = 'Tired'
        else:
            self.mood = 'Lazy'
    
    def drive(self, distance_to_work):
        self.car.run(self.car.velocity, distance_to_work)
    
    def refuel(self, gasAmount=100):
        self.car.fuelRate = min(100, self.car.fuelRate + gasAmount)

    def send_email(self, to, subject, body):
        print(f"From: {self.email}")
        print(f"To: {to}")
        print(f"Subject: {subject}")
        print(f"Message: {body}")


class Office:
    employeesNum = 0

    def __init__(self, name):
        self.name = name
        self.employees = []

    @classmethod
    def change_emps_num(cls, num):
        cls.employeesNum = num

    @staticmethod
    def calculate_lateness(targetHour, moveHour, distance, velocity):
        if velocity <= 0:
            return True
        return moveHour + (distance / velocity) > targetHour

    def get_all_employees(self):
        return self.employees

    def get_employee(self, empId):
        for emp in self.employees:
            if emp.eid == empId:
                return emp
        return None

    def hire(self, employee):
        self.employees.append(employee)
        Office.employeesNum += 1

    def fire(self, empId):
        emp = self.get_employee(empId)
        if emp:
            self.employees.remove(emp)
            Office.employeesNum -= 1

    def deduct(self, empId, amount):
        emp = self.get_employee(empId)
        if emp:
            emp.salary -= amount

    def reward(self, empId, amount):
        emp = self.get_employee(empId)
        if emp:
            emp.salary += amount

    def check_lateness(self, eid, movehour):
        emp = self.get_employee(eid)
        if emp:
            if emp.car.fuelRate >= emp.distance_to_work:
                emp.car.fuelRate -= emp.distance_to_work
                late = Office.calculate_lateness(9, movehour, emp.distance_to_work, emp.car.velocity)
            else:
                emp.car.fuelRate = 0
                late = True
            
            if late:
                self.deduct(eid, 10)
            else:
                self.reward(eid, 10)


# ============= TEST WITH SAMY =============
if __name__ == "__main__":
    # Create Fiat 128
    fiat = Car("Fiat 128", fuelRate=100, velocity=60)
    print(f"\nCar: {fiat.car_name}")
    print(f"Fuel: {fiat.fuelRate}%, Speed: {fiat.velocity} km/h")

    # Create Samy
    samy = Employee("Samy", 500, "Normal", "100%", 101, fiat, "samy@iti.gov.eg", 5000, 20)
    print(f"\nEmployee: {samy.name}")
    print(f"Salary: {samy.salary} L.E")
    print(f"Distance to work: {samy.distance_to_work} km")

    # Create ITI Office
    iti = Office("ITI Smart Village")
    iti.hire(samy)
    print(f"\nOffice: {iti.name}")
    print(f"Total employees: {Office.employeesNum}")

    # Test 1: On time
    print("\n" + "-" * 50)
    print("Test 1: Leave at 8:00 AM")
    print("-" * 50)
    print(f"Before → Salary: {samy.salary} L.E, Fuel: {samy.car.fuelRate}%")
    iti.check_lateness(101, 8)
    print(f"After  → Salary: {samy.salary} L.E, Fuel: {samy.car.fuelRate}%")
    print("Result: ON TIME ✓")

    # Test 2: Late
    print("\n" + "-" * 50)
    print("Test 2: Leave at 8:45 AM")
    print("-" * 50)
    samy.car.fuelRate = 100
    print(f"Before → Salary: {samy.salary} L.E, Fuel: {samy.car.fuelRate}%")
    iti.check_lateness(101, 8.75)
    print(f"After  → Salary: {samy.salary} L.E, Fuel: {samy.car.fuelRate}%")
    print("Result: LATE ✗")

    # Test 3: Low fuel
    print("\n" + "-" * 50)
    print("Test 3: Low fuel (15%)")
    print("-" * 50)
    samy.car.fuelRate = 15
    print(f"Before → Salary: {samy.salary} L.E, Fuel: {samy.car.fuelRate}%")
    iti.check_lateness(101, 8)
    print(f"After  → Salary: {samy.salary} L.E, Fuel: {samy.car.fuelRate}%")
    print("Result: LATE (No fuel)")
