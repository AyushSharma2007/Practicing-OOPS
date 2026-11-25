from Point import Point


class Engine:
    """Represents a car engine with horsepower, mileage, and an on/off state.

    Attributes:
        BASE_RATE: Class constant used to calculate mileage from horsepower.
        horsepower: The engine's power rating.
        is_engine_running: Whether the engine is currently turned on.
        mileage: Distance travelled per unit of fuel (BASE_RATE / horsepower).
    """

    BASE_RATE = 200

    def __init__(self, horsepower: int) -> None:
        """Initializes the engine in the off state and calculates its mileage.

        Args:
            horsepower: The horsepower rating of the engine (must be greater than 0).

        Raises:
            ValueError: If horsepower is less than or equal to 0.
        """

        if horsepower <= 0:
            raise ValueError("Horsepower must be greater than 0!")

        self.horsepower = horsepower
        self.is_engine_running = False
        self.mileage = self.BASE_RATE / horsepower

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
    """Represents a car composed of an Engine and Point position, optionally operated by a Driver.

    Attributes:
        name: The display name or model of the car.
        color: The exterior color of the car.
        odometer: Cumulative distance travelled by the car.
        engine: The Engine instance owned by this car (Composition).
        driver: The currently seated Driver instance, or None (Aggregation).
        fuel: Current fuel level, between 0 and 100.
        position: The current 2D Point coordinates of the car (Composition).
    """

    def __init__(
        self,
        name: str,
        color: str,
        horsepower: int,
        start_pos: Point | None = None,
        fuel: float = 100.0,
    ) -> None:
        """Initializes a car with a name, owned engine, starting position, fuel level, and no driver.

        Args:
            name: The display name or model of the car.
            color: The exterior color of the car.
            horsepower: The horsepower rating used to create the car's engine.
            start_pos: Optional starting Point coordinates. Defaults to Point(0, 0).
            fuel: Initial fuel level between 0 and 100. Defaults to 100.0.

        Raises:
            ValueError: If fuel is outside the valid 0 to 100 range.
            TypeError: If start_pos is provided and is not a Point instance.
        """

        self.name = name
        self.color = color
        self.odometer = 0.0
        self.engine = Engine(horsepower)  # Composition
        self.driver: Driver | None = None  # Aggregation
        if 0 <= fuel <= 100:
            self.fuel = fuel
        else:
            raise ValueError("Fuel should be btw 0 and 100!")
        if start_pos is None:
            self.position = Point()
        elif not isinstance(start_pos, Point):
            raise TypeError("Type of start position is wrong!")
        else:
            self.position = Point(start_pos.x, start_pos.y)

    def drive(self, stop_pos: Point) -> None:
        """Drives the car toward a destination, consuming fuel based on distance and mileage.

        If fuel is insufficient for the full trip, the car travels as far as remaining
        fuel allows along the straight-line path and stops when the tank hits zero.

        Args:
            stop_pos: The target Point coordinates to drive toward.

        Raises:
            TypeError: If stop_pos is not a Point instance.
        """

        if not isinstance(stop_pos, Point):
            raise TypeError("Type of stop position is wrong!")

        if self.fuel <= 0:
            print("No fuel to move at all!")
            return

        if self.driver is None:
            print("No driver in car, cant drive!")
            return

        if not self.engine.is_engine_running:
            print("Engine is off, cant drive!")
            return

        distance = self.position.calcDistance(stop_pos)

        if distance == 0:
            print("Distance is zero, no movement needed!")
            return

        fuel_needed = distance / self.engine.mileage

        if self.fuel < fuel_needed:
            max_distance = self.fuel * self.engine.mileage
            ratio = max_distance / distance

            fuel_used = self.fuel
            self.fuel = 0.0
            delta_x, delta_y = (
                stop_pos.x - self.position.x,
                stop_pos.y - self.position.y,       
            )
            new_x, new_y = self.position.x + (delta_x * ratio), self.position.y + (
                delta_y * ratio
            )

            self.position.move(new_x, new_y)
            print(
                f"\n{self.driver.name} drove {self.name} until fuel ran out! \nDistance Travelled : {max_distance:.2f} \nCurrent Position : {self.position} \nFuel used : {fuel_used:.2f} \nfuel left : {self.fuel:.2f}"
            )
            self.odometer += max_distance
            return

        self.fuel = max(0.0, self.fuel - fuel_needed)
        self.position.move(stop_pos.x, stop_pos.y)
        print(
            f"\n{self.driver.name} drove {self.name} \nDistance Travelled : {distance:.2f} \nCurrent Position : {self.position} \nFuel used : {fuel_needed:.2f} \nfuel left : {self.fuel:.2f}"
        )
        self.odometer += distance

    def refuel(self, amount: float) -> None:
        """Adds fuel to the tank up to a maximum capacity of 100.0.

        Args:
            amount: Positive amount of fuel to add. Non-positive values are ignored.
        """

        if amount > 0:
            self.fuel = min(100.0, self.fuel + amount)

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

    def total_distance(self) -> None:
        """Prints the car's name and cumulative distance travelled on its odometer."""

        print(f"{self.name} - Total distance travelled till now : {self.odometer:.2f}")