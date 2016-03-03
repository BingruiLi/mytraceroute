egrep -v '^trace|\*$' AF/24.text | awk '{print $2}' | sort -u > AF.routeip
