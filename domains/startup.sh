#!/usr/bin/bash
#30 22 * * * nohup sh /home/shell/start_domain.sh >>/home/sec/log/scrapy_domain.log 2>&1 &
cd /home/script/domains/
/usr/bin/python3 -m scrapy crawl domains