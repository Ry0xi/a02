# ベースとなるイメージ
FROM python:3.9.7

# 作業ディレクトリの作成
RUN mkdir /app

# 作業ディレクトリの指定
WORKDIR /app

# カレントディレクトリのデータをコピーする
ADD . /app

# requirements.txtに指定してあるパッケージをインストールする
RUN pip install -r ./requirements.txt