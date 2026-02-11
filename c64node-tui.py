#!/usr/bin/env python3
"""C64 Chain Node - Commodore 64 Style Terminal UI"""

import curses
import subprocess
import threading
import time
import re
import os
import sys
from collections import deque

class C64NodeTUI:
    # C64 color scheme: light blue on blue
    def __init__(self):
        self.height = 0
        self.difficulty = 0
        self.last_block_id = ""
        self.last_pow = ""
        self.last_reward = ""
        self.blocks_added = 0
        self.blocks_alt = 0
        self.start_time = time.time()
        self.log_lines = deque(maxlen=200)
        self.status = "INITIALIZING..."
        self.daemon_proc = None
        self.running = True
        self.rpc_calls = 0

    def parse_line(self, line):
        """Parse daemon output and update state"""
        self.log_lines.append(line.rstrip())

        # Block added
        m = re.search(r'HEIGHT (\d+), difficulty:\s+(\d+)', line)
        if m:
            self.height = int(m.group(1))
            self.difficulty = int(m.group(2))
            self.blocks_added += 1
            self.status = "MINING"

        # Block reward
        m = re.search(r'block reward: ([\d.]+)\(', line)
        if m:
            self.last_reward = m.group(1)

        # Block ID
        m = re.search(r'id:\s+<([a-f0-9]+)>', line)
        if m:
            self.last_block_id = m.group(1)[:32] + "..."

        # PoW hash
        m = re.search(r'PoW:\s+<([a-f0-9]+)>', line)
        if m:
            self.last_pow = m.group(1)[:32] + "..."

        # Alternative block
        if 'ALTERNATIVE' in line:
            self.blocks_alt += 1

        # RPC calls
        if 'Calling RPC method' in line:
            self.rpc_calls += 1

        # Sync status
        if 'Synchronized OK' in line or 'SYNCHRONIZED' in line:
            self.status = "SYNCHRONIZED"
        
        if 'Loading blockchain' in line:
            self.status = "LOADING BLOCKCHAIN..."

        if 'BLOCK SUCCESSFULLY ADDED' in line:
            self.status = "MINING"

    def start_daemon(self, args):
        """Start daemon subprocess"""
        self.daemon_proc = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True
        )

        def reader():
            for line in self.daemon_proc.stdout:
                if not self.running:
                    break
                self.parse_line(line)

        t = threading.Thread(target=reader, daemon=True)
        t.start()

    def draw_border(self, win, h, w):
        """Draw C64-style border"""
        # Top
        win.addstr(0, 0, "+" + "-" * (w - 2) + "+")
        # Sides
        for y in range(1, h - 1):
            try:
                win.addstr(y, 0, "|")
                win.addstr(y, w - 1, "|")
            except:
                pass
        # Bottom
        try:
            win.addstr(h - 1, 0, "+" + "-" * (w - 2) + "+")
        except:
            pass

    def draw_header(self, win, w, y):
        """Draw C64-style header"""
        title = "**** C64 CHAIN NODE V0.1 ****"
        win.addstr(y, (w - len(title)) // 2, title, curses.A_BOLD | curses.color_pair(2))
        y += 1
        sub = "64K RAM SYSTEM  38911 BASIC BYTES FREE"
        win.addstr(y, (w - len(sub)) // 2, sub, curses.color_pair(1))
        return y + 1

    def draw_stats(self, win, w, y):
        """Draw node statistics"""
        uptime = int(time.time() - self.start_time)
        h, m, s = uptime // 3600, (uptime % 3600) // 60, uptime % 60

        stats = [
            f"STATUS:      {self.status}",
            f"HEIGHT:      {self.height}",
            f"DIFFICULTY:  {self.difficulty}",
            f"BLOCKS OK:   {self.blocks_added}",
            f"BLOCKS ALT:  {self.blocks_alt}",
            f"REWARD:      {self.last_reward} C64",
            f"RPC CALLS:   {self.rpc_calls}",
            f"UPTIME:      {h:02d}:{m:02d}:{s:02d}",
        ]

        win.addstr(y, 3, "READY.", curses.A_BOLD | curses.color_pair(2))
        y += 1
        win.addstr(y, 3, "LIST", curses.color_pair(1))
        y += 2

        for i, stat in enumerate(stats):
            win.addstr(y, 3, f"{i}  \"{stat}\"", curses.color_pair(1))
            y += 1

        return y + 1

    def draw_block_info(self, win, w, y):
        """Draw latest block info"""
        win.addstr(y, 3, "LAST BLOCK:", curses.A_BOLD | curses.color_pair(2))
        y += 1
        if self.last_block_id:
            win.addstr(y, 3, f"  ID:  {self.last_block_id}", curses.color_pair(1))
            y += 1
            win.addstr(y, 3, f"  POW: {self.last_pow}", curses.color_pair(1))
            y += 1
        else:
            win.addstr(y, 3, "  WAITING FOR BLOCKS...", curses.color_pair(1))
            y += 1
        return y + 1

    def draw_log(self, win, w, y, max_y):
        """Draw scrolling log at bottom"""
        win.addstr(y, 3, "LOG:", curses.A_BOLD | curses.color_pair(2))
        y += 1

        available = max_y - y - 2
        if available < 1:
            return

        lines = list(self.log_lines)
        show = lines[-available:] if len(lines) > available else lines

        for line in show:
            if y >= max_y - 1:
                break
            # Truncate and clean
            clean = line.replace('\033[', '?[')  # strip ANSI
            clean = re.sub(r'\?\[[0-9;]*m', '', clean)  # remove color codes
            display = clean[:w - 6]
            
            # Color highlights
            pair = curses.color_pair(1)
            if 'SUCCESSFULLY' in line or '+++++' in line:
                pair = curses.color_pair(3)
            elif 'ERROR' in line or 'error' in line:
                pair = curses.color_pair(4)
            elif 'ALTERNATIVE' in line:
                pair = curses.color_pair(5)

            try:
                win.addstr(y, 3, display, pair)
            except:
                pass
            y += 1

    def draw_footer(self, win, h, w):
        """Draw footer"""
        footer = " CTRL+C TO QUIT  -  C64 CHAIN (C) 2026 "
        try:
            win.addstr(h - 2, (w - len(footer)) // 2, footer, curses.A_BOLD | curses.color_pair(2))
        except:
            pass

    def run(self, stdscr, daemon_args):
        """Main curses loop"""
        # Setup colors - C64 palette
        curses.start_color()
        curses.use_default_colors()
        
        # Init color pairs - C64 authentic palette
        # Real C64: light blue (#6C5EB5) on dark blue (#40318D)
        # Terminal approximation: bright white/cyan on blue
        if curses.can_change_color():
            # Custom C64 colors if terminal supports it
            curses.init_color(20, 260, 220, 560)   # C64 dark blue bg
            curses.init_color(21, 420, 370, 710)   # C64 light blue text
            curses.init_color(22, 1000, 1000, 1000) # White
            curses.init_color(23, 700, 1000, 700)   # Green - very bright
            curses.init_color(24, 1000, 400, 400)   # Red - brighter
            curses.init_color(25, 1000, 1000, 700)   # Yellow - very bright
            curses.init_pair(1, 22, 20)              # Normal: white on dark blue
            curses.init_pair(2, 21, 20)              # Headers: light blue on dark blue
            curses.init_pair(3, 23, 20)              # Success: green on dark blue
            curses.init_pair(4, 24, 20)              # Errors: red on dark blue
            curses.init_pair(5, 25, 20)              # Warnings: yellow on dark blue
            curses.init_pair(6, 21, 20)              # Border: light blue on dark blue
        else:
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
            curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLUE)
            curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLUE)
            curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLUE)
            curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLUE)
            curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLUE)

        stdscr.bkgd(' ', curses.color_pair(1))
        stdscr.nodelay(True)
        curses.curs_set(0)

        # Start daemon
        self.start_daemon(daemon_args)
        self.status = "LOADING BLOCKCHAIN..."

        # Poll RPC to get initial state once daemon is ready
        def poll_rpc():
            import urllib.request
            import json as js
            time.sleep(10)  # Wait for daemon to load
            for _ in range(300):  # Keep polling
                if not self.running:
                    break
                try:
                    req = urllib.request.Request(
                        "http://127.0.0.1:29641/json_rpc",
                        data=js.dumps({"jsonrpc":"2.0","id":"0","method":"get_info"}).encode(),
                        headers={"Content-Type": "application/json"}
                    )
                    resp = urllib.request.urlopen(req, timeout=2)
                    data = js.loads(resp.read())["result"]
                    self.height = data.get("height", self.height)
                    self.difficulty = data.get("difficulty", self.difficulty)
                    if self.height > 0:
                        self.status = "MINING" if data.get("busy_syncing") == False else "SYNCING"
                except:
                    pass
                time.sleep(2)

        rpc_thread = threading.Thread(target=poll_rpc, daemon=True)
        rpc_thread.start()

        while self.running:
            try:
                h, w = stdscr.getmaxyx()
                stdscr.erase()

                # Draw everything
                self.draw_border(stdscr, h, w)
                y = 2
                y = self.draw_header(stdscr, w, y)
                y += 1
                y = self.draw_stats(stdscr, w, y)
                y = self.draw_block_info(stdscr, w, y)
                self.draw_log(stdscr, w, y, h)
                self.draw_footer(stdscr, h, w)

                # Cursor blink effect
                blink = "_" if int(time.time() * 2) % 2 else " "
                try:
                    stdscr.addstr(h - 3, 3, f"READY. {blink}", curses.A_BOLD | curses.color_pair(2))
                except:
                    pass

                stdscr.refresh()

                # Handle input - poll multiple times per refresh
                for _ in range(5):
                    key = stdscr.getch()
                    if key == ord('q') or key == ord('Q'):
                        self.running = False
                        break
                    if key == 27:  # ESC
                        self.running = False
                        break
                    time.sleep(0.05)
                if not self.running:
                    break

            except KeyboardInterrupt:
                break

        # Cleanup
        if self.daemon_proc:
            self.daemon_proc.terminate()
            try:
                self.daemon_proc.wait(timeout=5)
            except:
                self.daemon_proc.kill()


