from Learning import QLearning
from Maze import Map

def main():
    print("QLearning with 20,000 cycles")

    newMap = Map("walls.txt", "goals.txt", 7, 7)
    learning = QLearning(0.9, newMap)

    for x in range(1, 5):
        learning.run_cycle()

    newMap.print_q_values()
    print("\n")
    #newMap.print_n_values()
    return

if __name__ == "__main__":
    main()