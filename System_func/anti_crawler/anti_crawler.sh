#!/usr/bin/env bash
line_num=(500 5000 10000 50000 100000)
for num in ${line_num[@]};
do
  case $num in
      500)    limit=100
      ;;
      5000)   limit=500
      ;;
      10000)  limit=1000
      ;;
      50000)  limit=2000
      ;;
      100000) limit=5000
      ;;
  esac
  IPS=`tail -n $num /var/log/nginx/access.log|grep -E -v "ELB-HealthChecker/1.0|HEAD"|grep -E "GET /cruises/[0-9]*"|awk \
  '{IP[$1]++}END{ for(N in IP) print N, IP[N]}'|sort -nr -k 2|awk  '{if($2>=limit) print $1}' limit=$limit`
  for IP in $IPS;
    do
      grep $IP crawlerip.txt;
      if [ $? -ne 0 ]; then
        echo $IP >> crawlerip.txt
      fi
    done
done

*/10 * * * * /bin/bash /root/anti_crawler.sh >> /dev/null 2>&1