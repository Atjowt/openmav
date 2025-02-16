from openmav import OpenMav, FlightEnvironment


def main():
    openmav = OpenMav()
    environment = FlightEnvironment.simple(
        latitude=59.354,
        longitude=17.939,
        altitude=15000.0,
        heading=90.0,
        speed=400.0
    )
    openmav.load(environment)
    openmav.launch()


if __name__ == "__main__":
    main()

