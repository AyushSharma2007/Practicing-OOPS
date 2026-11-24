class Engine:
    """Represents a car engine with horsepower and an on/off state.

    Attributes:
        horsepower: The engine's power rating.
        is_engine_running: Whether the engine is currently turned on.
    """

    def __init__(self, horsepower: int) -> None:
        """Initializes the engine in the off state.

        Args:
            horsepower: The horsepower rating of the engine.
        """
        
        self.horsepower = horsepower
        self.is_engine_running = False

    def start(self) -> None:
        """Starts the engine if it is currently off."""
        
        if not self.is_engine_running:
            self.is_engine_running = True
            print("Engine started!")
        else:
            print("Engine is already running!")

    def stop(self) -> None:
        """Stops the engine if it is currently running."""
        
        if self.is_engine_running:
            self.is_engine_running = False
            print("Engine stopped!")
        else:
            print("Engine is already off!")


class Driver:
    """Represents an independent driver who can operate a car.

    Attributes:
        name: The driver's name.
    """

    def __init__(self, name: str) -> None:
        """Initializes a driver with a name.

        Args:
            name: The name of the driver.
        """
        
        self.name = name


class Car:
    """Represents a car composed of an Engine and optionally operated by a Driver.

    Attributes:
        color: The exterior color of the car.
        fuel: Current fuel level, capped at 100.
        engine: The Engine instance owned by this car (Composition).
        driver: The currently seated Driver instance, or None (Aggregation).
    """

    def __init__(self, color: str, horsepower: int) -> None:
        """Initializes a car with a full tank, an owned engine, and no driver.

        Args:
            color: The color of the car.
            horsepower: The horsepower used to create the car's engine.
        """
        
        self.color = color
        self.fuel = 100
        self.engine = Engine(horsepower)  # Composition
        self.driver: Driver | None = None  # Aggregation

    def drive(self) -> None:
        """Drives the car and consumes 10 fuel if a driver, running engine, and enough fuel are present."""
        
        if self.driver is None:
            print("No driver in car, cant drive!")
            return
        if not self.engine.is_engine_running:
            print("Engine is off, cant drive!")
            return
        if self.fuel < 10:
            print("Fuel low, Refuel to drive!")
            return

        self.fuel -= 10
        print(f"{self.driver.name} drove, fuel left : {self.fuel}")

    def refuel(self, amount: int) -> None:
        """Adds fuel to the tank up to a maximum capacity of 100.

        Args:
            amount: Positive amount of fuel to add. Non-positive values are ignored.
        """
        
        if amount > 0:
            self.fuel = min(100, self.fuel + amount)

    def set_driver(self, driver: Driver) -> None:
        """Seats a driver and starts the engine if the car is currently empty.

        Args:
            driver: The Driver instance to seat in the car.
        """
        
        if self.driver is None:
            self.driver = driver
            print(f"{driver.name} seated!")
            self.engine.start()
        else:
            print("Driver is already seated!")

    def remove_driver(self) -> None:
        """Removes the seated driver and stops the engine if a driver is present."""
        
        if self.driver is not None:
            self.driver = None
            print("Driver removed!")
            self.engine.stop()
        else:
            print("No driver to remove!")

alex = Driver("Alex")
car1 = Car("red", 200)
car2 = Car("black", 350)

car1.drive()
car1.set_driver(alex)
car1.drive()
car1.remove_driver()
car1.drive()

del car1  # Scraps car1 and its Engine (Composition)

car2.set_driver(alex)  # Alex survived and hops into car2 (Aggregation)
car2.drive()
