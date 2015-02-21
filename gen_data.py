import random
def generate_data():
    print("Generating data...")
    for x in range(5):
        name = "random_vals_" + str(x) + ".txt"
        f = open(name,"w")
        for _ in range(100000):
            f.write(str(random.uniform(0,1)) + "\n")
        f.close()
        print(name)
    