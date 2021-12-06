# iorScript
Lustre Test 스크립트 

포함된 것 
1. ior벤치마크 - iorMark.py
2. lustre iokit (obdfilter survey) 벤치마크 - 예정
3. 1,2를 포함하는 totalMark.py - 미완
4. 결과 추출기 - markAnalyzer.py 
5. 폴더내의 모든 파일 크기 분석기 - fileStatistics.py


# Step
1. Load MPI module (# module load mpi/openmpi-x86_64)

2. Make options for test (totalMark/options/)
  - options는 .options의 확장자를 가져야 함
  - key:val1,val2 형식 (아래는 key에 대한 설명)
    - target:테스트 폴더, 미리 stripe가 설정된 lustre 폴더
    - stripe:target에서 설정된 lustre stripe 갯수
    - block:-b 옵션 변수 (block size)
    - transfer:-t 옵션 변수 (transfer size)
    - process: 측정 thread 갯수
    
4. iorMark 실행
5. markAnalyzer 실행

6. (옵션) fileStatistics를 실행해서 참고

# Run

포함된 .sh 참조

- totalMark

python3 totalMark.py options_path results_path

```
python3 totalMark.py options/test.options results/test/
```



- markAnalyzer

python3 markAnalyzer.py results_path NUMBER_OF_OST OST_TYPE

OST_TYPE
  1:SSD
  2:HDD
  3:MIXED

```
python3 markAnalyzer.py results/test/ 4 2
```

- fileStatistics

python3 markAnalyzer.py target_dir_path

```
python3 markAnalyzer.py /home/byeonghyun/repo
```
