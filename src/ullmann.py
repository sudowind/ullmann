from src.graph import *


class Ullmann(object):

    def __init__(self, g_1, g_2):
        self.g_1 = g_1
        self.g_2 = g_2
        # print(g_1.get_matrix())
        # print(g_2.get_matrix())
        # print()

    @staticmethod
    def check_mat(g_1, g_2, mat):
        mat_1 = g_1.get_matrix()
        mat_2 = g_2.get_matrix()
        mat_3 = mat.dot(mat.dot(mat_2).T)
        for i in range(mat_1.shape[0]):
            for j in range(mat_1.shape[1]):
                if mat_1[i][j]:
                    if not mat_3[i][j]:
                        return False
        # print(mat_3)
        return True

    @staticmethod
    def refinement(g_1, g_2, mat):
        mat_1 = g_1.get_matrix()
        mat_2 = g_2.get_matrix()
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                if mat[i][j]:
                    for x in range(mat_1.shape[0]):
                        if mat_1[i][x]:
                            flag = False
                            for y in range(mat_2.shape[0]):
                                if mat[x][y] * mat_2[y][j]:
                                    flag = True
                                    break
                            if not flag:
                                mat[i][j] = 0
                    if not mat[i][j]:
                        break
        return mat

    @staticmethod
    def mat_fail(mat):
        for i in mat:
            if sum(i) == 0:
                return True
        return False

    @staticmethod
    def get_trans_mat(g_1, g_2):
        m_1 = g_1.get_matrix()
        m_2 = g_2.get_matrix()

        mat = np.zeros((len(g_1.vertices), len(g_2.vertices)))
        for i in g_1.vertices:
            for j in g_2.vertices:
                if i.vlb == j.vlb and len(i.neighbors) <= len(j.neighbors):
                    mat[i.vid][j.vid] = 1
        return mat

    @staticmethod
    def read_file(path):
        graphs = []
        with open(path) as f_in:
            tmp = Graph()
            for i in f_in.readlines():
                line = i.strip().split()
                if 't' in line:
                    if not len(tmp.vertices) == 0:
                        graphs.append(tmp)
                    tmp = Graph()
                elif 'v' in line:
                    tmp.add_vertex(*line[1:])
                elif 'e' in line:
                    tmp.add_edges(*line[1:])
        return graphs

    def search(self):
        p_1 = len(self.g_1.vertices)
        p_2 = len(self.g_2.vertices)
        trans_mat = self.get_trans_mat(self.g_1, self.g_2)
        trans_mat = self.refinement(self.g_1, self.g_2, trans_mat)
        if self.mat_fail(trans_mat):
            return
        mats = [trans_mat.copy() for _ in range(p_1)]   # store mat copy in depth d
        col_used = [0 for _ in range(p_2 + 1)]   # F in paper, 0 or 1
        d = 0   # depth
        k = 0   # column id
        depth_marker = [-1 for _ in range(p_1 + 1)]  # H in paper

        if d == 0:
            k = depth_marker[0]
        else:
            k = -1
        count = 0
        while d >= 0:
            able = False
            for j in range(k + 1, p_2):
                if trans_mat[d][j] == 1 and col_used[j] == 0:
                    # 本层是否还有候选项
                    able = True
                    col_used[j] = 1
                    depth_marker[d] = j
                    # 找到了候选项，更新矩阵
                    for col in range(p_2):
                        if col != j:
                            trans_mat[d][col] = 0
                    tmp = self.refinement(self.g_1, self.g_2, trans_mat.copy())
                    if self.mat_fail(tmp):
                        able = False
                        trans_mat = mats[d]
                        continue
                    break
            # 进入下一层
            if able:
                d += 1
                if d == p_1:
                    # 已经是最后一层，输出结果
                    if self.check_mat(self.g_1, self.g_2, trans_mat.copy()):
                        count += 1
                        print(trans_mat)
                        # print()
                    able = False
                else:
                    # 进入下一层，保留下一层的搜索矩阵
                    # trans_mat = self.refinement(self.g_1, self.g_2, trans_mat.copy())
                    mats[d] = trans_mat.copy()
                    k = depth_marker[d]

            if not able:
                if d == 0:
                    print('total: {}'.format(count))
                    return
                # 回溯
                depth_marker[d] = -1
                d -= 1
                trans_mat = mats[d].copy()
                k = depth_marker[d]
                col_used[depth_marker[d]] = 0
