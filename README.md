# iorScript
Lustre Test 스크립트 

포함된 것 
1. ior벤치마크 - iorMark.py
2. lustre iokit (obdfilter survey) 벤치마크 - 예정
3. 결과 추출기 - markAnalyzer.py 


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

# Run

포함된 .sh 참조

- iorMark
```
python3 totalMark/iorMark.py options_path results_path

(example) python3 totalMark/iorMark.py totalMark/options/test.options totalMark/results/test
```



- markAnalyzer
```
python3 totalMark/markAnalyzer.py results_path

(example) python3 totalMark/markAnalyzer.py totalMark/results/test
```

