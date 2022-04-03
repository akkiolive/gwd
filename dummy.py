from random import randint



dwg_max = 10
with open("dummy.csv", "w") as f:
    for i in range(50):
        #pubn = randint(0,dwg_max)
        line = f"dwg{i},ram{i},pub"
        f.write(line + "\n")

        for j in range(dwg_max):
            if j == i or j > i:
                continue
            if randint(0, 100) < 10:
                line = f"dwg{j},ram{i},ext"
                f.write(line + "\n")

