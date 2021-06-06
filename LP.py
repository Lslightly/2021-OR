from fractions import Fraction
import sys

class chart:

    def __init__(self, n, m, cj, bi, base, xishu):
        self.n = n  #   变量数
        self.m = m  #   等式数量
        self.cj = cj    #   cj
        self.bi = bi    #   bi
        self.xishu = xishu  #   系数矩阵
        self.base = base    #   每一行的基变量
        self.cj_zj = []     #   cj-zj



    def print_chart(self):
        self.print_cj()
        self.print_Cb_Xb_b_xi()
        self.print_rows()
        self.print_cj_zj()
        print()


    def print_cj(self):
        print('\tcj\t\t', end="")
        for j in range(self.n):
            print('{}\t'.format(self.cj[j]), end='')
        print()


    def print_Cb_Xb_b_xi(self):
        print('Cb\tXb\tb\t', end='')
        for j in range(self.n):
            print('x{}\t'.format(j+1), end='')
        print()
    

    def print_rows(self):
        for i in range(self.m):
            print('{}\tx{}\t{}\t'.format(self.cj[self.base[i]], self.base[i]+1, self.bi[i]), end='')
            for j in range(self.n):
                print('{}\t'.format(self.xishu[i][j]), end="")
            print()


    def calculate_cj_zj(self):
        self.cj_zj = []
        for j in range(self.n):
            temp_sum = 0
            for i in range(self.m):
                temp_sum += self.xishu[i][j]*self.cj[self.base[i]]
            self.cj_zj.append(self.cj[j] - temp_sum)


    def print_cj_zj(self):
        self.calculate_cj_zj()
        print('\tcj-zj\t\t', end='')
        for j in range(self.n):
            print('{}\t'.format(self.cj_zj[j]), end='')
        print()


    def row_multiple(self, row, mult):
        self.bi[row] *= mult
        for j in range(self.n):
            self.xishu[row][j] *= mult


    def row_multiple_add_to_another_row(self, source_row, mult, dest_row):
        self.bi[dest_row] += self.bi[source_row] * mult
        for j in range(self.n):
            self.xishu[dest_row][j] += self.xishu[source_row][j]*mult


    def baselize(self, row, j):     #   单位化某变元所在行的某列
        self.row_multiple(row, 1/self.xishu[row][j])
        for dest_row in range(self.m):
            if dest_row != row:
                self.row_multiple_add_to_another_row(row, -self.xishu[dest_row][j], dest_row)


    def in_out(self):
        self.calculate_cj_zj()
        if min(self.bi) < 0:
            i = self.bi.index(min(self.bi))
            if min(self.xishu[i]) > 0:
                print("无可行解")
                return -1
            else:
                minj = 0
                min_num = float('inf')
                for j in range(self.n):
                    if (self.xishu[i][j] != 0):
                        if (((self.xishu[i][j] < 0) & (self.cj_zj[j] < 0)) & (self.cj_zj[j]/self.xishu[i][j] < min_num)):
                            minj = j
                            min_num = self.cj_zj[j]/self.xishu[i][j]
                self.baselize(i, minj)
                self.base[i] = minj
                return 1
        elif max(self.cj_zj) > 0:
            j = self.cj_zj.index(max(self.cj_zj))
            mini = 0
            min_num = float('inf')
            for i in range(self.m):
                if self.xishu[i][j] != 0:
                    if ((self.xishu[i][j] > 0) & (self.bi[i]/self.xishu[i][j] < min_num)):
                        mini = i
                        min_num = self.bi[i]/self.xishu[i][j]
            self.baselize(mini, j)
            self.base[mini] = j
            return 1
        else:
            return 0


    def chart_calculate(self):
        self.print_chart()
        while (self.in_out() == 1):
            self.print_chart()
            if self.is_best():
                break


    def is_best(self):
        if (max(self.cj_zj)) < 0:
            return true


    def output_to_out(self):
        print(self.n)
        print(self.m)
        for i in range(self.m):
            for j in range(self.n):
                print(self.xishu[i][j], end=' ')
            print()
        for j in range(self.n):
            print(self.cj[j], end=' ')
        print()
        for i in range(self.m):
            print(self.bi[i], end=' ')
        print()
        for i in self.base:
            print(i+1, end=' ')
        print()


def print_arr(xishu_arr, bi, cj, n, m):
    for i in range(m):
        for j in range(n):
            if xishu_arr[i][j] > 0:
                print('+{}x_{} '.format(xishu_arr[i][j], j+1), end="")
            elif xishu_arr[i][j] == 0:
                print('        ', end="")
            else:
                print('{}x_{} '.format(j+1), end="")
        print('= {}'.format(bi[i]))





if __name__ == "__main__":
    file = open('data', 'r')
    sys.stdin = file
    n = int(input('变量个数:'))
    m = int(input('等式个数:'))
    print('输入系数矩阵:')
    xishu_arr = []
    for i in range(m):
        print("第{0}行:".format(i+1))
        xishu_arr.append(list(map(Fraction, input().rstrip().split())))
    cj = input('一次性输入权值cj:')
    cj = [Fraction(n) for n in cj.split()]
    bi = input('一次性输入边界值bi:')
    bi = [Fraction(x) for x in bi.split()]
    base = input('指定基变量:')
    print('\n\n\n\n')
    base = [int(i)-1 for i in base.split()]
    chart1 = chart(n, m, cj, bi, base, xishu_arr)
    chart1.chart_calculate()
    out = open('out', 'w')
    sys.stdout = out
    chart1.output_to_out()