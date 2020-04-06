from Learning import QLearning
from Maze import Map

def main():
    print("QLearning with 20,000 cycles")

    newMap = Map("walls.txt", "goals.txt", 7, 6)
    learning = QLearning(0.9, newMap)
    for x in range(1, 20000): #itterate over this 20000 times
        print("\nIteration: " + str(x))
        print("Q Values")
        newMap.print_q_values()
        print("\nN Values")
        newMap.print_n_values()
        print("\nOptimal Solution")
        newMap.print_optimal_path()
        learning.run_cycle()

    print("\n Final Map")
    print("Q Values")
    newMap.print_q_values()
    print("\nN Values")
    newMap.print_n_values()
    print("\nOptimal Solution")
    newMap.print_optimal_path()
    return

if __name__ == "__main__":
    main()