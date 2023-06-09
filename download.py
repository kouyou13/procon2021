import subprocess

def download():
    subprocess.run(["python3","procon32.py","download","--token=37a76c1de6d25f4b30d248f44062166811c9d0d4df361d7cad32336ed712ef73"])
    # print("hello")
    # time.sleep(3) #画像取得に時間がかかる
    
# ppm画像のヘッダ情報取得
def ImgInfo():
    infile = open("./problem.ppm", 'r', encoding='utf-8', errors='ignore')
    for _ in range(6):
        num = infile.readline().split()
        img_info.append(num)
    return img_info

if __name__ == '__main__':
    download()
    img_info = [] # 画像情報を格納する配列
    img_info = ImgInfo() # 画像情報の取得
    
    choise_count=int(img_info[2][1]) #選択回数
    w_image_size = int(img_info[4][0]) #元画像の幅
    h_image_size = int(img_info[4][1]) #元画像の高さ
    w_grid_size = int(img_info[1][1]) #横の1辺が何ピースか
    h_grid_size = int(img_info[1][2]) #縦の1辺が何ピースか
    
    print('選択回数:',choise_count)
    # print('横x縦 [pixel]:',w_image_size, '*', h_image_size)
    print('横x縦:',w_grid_size, '*', h_grid_size)