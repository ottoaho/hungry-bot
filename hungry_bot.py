""" Made by Otto. Quality guaranteed. """
from selenium import webdriver
import lackey
import mouse
import os

CIRCLE_PARAMS = { "r": 280, "n": 100, "offset":(-25, 0) }
MOUSE_SPEED = 0.0001
lackey.Settings.MinSimilarity = 0.8
lackey.setAutoWaitTimeout(5)

def spin_mouse(locations):
    [mouse.move(loc[0], loc[1], duration=MOUSE_SPEED) for loc in locations]

def get_mouse_coordinates(center, **kwargs):

    def _circle_points(r, n=1000):
        import math; pi = math.pi
        return [(math.cos(2 * pi / n * x) * r, math.sin(2 * pi / n * x) * r) for x in range(0, n + 1)]

    center = center.offset(*CIRCLE_PARAMS.get("offset", (0,0)))
    return [ (center.x + x, center.y + y) for x, y in _circle_points(CIRCLE_PARAMS["r"], CIRCLE_PARAMS["n"]) ]

def try_attach_game():
    app = lackey.App("Space Is Hungry")
    if app.isValid():
        app.focus()
        return app
    else:
        return None

def open_and_attach_game():
        chrome = webdriver.Chrome()
        chrome.get("https://turhaarpa.itch.io/space-is-hungry")
        print("browser ready")
        chrome.find_element_by_css_selector("button.load_iframe_btn").click()
        game_menu_ready = False
        while not game_menu_ready:
            game_menu_ready = lackey.exists("images/menu.png", 1) 
        return try_attach_game()
    

def prepare_game():#trigger_event=None):

    if lackey.exists("images/restart.png", seconds=0):
        goto_tutorial_btn = lackey.find("images/restart.png")
    else:
        start_menu = lackey.find("images/menu.png")
        goto_tutorial_btn = start_menu.offset(20, -40)

    goto_tutorial_btn.click()

def set_game_over(trigger_event):
    raise NotImplementedError

def poll_for_game_over(region):
    # start looking for game over state in subprocess
    lackey.setObserveScanRate(0.5)
    region.onAppear("images/restart.png", raise_error)
    region.observeInBackground()

def start_game():
    start_game_btn = lackey.find("images/start_game.png")
    start_game_btn.click()

if __name__ == "__main__":

    game = try_attach_game()

    if not game:
        game = open_and_attach_game()

    prepare_game()
    game_area = lackey.find("images/game_area.png")

    coords = get_mouse_coordinates(game_area.getCenter())

    poll_for_game_over(game_area)
    start_game()

    while True:
        spin_mouse(coords)