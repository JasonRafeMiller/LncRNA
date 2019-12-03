grep  original class*.txt > 1.tmp
grep -c Noncoding class*.txt > 2.tmp
grep -c Coding class*.txt > 3.tmp

paste 1.tmp 2.tmp 3.tmp | tr ':' ' ' | awk '{print $2,$4,$6,$8;}' > seq.class.mutNoncoding.mutCoding.txt
