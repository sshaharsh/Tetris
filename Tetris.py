import tkinter as tk
import random

GAME_TITLE = "Tkinter Tetris"
GRID_ROWS = 20
GRID_COLS = 10
BLOCK_SIZE = 30
CANVAS_WIDTH = GRID_COLS * BLOCK_SIZE
CANVAS_HEIGHT = GRID_ROWS * BLOCK_SIZE
INITIAL_GAME_SPEED = 500

BACKGROUND_COLOR = "#000000"
SCORE_COLOR = "#ffffff"
INFO_BG_COLOR = "#222222"

SHAPES = {
    'I': {'color': '#00ffff', 'rotations': [
        [(-2, 0), (-1, 0), (0, 0), (1, 0)],
        [(0, -2), (0, -1), (0, 0), (0, 1)]
    ]},
    'J': {'color': '#0000ff', 'rotations': [
        [(-1, -1), (0, -1), (0, 0), (1, 0)],
        [(-1, 1), (-1, 0), (0, 0), (0, -1)],
        [(1, 1), (0, 1), (0, 0), (-1, 0)],
        [(1, -1), (1, 0), (0, 0), (0, 1)]
    ]},
    'L': {'color': '#ffaa00', 'rotations': [
        [(-1, 1), (0, 1), (0, 0), (1, 0)],
        [(-1, -1), (0, -1), (0, 0), (0, 1)],
        [(1, -1), (0, -1), (0, 0), (-1, 0)],
        [(1, 1), (1, 0), (0, 0), (0, -1)]
    ]},
    'O': {'color': '#ffff00', 'rotations': [
        [(0, 0), (0, 1), (1, 0), (1, 1)]
    ]},
    'S': {'color': '#00ff00', 'rotations': [
        [(0, -1), (0, 0), (1, 0), (1, 1)],
        [(-1, 0), (0, 0), (0, -1), (1, -1)]
    ]},
    'T': {'color': '#800080', 'rotations': [
        [(0, -1), (0, 0), (0, 1), (1, 0)],
        [(-1, 0), (0, 0), (1, 0), (0, 1)],
        [(0, 1), (0, 0), (0, -1), (-1, 0)],
        [(1, 0), (0, 0), (-1, 0), (0, -1)]
    ]},
    'Z': {'color': '#ff0000', 'rotations': [
        [(0, 1), (0, 0), (1, 0), (1, -1)],
        [(-1, -1), (0, -1), (0, 0), (1, 0)]
    ]}
}

