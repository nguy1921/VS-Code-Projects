class TowerOfHanoi:

    def __init__(self, num_disks, start='A', destination='C'):
        self.num_disks = num_disks
        self.start = start
        self.destination = destination

        self.towers = {
            'A': [],
            'B': [],
            'C': []
        }

        # Largest disk at bottom, smallest at top
        self.towers[start] = list(range(num_disks, 0, -1))

        self.moves = 0
        self.history = []

    # -----------------------------------------
    # DISPLAY
    # -----------------------------------------

    def draw_towers(self, clear=False):

        if clear:
            print("\033[2J\033[H", end="")

        width = self.num_disks * 2 + 3

        print("=" * (width * 3 + 8))

        # Tower labels
        print(
            " ".join(
                tower.center(width)
                for tower in self.towers
            )
        )

        # Draw disks from top to bottom
        for level in range(self.num_disks - 1, -1, -1):

            row = []

            for tower in self.towers.values():

                if level < len(tower):
                    disk = tower[level]
                    disk_visual = "[" + "=" * (disk * 2 - 1) + "]"
                else:
                    disk_visual = "|"

                row.append(disk_visual.center(width))

            print("   ".join(row))

        # Tower bases
        print("-" * (width * 3 + 8))

        print(f"Moves: {self.moves}")
        print(f"Minimum moves: {2 ** self.num_disks - 1}")

        print("=" * (width * 3 + 8))

    # -----------------------------------------
    # DISK MOVEMENT
    # -----------------------------------------

    def move_disk(self, source, destination):

        # Check that the tower names are valid
        if source not in self.towers or destination not in self.towers:
            print("Invalid tower!")
            return False

        # Cannot move a disk to the same tower
        if source == destination:
            print("Choose two different towers!")
            return False

        # Check whether source tower has disks
        if not self.towers[source]:
            print("Source tower is empty!")
            return False

        disk = self.towers[source][-1]

        # Check whether destination has a larger disk on top
        if self.towers[destination]:

            if self.towers[destination][-1] < disk:
                print("Invalid move! You cannot place a larger disk on a smaller disk.")
                return False

        # Perform the move
        self.towers[source].pop()
        self.towers[destination].append(disk)

        self.moves += 1

        # Record move for undo/history
        self.history.append((source, destination, disk))

        return True

    # -----------------------------------------
    # UNDO
    # -----------------------------------------

    def undo_move(self):

        if not self.history:
            print("There are no moves to undo!")
            return False

        source, destination, disk = self.history.pop()

        self.towers[destination].pop()
        self.towers[source].append(disk)

        self.moves -= 1

        return True

    # -----------------------------------------
    # RESTART
    # -----------------------------------------

    def restart(self):

        self.towers = {
            'A': [],
            'B': [],
            'C': []
        }

        self.towers[self.start] = list(
            range(self.num_disks, 0, -1)
        )

        self.moves = 0
        self.history.clear()

    # -----------------------------------------
    # SOLUTION CHECK
    # -----------------------------------------

    def is_solved(self):

        return len(self.towers[self.destination]) == self.num_disks

    # -----------------------------------------
    # RECURSIVE SOLVER
    # -----------------------------------------

    def solve(self, n, source, auxiliary, destination,
              step_by_step=False, delay=0.5):

        if n == 0:
            return

        # Move n-1 disks to auxiliary tower
        self.solve(
            n - 1,
            source,
            destination,
            auxiliary,
            step_by_step,
            delay
        )

        # Move largest remaining disk
        self.move_disk(source, destination)

        self.draw_towers(clear=True)

        print(f"\nMoving disk from {source} to {destination}")

        if step_by_step:
            input("\nPress Enter for next move...")
        else:
            import time
            time.sleep(delay)

        # Move n-1 disks onto destination
        self.solve(
            n - 1,
            auxiliary,
            source,
            destination,
            step_by_step,
            delay
        )