def main():
    # Default daemon args
    script_dir = os.path.dirname(os.path.abspath(__file__))
    home = os.path.expanduser("~")
    daemon_args = [
        os.path.join(script_dir, "build/bin/c64chaind"),
        "--testnet", "--offline",
        f"--data-dir={home}/.c64chain",
        "--rpc-bind-port=29641",
        "--fixed-difficulty=100",
        "--log-level=1"
    ]

    # Allow custom args
    if len(sys.argv) > 1:
        daemon_args = sys.argv[1:]

    # Datasette loading animation (before curses takes over)
    import random
    colors = [
        "\033[41m", "\033[42m", "\033[43m", "\033[44m",
        "\033[45m", "\033[46m", "\033[47m", "\033[44m",
        "\033[41m", "\033[43m", "\033[42m", "\033[45m",
        "\033[46m", "\033[41m", "\033[44m", "\033[47m"
    ]
    reset = "\033[0m"
    
    print("\033[2J\033[H", end="")  # Clear screen
    print("\033[36m    PRESS PLAY ON TAPE\033[0m\n")
    time.sleep(1.5)
    print("\033[36m    OK\033[0m\n")
    time.sleep(0.5)
    
    random.seed()
    for frame in range(120):
        line = "    "
        tw = os.get_terminal_size().columns - 4
        for x in range(tw):
            ci = (x + frame * 3 + random.randint(0, 2)) % 16
            line += colors[ci] + " "
        line += reset
        print(line)
        time.sleep(0.05)
    
    print()
    time.sleep(0.5)
    print("\033[36m    FOUND C64CHAIN\033[0m")
    time.sleep(1.0)
    print("\033[36m    LOADING...\033[0m")
    time.sleep(1.5)
    print("\033[36m    READY.\033[0m\n")
    time.sleep(0.5)

    tui = C64NodeTUI()
    curses.wrapper(lambda stdscr: tui.run(stdscr, daemon_args))


if __name__ == "__main__":
    main()
