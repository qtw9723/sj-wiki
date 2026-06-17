#!/bin/sh
cd /Users/sangjun/sj-wiki
for name in 종합기획서 기술설계서 기능화면정의서; do
  textutil -convert txt -output ".extract_${name}.txt" "raw/교회-일정공유캘린더-${name}.docx"
  echo "done ${name}"
done