# -----------------------------------------
# User Interface Functions
# -----------------------------------------
def get_number_of_disks():

    while True:

        try:
            disks = int(input("Number of disks (1-8): "))

            if 1 <= disks <= 8:
                return disks

            print("Please enter a number between 1 and 8.")

        except ValueError:
            print("Please enter a valid integer.")


def get_tower(prompt):

    while True:

        tower = input(prompt).upper()

        if tower in ['A', 'B', 'C']:
            return tower

        print("Please choose A, B, or C.")


def configure_puzzle():

    print("\n--- Puzzle Configuration ---")

    disks = get_number_of_disks()

    start = get_tower("Starting tower (A/B/C): ")

    while True:

        destination = get_tower("Destination tower (A/B/C): ")

        if destination != start:
            break

        print("Starting and destination towers must be different!")

    return disks, start, destination


# -----------------------------------------
# Automatic Puzzle Solver Mode
# -----------------------------------------
def automatic_mode():

    disks, start, destination = configure_puzzle()

    game = TowerOfHanoi(disks, start, destination)

    auxiliary = next(
        tower for tower in ['A', 'B', 'C']
        if tower != start and tower != destination
    )

    print("\n--- Automatic Solver ---")

    game.draw_towers()

    print("\n1. Animated solving")
    print("2. Step-by-step solving")

    choice = input("\nChoose an option: ")

    if choice == '1':

        game.solve(
            disks,
            start,
            auxiliary,
            destination,
            delay=0.5
        )

    elif choice == '2':

        game.solve(
            disks,
            start,
            auxiliary,
            destination,
            step_by_step=True
        )

    else:
        print("Invalid selection!")
        return

    print("\nPuzzle solved!")
    print(f"Total moves: {game.moves}")
    print(f"Optimal moves: {2 ** disks - 1}")

    input("\nPress Enter to return to the menu...")


# -----------------------------------------
# Manual Puzzle Solving Mode
# -----------------------------------------
def manual_mode():

    disks, start, destination = configure_puzzle()

    game = TowerOfHanoi(disks, start, destination)

    print("\n--- Manual Mode ---")
    print("Move disks using commands such as: A C")
    print("U = Undo | H = History | R = Restart | Q = Quit")

    while True:

        game.draw_towers()

        if game.is_solved():

            print("\nCongratulations! You solved the puzzle!")
            print(f"Your moves: {game.moves}")
            print(f"Minimum moves: {2 ** disks - 1}")

            break

        command = input("\nYour move: ").upper().strip()

        if command == 'Q':
            break

        elif command == 'U':

            if game.undo_move():
                print("Last move undone.")

        elif command == 'H':

            print("\n--- Move History ---")

            if not game.history:
                print("No moves yet.")

            for index, move in enumerate(game.history, start=1):

                source, destination, disk = move

                print(
                    f"{index}. Disk {disk}: "
                    f"{source} -> {destination}"
                )

            input("\nPress Enter to continue...")

        elif command == 'R':

            confirm = input("Restart puzzle? (y/n): ").lower()

            if confirm == 'y':
                game.restart()

        else:

            parts = command.split()

            if len(parts) != 2:
                print("Invalid command! Example: A C")
                input("Press Enter to continue...")
                continue

            source, destination = parts

            game.move_disk(source, destination)

            if not game.is_solved():
                input("\nPress Enter to continue...")


# -----------------------------------------
# Main Menu Initialization
# -----------------------------------------
def main_menu():

    while True:

        print("\n")
        print("=" * 40)
        print("       TOWER OF HANOI SOLVER")
        print("=" * 40)

        print("1. Automatic Solver")
        print("2. Manual Mode")
        print("3. Exit")

        print("=" * 40)

        choice = input("\nSelect an option: ")

        if choice == '1':
            automatic_mode()

        elif choice == '2':
            manual_mode()

        elif choice == '3':
            print("\nThanks for playing!")
            break

        else:
            print("\nInvalid selection!")


def main():

    main_menu()


if __name__ == "__main__":
    main()