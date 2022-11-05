import os
import glob
import csv
import numpy as np
import fasttext as ft

dazai = glob.glob('../texts/dazai/*.txt')
edogawa=glob.glob('../texts/edogawa/*.txt')
yumeno=glob.glob('../texts/yumeno/*.txt')

txt_files=list()
txt_files.append(dazai)
txt_files.append(edogawa)
txt_files.append(yumeno)

# print(txt_files)

path_models=os.path.join(os.path.abspath('..'),'models/')
model1=ft.load_model(os.path.join(path_models,'model_dazai.bin'))
model2=ft.load_model(os.path.join(path_models,'model_edogawa.bin'))
model3=ft.load_model(os.path.join(path_models,'model_yumeno.bin'))

def distance(target_path,target,list_models):
    #引数がFastText._FastTextクラスか判別
    if type(target) is not ft.FastText._FastText:
        return 
    else:
        #カウンター
        counter=1
        d_list=list()
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
            d_list.append(d)
            # print(f'targetとmodel{counter}の単語分散表現の平均距離:{d}')
            """ if counter == 1:
                print(f'{os.path.basename(target_path)}と太宰モデルの分散表現の平均距離:{d}')
            elif counter == 2:
                print(f'{os.path.basename(target_path)}と夢野モデルの分散表現の平均距離:{d}')
            elif counter == 3:
                print(f'{os.path.basename(target_path)}と江戸川モデルの分散表現の平均距離:{d}') """
            counter+=1
            
    return d_list

with open('../data/data.csv','w') as f:
    writer = csv.writer(f)

    for auth in txt_files:
        
        for target_path in auth:
            # writer.writerow(target_path)
            target = ft.train_unsupervised(input=target_path)
            print(os.path.commonprefix(auth).strip('../texts/'))
            writer.writerow([os.path.commonprefix(auth).strip(',')])
            writer.writerow([os.path.basename(target_path),''])
            # print(f'{target_path}の単語数:',len(target.words))gi
            # print('太宰モデルの単語数:',len(model1.words))
            # print('江戸川モデルの単語数:',len(model2.words))
            # print('夢野モデルの単語数:',len(model3.words))  
            
            d_list=distance(target_path,target,[model1,model2,model3])
            writer.writerow(d_list)
            min=np.min(d_list)

            for i in range(len(d_list)):
                if min == d_list[i]:
                    if i==0 :
                        writer.writerow(['太宰',d_list[i]])
                    elif i==1:
                        writer.writerow(['江戸川',d_list[i]])
                    elif i==2:
                        writer.writerow(['夢野',d_list[i]])
            writer.writerow(['CRLF'])

# print(txt_files)
# モデルを作成
# model = ft.train_unsupervised(input='../texts/target.txt')
# モデルを保存
# model.save_model('target.bin')

#print(model.get_dimension())
#print(model.get_word_vector('六つ'))
#print(model.words)
#print(model.predict('私'))
# or, cbow model :
#model = ft.train_unsupervised('data.txt', model='cbow')
#print(model.get_word_vector('の'))
""" 
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
            
distance(target,[model1,model2,model3]) """