import xgboost as xgb

rawData = [[2,4],[3,4], [1,2], [4,5], [7,8]]
label = [6,7,3,9,15]

dtrain = xgb.DMatrix(rawData, label=label)
deval = xgb.DMatrix([[3,5],[3,6]], label=[8,9])

param = {'max_depth': 2, 'eta': 1, 'silent': 1, 'objective': 'reg:linear'}
# param['nthread'] = 4
# param['eval_metric'] = 'auc'

evallist = [(deval, 'eval'), (dtrain, 'train')]


num_round = 10
bst = xgb.train(param, dtrain, num_round, evallist)

bst.save_model('0001.model')

dtest = xgb.DMatrix([[2,4], [7,8]])
ypred = bst.predict(dtest)

print(ypred)