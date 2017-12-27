from src.ullmann import *


if __name__ == '__main__':
    graphs = Ullmann.read_file('../graphDB/testdb.data')
    queries = Ullmann.read_file('../graphDB/testq.data')
    # graphs = Ullmann.read_file('../graphDB/mygraphdb.data')
    # queries = Ullmann.read_file('../graphDB/Q4.my')

    print(len(graphs))
    print(len(queries))

    for i in queries:
        for j in graphs:
            solver = Ullmann(i, j)
            solver.search()

    # for i in queries:
    #     for j in graphs:
    #         if len(i.vertices) <= len(j.vertices):
    #             trans_mat = Ullmann.get_trans_mat(i, j)
    #             print(trans_mat)
    #             print(Ullmann.refinement(i, j, trans_mat))

