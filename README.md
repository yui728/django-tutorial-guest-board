# django-tutorial-guest-board
- [DjangoによるWebアプリケーション開発入門 ゲストボードを作ろう](https://eiry.bitbucket.io/tutorials/guest_board/index.html)の実装
  - Django 2.2対応
- Docker-composeを用いてdocker上で稼働できるように設定

## ディレクトリ構成
- src：[DjangoによるWebアプリケーション開発入門 ゲストボードを作ろう](https://eiry.bitbucket.io/tutorials/guest_board/index.html)の実装
- docker：docker設定
  - django-server：Djangoアプリケーションをgunicorn上で動かすためのDockerfile
  - nginx：nginxコンテナをDjangoアプリケーション+gunicornコンテナ、静的ファイルへのプロキシサーバにするための設定
- docker-compose.yml：Djangoアプリケーション+gunicornコンテナとnginxコンテナの起動・ボリューム連携設定