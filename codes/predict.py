import os
import numpy as np
import fasttext as ft

path_models=os.path.join(os.path.abspath('..'),'models/')

target=ft.load_model(os.path.join(path_models,'target.bin'))
model1=ft.load_model(os.path.join(path_models,'model_dazai.bin'))
model2=ft.load_model(os.path.join(path_models,'model_yumeno.bin'))
model3=ft.load_model(os.path.join(path_models,'model_edogawa.bin'))

print('targetの単語数:',len(target.words))
print('model1の単語数:',len(model1.words))
print('model2の単語数:',len(model2.words))
print('model3の単語数:',len(model3.words))

def distance(target,list_models):
    #引数がFastText._FastTextクラスか判別
    if type(target) is not ft.FastText._FastText:
        return 
    else:
        #カウンター
        counter=1
        for model in list_models:
            #引数がFastText._FastTextクラスか判別
            if type(model) is not ft.FastText._FastText:
                break

            #著者モデルと検証用モデルで共通の単語を取得
            intersection=set(target.words)&set(model.words)
            list(intersection)
            # print(intersection)
            # print(f'model{counter}とtargetの共通の単語数:{len(intersection)}')
            #共通の単語のベクトルをリスト化
            vec_target= np.array([target[x] for x in intersection])
            vec_model=np.array([model[x] for x in intersection])

            #距離を計算するため
            diff=vec_target-vec_model
           
            #単語分散表現の数(ベクトル数）
            length=len(diff)
            #d = distance
            d=np.sum([np.power(x,2) for x in diff])/length 
            
            # print(f'targetとmodel{counter}の単語分散表現の平均距離:{d}')
            if counter == 1:
                print(f'targetと太宰モデルの分散表現の平均距離:{d}')
            elif counter == 2:
                print(f'targetと夢野モデルの分散表現の平均距離:{d}')
            elif counter == 3:
                print(f'targetと江戸川モデルの分散表現の平均距離:{d}')
            counter+=1
            
distance(target,[model1,model2,model3])