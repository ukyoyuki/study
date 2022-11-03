import sys
import fasttext as ft

# モデルを作成
model = ft.train_unsupervised(input='../texts/yumeno/yumeno.txt')
# モデルを保存
model.save_model('model_yumeno.bin')

#print(model.get_dimension())
#print(model.get_word_vector('六つ'))
#print(model.words)
#print(model.predict('私'))
# or, cbow model :
#model = ft.train_unsupervised('data.txt', model='cbow')
#print(model.get_word_vector('の'))