import random
def generate_data():
    print("Generating data...")
    for x in range(5):
        name = "random_vals_" + str(x) + ".txt"
        f = open(name,"w")
        if x is 1:
            for _ in range(100000): f.write()
        else:
            for _ in range(100000):
                f.write(str(random.uniform(0,1)) + "\n")
            f.close()
        print(name)
        
def generate_uniform(V):
    prob = 1.0/V
    f = open("uniform_model.txt","w")
    for _ in range(17354):
        f.write(str(prob)+"\n")
    f.close()
        
        
    