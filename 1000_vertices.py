from graph.graph import Graph


gr1000 = Graph()
with open('1000.txt', 'r') as f:
    for l in f:
        try:
            line = l.split()[0:3]
            if len(line) < 3:
                continue
            gr1000.add_edge(int(line[0]), int(line[1]), int(line[2]))
        except:
            continue


has_cycle = gr1000.has_hamiltonial_cycle()

if has_cycle:
    print("Гамильтонов цикл в грфе есть")
else:
    print('Гамильтонова цикла в графе нет')

gr1000.make_closure()


has_cycle = gr1000.has_hamiltonial_cycle()

if has_cycle:
    print("Гамильтонов цикл в грфе есть")
else:
    print('Гамильтонова цикла в графе нет')
