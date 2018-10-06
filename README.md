# A crawler to collect hot products on https://tw.buy.yahoo.com

## Require

* [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)(docker)
* [Docker Compose](https://docs.docker.com/compose/install/)(docker-compose)

## Quick Start

* Checkout repo
  * `git clone git@github.com:yarencheng/juvo-interview.git`
  * `cd juvo-interview`
* Build & Run
  * `docker-compose up --build --abort-on-container-exit`
* After 5~30 minutes, see `output.csv`.

## Monitor

* When crawler is running, monitor browser activity via a web VNC client: `http://localhost:6080/vnc.html`
* Password: `secret`

## Columns of output.csv

* 1st Category: E.g. `服裝 / 飾品 / 配件`
* 2nd Category: E.g. `流行女裝`
* 3rd Category: E.g. `新品上市`
* 4th Category: E.g. `秋換季NEW!!`
* product name: E.g. `LIYO理優MIT打摺造型西裝褲E711010 S-XXL`