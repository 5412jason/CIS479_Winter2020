from Learning import QLearning
from Maze import Map

def main():
    print("QLearning with 20,000 cycles")

    newMap = Map("walls.txt", "goals.txt", 7, 6)
    learning = QLearning(0.9, newMap)

    for x in range(1, 100):
        learning.run_cycle()

    print("\n")
    newMap.print_q_values()
    #newMap.print_n_values()
    return

if __name__ == "__main__":
    main()