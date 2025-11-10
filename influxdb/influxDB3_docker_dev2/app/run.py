from influx_setup import influx_setup
import writer

if __name__ == "__main__":
    influx_setup()
    writer.run()
