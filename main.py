
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Line
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
import random

SIZE = 20

class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_width = 360
        self.game_height = 500
        
        # Game variables
        self.snake = [(160,200), (160,180), (160,160)]
        self.direction = (20, 0)
        self.score = 0
        self.high_score = 0
        self.delay = 0.18
        self.game_over = False
        self.touch_pos = None
        self.swipe_threshold = 40
        
        # UI setup
        self.create_ui()
        self.food = self.random_food()
        
        # Game loop
        Clock.schedule_interval(self.update, self.delay)

    def create_ui(self):
        # Score label
        self.score_label = Label(
            text='Score: 0  High: 0',
            pos=(10, 510),
            size_hint=(None, None),
            size=(340, 40),
            font_size=20
        )
        self.add_widget(self.score_label)
        
        # Instructions
        self.instr_label = Label(
            text='SWIPE to move! TAP RESTART',
            pos=(10, 475),
            size_hint=(None, None),
            size=(340, 25),
            font_size=14,
            color=(1,1,1,0.8)
        )
        self.add_widget(self.instr_label)
        
        # Restart button
        self.restart_btn = Button(
            text='RESTART',
            size_hint=(None, None),
            size=(100, 40),
            pos=(10, 10),
            background_color=(0.2, 0.8, 0.2, 1)
        )
        self.restart_btn.bind(on_press=self.restart)
        self.add_widget(self.restart_btn)

    def random_food(self):
        while True:
            food = (
                random.randint(0, 17) * 20,
                random.randint(1, 23) * 20
            )
            if food not in self.snake:
                return food

    def on_touch_down(self, touch):
        self.touch_pos = (touch.x, touch.y)
        return True

    def on_touch_move(self, touch):
        if self.touch_pos and not self.game_over:
            dx = touch.x - self.touch_pos[0]
            dy = touch.y - self.touch_pos[1]
            
            # Horizontal swipe
            if abs(dx) > abs(dy) and abs(dx) > self.swipe_threshold:
                if dx > 0 and self.direction != (-20, 0):
                    self.direction = (20, 0)
                elif dx < 0 and self.direction != (20, 0):
                    self.direction = (-20, 0)
            # Vertical swipe
            elif abs(dy) > self.swipe_threshold:
                if dy > 0 and self.direction != (0, -20):
                    self.direction = (0, 20)
                elif dy < 0 and self.direction != (0, 20):
                    self.direction = (0, -20)
                    
        self.touch_pos = (touch.x, touch.y)
        return True

    def update(self, dt):
        if self.game_over:
            return

        head = self.snake[-1]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        # Wall collision
        if (new_head[0] < 0 or new_head[1] < 0 or 
            new_head[0] >= self.game_width or new_head[1] >= 440):
            self.game_over = True
            self.show_game_over()
            return

        # Self collision
        if new_head in self.snake:
            self.game_over = True
            self.show_game_over()
            return

        self.snake.append(new_head)

        # Food collision
        if new_head == self.food:
            self.score += 10
            if self.score > self.high_score:
                self.high_score = self.score
            self.food = self.random_food()
            if self.delay > 0.10:
                self.delay -= 0.002
        else:
            self.snake.pop(0)

        self.draw()
        self.update_ui()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            # Border
            Color(0.3, 0.3, 0.3, 1)
            Line(rectangle=(0, 0, 360, 440), width=4)
            
            # Snake body (gradient)
            for i, seg in enumerate(self.snake):
                alpha = 1.0 - (i * 0.02)
                Color(0, 1 - (i * 0.03), 0, alpha)
                Rectangle(pos=seg, size=(SIZE, SIZE))
            
            # Snake head
            Color(0, 1, 0.5, 1)
            Rectangle(pos=self.snake[-1], size=(SIZE, SIZE))
            
            # Food
            Color(1, 0.2, 0.2, 1)
            Rectangle(pos=self.food, size=(24, 24))

    def update_ui(self):
        self.score_label.text = f'Score: {self.score}  High: {self.high_score}'

    def show_game_over(self):
        self.instr_label.text = f'GAME OVER! Score: {self.score}  TAP RESTART!'

    def restart(self, instance):
        self.snake = [(160,200), (160,180), (160,160)]
        self.direction = (20, 0)
        self.score = 0
        self.delay = 0.18
        self.game_over = False
        self.food = self.random_food()
        self.instr_label.text = 'SWIPE to move! TAP RESTART'
        self.draw()
        self.update_ui()

class SnakeApp(App):
    def build(self):
        return SnakeGame()

if __name__ == '__main__':
    SnakeApp().run()
EOF