from Point import Point
from Car import Car, Driver, Engine  # Update 'Car' to your module filename


def run_tests() -> None:
    print("=== 1. INPUT VALIDATION & EXCEPTIONS ===")
    try:
        Engine(0)
    except ValueError as e:
        print(f"Caught expected Engine error: {e}")

    try:
        Car("Red", 100, fuel=120.0)
    except ValueError as e:
        print(f"Caught expected fuel error: {e}")

    try:
        Car("Red", 100, start_pos="(0, 0)")  # type: ignore
    except TypeError as e:
        print(f"Caught expected start_pos TypeError: {e}")

    print("\n=== 2. COMPOSITION & AGGREGATION ISOLATION ===")
    start = Point(1, 1)
    car1 = Car("Matte Black", horsepower=100, start_pos=start)
    start.move(99, 99)  # Mutating external Point must NOT move car1
    assert car1.position.x == 1 and car1.position.y == 1, "Composition aliasing bug!"
    print(f"Car1 position unaffected by external Point move: {car1.position}")

    driver = Driver("Ayush")
    car1.set_driver(driver)
    car1.remove_driver()
    assert driver.name == "Ayush", "Driver should survive removal from car!"
    print(f"Driver '{driver.name}' still exists independently after removal.")

    print("\n=== 3. GUARD CLAUSES IN DRIVE() ===")
    dest = Point(4, 5)
    car1.drive(dest)  # No driver

    car1.set_driver(driver)
    car1.engine.stop()
    car1.drive(dest)  # Engine off

    car1.engine.start()
    car1.drive(Point(1, 1))  # Zero distance

    try:
        car1.drive("not_a_point")  # type: ignore
    except TypeError as e:
        print(f"Caught expected stop_pos TypeError: {e}")

    print("\n=== 4. FULL TRIP MATH (3-4-5 TRIANGLE) ===")
    # Start: Point(1, 1) -> Dest: Point(4, 5) => dx=3, dy=4 => distance = 5.0
    # hp=100 => mileage = 200 / 100 = 2.0 => fuel_needed = 5.0 / 2.0 = 2.5
    car1.drive(dest)
    dest.move(50, 50)  # Mutating destination afterward must NOT move car1
    assert car1.position.x == 4 and car1.position.y == 5
    assert round(car1.fuel, 2) == 97.50
    car1.total_distance()  # Expected: 5.00

    print("\n=== 5. MID-TRIP FUEL EXHAUSTION (SIMILAR TRIANGLES) ===")
    # Start: Point(0, 0) -> Dest: Point(6, 8) => distance = 10.0
    # hp=200 => mileage = 200 / 200 = 1.0; fuel = 5.0 => max_distance = 5.0 (ratio = 0.5)
    # Expected stop: Point(3.0, 4.0), fuel = 0.00
    racer = Car("Midnight Blue", horsepower=200, fuel=5.0)
    racer.set_driver(Driver("Rohan"))
    racer.drive(Point(6, 8))
    assert racer.position.x == 3.0 and racer.position.y == 4.0
    assert racer.fuel == 0.0
    racer.total_distance()  # Expected: 5.00

    print("\n=== 6. EMPTY TANK GUARD & REFUEL CAP ===")
    racer.drive(Point(10, 10))  # Must print "No fuel to move at all!"
    racer.refuel(-25)  # Negative refuel ignored
    assert racer.fuel == 0.0
    racer.refuel(150)  # Must cap at 100.0
    assert racer.fuel == 100.0
    print(f"Fuel after invalid (-25) and overflow (+150) refuels: {racer.fuel:.2f}")

    print("\nAll assertions passed!")


if __name__ == "__main__":
    run_tests()