# ベースとなるイメージ
FROM node:16.9

# 作業ディレクトリの作成
RUN mkdir /app

# 作業ディレクトリの指定
WORKDIR /app

# カレントディレクトリのデータをコピーする
ADD . /app

RUN apt-get update -y && \
    apt-get upgrade -y && \
    npm install -g npm && \
    npm install -g nuxt && \
    npm install

# permission denied エラーを回避するため
RUN mkdir node_modules/.cache && chmod -R 777 node_modules/.cache

EXPOSE 3000
ENV HOST 0.0.0.0