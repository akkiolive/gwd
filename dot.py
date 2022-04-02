


import pydot

# read file
with open("rams_output.csv", encoding="utf8") as f:
    lines = f.read().split("\n")

# class definition
class BASE:
    def __init__(self):
        self.name
    
    def __eq__(self, other):
        if not isinstance(other, BASE):
            return NotImplemented
        return self.name == other.name
    def __ne__(self, other):
        if not isinstance(other, BASE):
            return NotImplemented
        return self.name != other.name
    def __lt__(self, other):
        if not isinstance(other, BASE):
            return NotImplemented
        return self.name < other.name
    def __le__(self, other):
        if not isinstance(other, BASE):
            return NotImplemented
        return self.name <= other.name
    def __gt__(self, other):
        if not isinstance(other, BASE):
            return NotImplemented
        return self.name > other.name
    def __ge__(self, other):
        if not isinstance(other, BASE):
            return NotImplemented
        return self.name >= other.name
        
class DWG(BASE):
    def __init__(self, name=""):
        self.name = name
        self.func_name = ""
        self.rams_public = []
        self.rams_extern = []
        self.calibs_public = []
        self.calibs_extern = []
    
    @property
    def node_name(self):
        return self.name.replace("-", "_")

    @property
    def record_ext(self):
        tmp = ""
        for n, ram in enumerate(self.rams_extern):
            if n >= 1:
                tmp += "|"
            tmp += f"<{ram.node_name}>{ram.name}"
        return tmp
    
    @property
    def record_pub(self):
        tmp = ""
        for n, ram in enumerate(self.rams_public):
            if n >= 1:
                tmp += "|"
            tmp += f"<{ram.node_name}>{ram.name}"
        return tmp

    def sort(self):
        self.rams_extern.sort()
        self.rams_public.sort()
        self.calibs_extern.sort()
        self.calibs_public.sort()

class RAM(BASE):
    def __init__(self, name=""):
        self.name = name
        self.dwgs_variable = []
        self.dwgs_extern = []

    def sort(self):
        self.dwgs_variable.sort()
        self.dwgs_extern.sort()
    
    @property
    def node_name(self):
        return self.name.replace("-", "_")


# load data
dwgs = {}
rams = {}

for line_no, line in enumerate(lines):
    line = line.strip()
    if line_no <= -1 or not line:
        continue

    dwg_name = line.split(",")[0]
    ram_name = line.split(",")[1]
    ram_or_calib = "ram"
    ext_or_pub = line.split(",")[2]

    print(dwg_name, ram_name, ram_or_calib, ext_or_pub)

    if dwg_name not in dwgs:
        dwgs[dwg_name] = DWG(dwg_name)

    dwg = dwgs[dwg_name]
    
    if ram_name not in rams:
        rams[ram_name] = RAM(ram_name)

    ram = rams[ram_name]

    if ram_or_calib == "ram":
        if ext_or_pub == "pub":
            dwg.rams_public.append(ram)
            ram.dwgs_variable.append(dwg)
        else:
            dwg.rams_extern.append(ram)
            ram.dwgs_extern.append(dwg)
    else:
        if ext_or_pub == "pub":
            dwg.calibs_public.append(ram)
        else:
            dwg.calibs_extern.append(ram)


# sort
for item in list(dwgs.items()) + list(rams.items()):
    item[1].sort()

nodes = []
nodes_str = ""

edges = []
edges_str = ""

# make nodes
for dwg_name in dwgs:
    dwg = dwgs[dwg_name]
    node = f"{dwg.node_name} [ shape=record, label=\"{dwg.name}|{{{{{dwg.record_ext}}}||{{{dwg.record_pub}}}}}\" ]"
    nodes_str += node + "\n"

    print(node)

# make edges
for ram_name in rams:
    ram = rams[ram_name]

    for dwg_v in ram.dwgs_variable:
        for dwg_e in ram.dwgs_extern:
            edge_str = f"{dwg_v.node_name}:{ram.node_name} -> {dwg_e.node_name}:{ram.node_name}"
            edges_str += edge_str + "\n"

# make dot dataa
dot_data = "Digraph G { "  +"\n"\
         + "    graph [rankdir=LR]"  +"\n"\
         + "    node []"  +"\n"\
         + "    " +"\n"\
         +f"    {nodes_str}"  +"\n"\
         + "    "  +"\n"\
         +f"    {edges_str}"  +"\n"\
         + "    "  +"\n"\
         + "}"

print(dot_data)

# make graph
graph = pydot.graph_from_dot_data(dot_data)
print(graph)
graph[0].write_jpeg("temp.jpg", prog="dot")







    



