from pathlib import Path

import click
import pyautogui
from pynput.keyboard import Listener as KeyboardListener

OUTPUTS_DIR = Path("outputs")


def get_region_coords():
    class Coordinates:
        def __init__(self):
            self.x = []
            self.y = []

        def on_press(self, key):
            if hasattr(key, "char") and key.char == "s":
                point = pyautogui.position()
                self.x.append(point.x)
                self.y.append(point.y)

            if len(self.x) == 2:
                return False

        def get_region(self):
            if (len(self.x) != 2) or (len(self.y) != 2):
                raise ValueError("You need to click 2 times to get the region")

            x_min = int(min(self.x))
            width = int(max(self.x) - x_min)
            y_min = int(min(self.y))
            height = int(max(self.y) - y_min)
            return x_min, y_min, width, height

    coordinates = Coordinates()

    with KeyboardListener(on_press=coordinates.on_press) as listener:
        print('Press "s" twice to set the region')
        listener.join()

    return coordinates.get_region()


class ScreenshotTaker:
    def __init__(self, button_location, region):
        self.region = region
        self.button_location = button_location
        self._idx = 0

    def take_screenshot(self, key):
        if hasattr(key, "char") and key.char == "n":
            self.region = get_region_coords()
            print("Region set to ", self.region)
            print('Press "n" to set a new region (otherwise the previous one will be used)')
            print('Press "c" to take a screenshot and go to the next page')
        if hasattr(key, "char") and key.char == "c":
            img = pyautogui.screenshot(region=self.region)
            img.save(OUTPUTS_DIR / f"output_{self._idx}.png")
            pyautogui.click(*self.button_location)
            self._idx += 1


def get_button_coords():
    class Coordinates:
        def __init__(self):
            self.x = None
            self.y = None

        def on_press(self, key):
            if hasattr(key, "char") and key.char == "b":
                point = pyautogui.position()
                self.x = point.x
                self.y = point.y
                return False

    coordinates = Coordinates()
    with KeyboardListener(on_press=coordinates.on_press) as listener:
        print('Press "b" to set the button location')
        listener.join()

    return coordinates.x, coordinates.y


@click.command()
def take_all_screenshots():
    OUTPUTS_DIR.mkdir(exist_ok=True)

    button_coords = get_button_coords()
    region = get_region_coords()

    screenshot_taker = ScreenshotTaker(button_coords, region)
    with KeyboardListener(on_press=screenshot_taker.take_screenshot) as listener:
        print('Press "n" to set a new region (otherwise the previous one will be used)')
        print('Press "c" to take a screenshot and go to the next page')
        listener.join()


@click.group()
def cli():
    pass


cli.add_command(take_all_screenshots)


if __name__ == "__main__":
    cli()