class TetrisGame:
    def __init__(self, root):
        self.root = root
        self.root.title(GAME_TITLE)
        self.root.resizable(False, False)

        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.game_speed = INITIAL_GAME_SPEED
        
        self.grid = [[BACKGROUND_COLOR for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        
        self.current_piece = None
        self.next_piece = self._get_random_piece()
        self.current_pos = None
        self.rotation_state = 0

        self._setup_ui()
        self._bind_keys()
        self.new_piece()
        self.game_loop()

    def _setup_ui(self):
        self.frame = tk.Frame(self.root, bg=INFO_BG_COLOR)
        self.frame.pack(padx=10, pady=10)

        self.canvas = tk.Canvas(self.frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT)

        self.info_panel = tk.Frame(self.frame, width=150, height=CANVAS_HEIGHT, bg=INFO_BG_COLOR)
        self.info_panel.pack(side=tk.RIGHT, padx=10)

        self.score_label = tk.Label(self.info_panel, text="Score: 0", font=("Helvetica", 16, "bold"), fg=SCORE_COLOR, bg=INFO_BG_COLOR)
        self.score_label.pack(pady=10)
        self.level_label = tk.Label(self.info_panel, text="Level: 1", font=("Helvetica", 16, "bold"), fg=SCORE_COLOR, bg=INFO_BG_COLOR)
        self.level_label.pack(pady=5)

        tk.Label(self.info_panel, text="Next:", font=("Helvetica", 14), fg=SCORE_COLOR, bg=INFO_BG_COLOR).pack(pady=10)
        self.next_canvas = tk.Canvas(self.info_panel, width=4 * BLOCK_SIZE, height=4 * BLOCK_SIZE, bg=BACKGROUND_COLOR, highlightthickness=1, highlightbackground=SCORE_COLOR)
        self.next_canvas.pack(pady=5)
        
        self.message_label = tk.Label(self.root, text="", font=("Helvetica", 20, "bold"), fg="#ff3333", bg=INFO_BG_COLOR)
        self.message_label.pack(fill='x', pady=5)

    def _bind_keys(self):
        self.root.bind('<Left>', lambda e: self.move_piece(0, -1))
        self.root.bind('<Right>', lambda e: self.move_piece(0, 1))
        self.root.bind('<Down>', lambda e: self.move_piece(1, 0, fast=True))
        self.root.bind('<space>', lambda e: self.hard_drop())
        self.root.bind('<Up>', lambda e: self.rotate_piece(1))

    def _get_random_piece(self):
        return random.choice(list(SHAPES.keys()))

    def new_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = self._get_random_piece()
        self.rotation_state = 0
        self.current_pos = [2, GRID_COLS // 2 - 1]
        
        if self._check_collision(0, 0, self.rotation_state):
            self.end_game()

        self.draw_next_piece()

    def get_piece_blocks(self, dx=0, dy=0, rotation=None):
        if rotation is None:
            rotation = self.rotation_state
        
        blocks = SHAPES[self.current_piece]['rotations'][rotation]
        
        new_blocks = []
        for r_offset, c_offset in blocks:
            row = self.current_pos[0] + r_offset + dx
            col = self.current_pos[1] + c_offset + dy
            new_blocks.append((row, col))
        return new_blocks

    def _check_collision(self, dx, dy, rotation):
        blocks = self.get_piece_blocks(dx, dy, rotation)
        for row, col in blocks:
            if not (0 <= col < GRID_COLS and 0 <= row < GRID_ROWS):
                return True
            if self.grid[row][col] != BACKGROUND_COLOR:
                return True
        return False

    def move_piece(self, dx, dy, fast=False):
        if self.game_over:
            return
            
        if not self._check_collision(dx, dy, self.rotation_state):
            self.current_pos[0] += dx
            self.current_pos[1] += dy
        elif dx == 1:
            self.lock_piece()
            
        if fast:
            self.game_loop()

    def rotate_piece(self, direction):
        if self.game_over:
            return
            
        new_rotation = (self.rotation_state + direction) % len(SHAPES[self.current_piece]['rotations'])
        
        if not self._check_collision(0, 0, new_rotation):
            self.rotation_state = new_rotation

    def hard_drop(self):
        if self.game_over:
            return
            
        while not self._check_collision(1, 0, self.rotation_state):
            self.current_pos[0] += 1
        
        self.current_pos[0] -= 1
        self.lock_piece()
        self.game_loop()

    def lock_piece(self):
        blocks = self.get_piece_blocks()
        color = SHAPES[self.current_piece]['color']
        
        for row, col in blocks:
            self.grid[row][col] = color
            
        self.clear_lines()
        self.new_piece()

    def clear_lines(self):
        new_grid = []
        lines_cleared_this_move = 0
        
        for row in self.grid:
            if BACKGROUND_COLOR in row:
                new_grid.append(row)
            else:
                lines_cleared_this_move += 1

        for _ in range(lines_cleared_this_move):
            new_grid.insert(0, [BACKGROUND_COLOR] * GRID_COLS)

        self.grid = new_grid
        
        if lines_cleared_this_move > 0:
            score_multiplier = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += score_multiplier.get(lines_cleared_this_move, 0) * self.level
            self.lines_cleared += lines_cleared_this_move
            self.level = (self.lines_cleared // 10) + 1
            self.game_speed = max(50, INITIAL_GAME_SPEED - (self.level - 1) * 40)
            self.score_label.config(text=f"Score: {self.score}")
            self.level_label.config(text=f"Level: {self.level}")

    def draw_elements(self):
        self.canvas.delete(tk.ALL)
        
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                color = self.grid[r][c]
                if color != BACKGROUND_COLOR:
                    self._draw_block(r, c, color)
        
        if self.current_piece:
            blocks = self.get_piece_blocks()
            color = SHAPES[self.current_piece]['color']
            for r, c in blocks:
                if 0 <= r < GRID_ROWS and 0 <= c < GRID_COLS:
                    self._draw_block(r, c, color)

    def _draw_block(self, row, col, color, canvas=None):
        if canvas is None:
            canvas = self.canvas
            
        x1 = col * BLOCK_SIZE
        y1 = row * BLOCK_SIZE
        x2 = x1 + BLOCK_SIZE
        y2 = y1 + BLOCK_SIZE
        
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=BACKGROUND_COLOR, width=2)
        canvas.create_rectangle(x1 + 3, y1 + 3, x2 - 3, y2 - 3, fill=color, outline=SCORE_COLOR, width=1)


    def draw_next_piece(self):
        self.next_canvas.delete(tk.ALL)
        
        blocks = SHAPES[self.next_piece]['rotations'][0]
        color = SHAPES[self.next_piece]['color']
        
        # Center the preview block
        center_row = 1.5
        center_col = 1.5

        # Find min offsets to normalize piece position in the 4x4 box
        min_r = min(b[0] for b in blocks)
        min_c = min(b[1] for b in blocks)

        # Draw the piece in the preview box
        for r_offset, c_offset in blocks:
            # Shift the piece to the top-left corner and then add padding
            row = r_offset - min_r
            col = c_offset - min_c
            
            # Additional centering for 2-wide pieces (like O) vs 4-wide (like I)
            if self.next_piece in ('O', 'S', 'Z'):
                col += 0.5
            elif self.next_piece in ('I'):
                if len(blocks) == 2: # I horizontal
                    row += 0.5
                else: # I vertical
                    col += 0.5

            x1 = int(col * BLOCK_SIZE)
            y1 = int(row * BLOCK_SIZE)
            x2 = x1 + BLOCK_SIZE
            y2 = y1 + BLOCK_SIZE
            
            self.next_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=BACKGROUND_COLOR, width=2)


    def game_loop(self):
        if self.game_over:
            return

        self.move_piece(1, 0)
        self.draw_elements()
            
        self.root.after(self.game_speed, self.game_loop)

    def end_game(self):
        self.game_over = True
        self.message_label.config(text="GAME OVER", fg="#ff3333")
        
if __name__ == "__main__":
    root = tk.Tk()
    game = TetrisGame(root)
    root.mainloop()
