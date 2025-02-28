# Defining a class

class Dog:
    species = "Canis familiaris"  # Class variable
    
    def __init__(self, name, age):
        self.name = name   # Instance attributes
        self.age = age
        
    # Instance Methon    
    def description(self):
        return f"{self.name} is {self.age} years old."
    
    def speak(self, sound):
        return f"{self.name} says {sound}"
    
# Inheritance
class JackRussellTerrier(Dog):
    def speak(self, sound="Arf"):
        return f"{self.name} says {sound}"


    
    
miles = JackRussellTerrier("Miles", 4)
print(miles.speak())


class Parent:
    speaks = ["English"]
    
class Child(Parent):    
    def __init__(self):
        super().__init__()
        self.speaks.append("Kiswahili")
