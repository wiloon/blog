# wiloon.com
    date '+%Y-%m-%d %H:%M:%S' && ls -lR content/post |grep '\.md'|wc -l && find content/post -name '*.md' -exec wc -w '{}' \; > /tmp/foo.txt && awk '{sum+=$1} END {print sum}' /tmp/foo.txt
    

