![Pygame](https://www.pygame.org/docs/_images/pygame_logo.png)

# TRULY CENTERED BUTTON CLASS
**Sick and tired of Pygame's uncentered text on your buttons? Look no further!**

## Required parameters
- **screen**: `pygame.Surface`
- **text**: `str`
- **COLOR**: `tuple` `(r, g, b)`
- **center**: `tuple` `(x, y)`
- **dim**: `tuple` `(w, h)`

## Optional parameters
- **thickness**: `int` `(default = 1)`
- **radius**: `int` `(default = -1)`
- **font_size**: `int` `(default = w*0.9)`

## Additional Attributes
- **real_rect**: Actual surrounding border seen on screen
- **font_rect**: Invisible border that wraps the text
- **screen_color**: Screen color behind the button

## Methods
- **is_hovered()**: Checks if button is hovered (does not update visual state)
- **check_clicked()**: Updates visual state of button based on user mouse event
