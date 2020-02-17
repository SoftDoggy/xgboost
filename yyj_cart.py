import math

Label_true = 'agree'
Label_false = 'refuse'
feat_enum = [['youth', 'mid', 'elder'],
             ['yes'],
             ['yes'],
             []]  # 1.5, 2.5


def create_samples():
    ''''' 
    提供训练样本集 
    每个example由多个特征值+1个分类标签值组成 
    比如第一个example=['youth', 'no', 'no', '1', 'refuse'],此样本的含义可以解读为： 
    如果一个人的条件是：youth age，no working, no house, 信誉值credit为1
    则此类人会被分类到refuse一类中，即在相亲中被拒绝(也可以理解为银行拒绝为此人贷款)
    每个example的特征值类型为： 
    ['age', 'working', 'house', 'credit'] 
    每个example的分类标签class_label取值范围为：'refuse'或者'agree' 
    '''
    data_list = [['youth', 'no', 'no', '1', 'refuse'],
                 ['youth', 'no', 'no', '2', 'refuse'],
                 ['youth', 'yes', 'no', '2', 'agree'],
                 ['youth', 'yes', 'yes', '1', 'agree'],
                 ['youth', 'no', 'no', '1', 'refuse'],
                 ['mid', 'no', 'no', '1', 'refuse'],
                 ['mid', 'no', 'no', '2', 'refuse'],
                 ['mid', 'yes', 'yes', '2', 'agree'],
                 ['mid', 'no', 'yes', '3', 'agree'],
                 ['mid', 'no', 'yes', '3', 'agree'],
                 ['elder', 'no', 'yes', '3', 'agree'],
                 ['elder', 'no', 'yes', '2', 'agree'],
                 ['elder', 'yes', 'no', '2', 'agree'],
                 ['elder', 'yes', 'no', '3', 'agree'],
                 ['elder', 'no', 'no', '1', 'refuse']]
    feat_list = ['age', 'working', 'house', 'credit']
    return data_list, feat_list


class TreeNode:
    def __init__(self, data_list):
        if len(data_list) == 0:
            # print("node return")
            return
        self.data_list = data_list
        self.gini = 1
        self.left = TreeNode([])
        self.right = TreeNode([])
        self.level = 1
        self.is_leaf = False
        self.feat_index = -1
        self.feat_detail_index = -1


class CartTree:
    def __init__(self, data_list, feat_list):
        self.root = TreeNode(data_list)
        self.feat_list = feat_list
        self.depth = 1
        self.max_depth = 3
        self.gini_threadhold = 0.1

    def calculate_gini(self, data_list):
        if len(data_list) == 0:
            return 1
        true_num = 0
        false_num = 0
        for data_row in data_list:
            if data_row[-1] == Label_true:
                true_num += 1
            else:
                false_num += 1
        return 1 - math.pow(true_num / len(data_list), 2) - math.pow(false_num / len(data_list), 2)

    def calculate_root_gini(self):
        self.root.gini = self.calculate_gini(self.data_list)

    def work(self, node):
        if node.level > self.max_depth:
            node.is_leaf = True
            return
        node.gini = self.calculate_gini(node.data_list)
        print("level")
        print(node.level)
        print("gini")
        print(node.gini)
        if node.gini <= self.gini_threadhold:
            node.is_leaf = True
            return
        gini_gain = []
        for index, feat_row in enumerate(feat_enum):
            gini_gain.append([])
            left_list = []
            right_list = []
            # 对应离散值
            if not len(feat_row) == 0:
                # 遍历选择对应feat
                for feat in feat_row:
                    left_list = []
                    right_list = []
                    for data_row in node.data_list:
                        if data_row[index] == feat:
                            left_list.append(data_row)
                        else:
                            right_list.append(data_row)
                    left_gini = self.calculate_gini(left_list)
                    right_gini = self.calculate_gini(right_list)
                    # print(left_gini)
                    # print(right_gini)
                    # print(len(left_list) / len(node.data_list))
                    # print(len(right_list) / len(node.data_list))
                    gini_gain_num = node.gini - len(left_list) / len(node.data_list) * left_gini - len(
                        right_list) / len(node.data_list) * right_gini
                    # print('gini_gain_num ' + str(gini_gain_num))
                    gini_gain[index].append(gini_gain_num)
            # 连续值
            else:
                # 遍历找到需要取的所有值
                values_taken = []
                all_values = []
                for data_row in node.data_list:
                    all_values.append(data_row[index])
                all_values = list(set(all_values))
                all_values.sort()
                print(all_values)
                for i in range(0, len(all_values) - 1):
                    values_taken.append((float(all_values[i]) + float(all_values[i + 1])) / 2.0)
                print(values_taken)
                # feat_enum[index] = values_taken
                for values in values_taken:
                    left_list = []
                    right_list = []
                    for data_row in node.data_list:
                        if float(data_row[index]) <= values:
                            left_list.append(data_row)
                        else:
                            right_list.append(data_row)
                    left_gini = self.calculate_gini(left_list)
                    right_gini = self.calculate_gini(right_list)
                    gini_gain_num = node.gini - len(left_list) / len(node.data_list) * left_gini - len(
                        right_list) / len(node.data_list) * right_gini
                    gini_gain[index].append(gini_gain_num)
        print(gini_gain)
        max_feat_index = 0
        max_feat_detail_index = 0
        max = gini_gain[0][0]
        for row_index, gini_row in enumerate(gini_gain):
            for detail_index, feat_detail in enumerate(gini_row):
                if max < feat_detail:
                    max_feat_index = row_index
                    max_feat_detail_index = detail_index
                    max = feat_detail
        print(max_feat_index)
        print(max_feat_detail_index)
        print(max)
        node.feat_index = max_feat_index
        node.feat_detail_index = max_feat_detail_index
        left_list = []
        right_list = []
        feat = feat_enum[max_feat_index][max_feat_detail_index]
        for data_row in node.data_list:
            if data_row[max_feat_index] == feat:
                left_list.append(data_row)
            else:
                right_list.append(data_row)
        node.left = TreeNode(left_list)
        node.right = TreeNode(right_list)
        node.left.level = node.level + 1
        node.right.level = node.level + 1
        print(left_list)
        print(right_list)
        print("left node")
        self.work(node.left)
        print("right node")
        self.work(node.right)

    def print_dict(self):
        print("CartTree {")
        self.print_sub(self.root)
        print("}")

    def print_sub(self, node):
        if not node.is_leaf:
            print(self.feat_list[node.feat_index] + " :{")
            if node.left.is_leaf:
                print(node.left.data_list[0][node.feat_index] + " : " + node.left.data_list[0][-1])
            else:
                print(node.left.data_list[0][node.feat_index] + " :{")
                self.print_sub(node.left)
                print("}")
            if node.right.is_leaf:
                print(node.right.data_list[0][node.feat_index] + " : " + node.right.data_list[0][-1])
            else:
                print(node.right.data_list[0][node.feat_index] + " :{")
                self.print_sub(node.right)
                print("}")
            print("}")


data_list, feat_list = create_samples()
cart_tree = CartTree(data_list, feat_list)
cart_tree.work(cart_tree.root)
cart_tree.print_dict()
