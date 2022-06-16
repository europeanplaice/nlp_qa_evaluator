# nlp_qa_evaluator

It evaluates the correctness of answers to questions based on the similarity between correct answers and students' answers. I am using `universal sentence encoder` inside the code to calculate similarity. It returns not only the correctness of answers, but also which part of the sentence is important.  

In evaluation, it masks the part of the sentence and calculates similarity to the correct answer. The masked sentence has the loss of information. The correctness difference between the full sentence and the masked sentence means the importance of the part of the sentence.

By repeating this process exhaustively to all the parts of the sentence, we can find where the important information exists.
## Example
`config.tsv`
```
question	correct_answer	students_answer	
Describe advantages of industrial robots.	It can complete tasks with precision and repeatability without requiring stoppages or breaks.	Generally, it does jobs faster and efficiently, but it often stops because of laziness. It gets bored easily.
産業革命について述べよ	産業革命は、18世紀後半にイギリスから始まった技術革新による産業構造の変化および経済発展のことである。	産業革命は、15世紀後半にドイツから始まった主に農業分野に関する技術革新のことである。
```

Run `python main.py`

`result_0.txt`  
```
question: Describe advantages of industrial robots.
correct_answer: It can complete tasks with precision and repeatability without requiring stoppages or breaks.
students_answer: Generally, it does jobs faster and efficiently, but it often stops because of laziness. It gets bored easily.

correctness: 0.20413890480995178
rank: 7 -> 0.06862731277942657, Generally, it
rank: 9 -> 0.06523540616035461, ly, it does
rank: 1 -> 0.09111086279153824, , it does jobs
rank: 12 -> 0.06327086687088013, it does jobs fast
rank: 13 -> 0.06200754642486572, does jobs faster
rank: 4 -> 0.07735158503055573, jobs faster and
rank: 19 -> 0.05433855950832367, faster and efficient
rank: 8 -> 0.06676959991455078, er and efficiently
rank: 6 -> 0.0736931562423706, and efficiently,
rank: 25 -> 0.023752450942993164, efficiently, but
rank: 23 -> 0.025838017463684082, ly, but it
rank: 26 -> 0.02346642315387726, , but it often
rank: 17 -> 0.05795574188232422, but it often stop
rank: 2 -> 0.08645569533109665, it often stops
rank: 3 -> 0.07821092009544373, often stops because
rank: 5 -> 0.0750008225440979, stops because of
rank: 20 -> 0.05427050590515137, s because of la
rank: 22 -> 0.04832765460014343, because of lazi
rank: 21 -> 0.050842851400375366, of laziness
rank: 11 -> 0.0634729266166687, laziness.
rank: 10 -> 0.06459644436836243, ziness. It
rank: 15 -> 0.058694690465927124, ness. It gets
rank: 14 -> 0.05934712290763855, . It gets bor
rank: 16 -> 0.0582873672246933, It gets bored
rank: 18 -> 0.05525369942188263, gets bored easily
rank: 24 -> 0.025737255811691284, bored easily.

```

`result_1.txt`
```
question: 産業革命について述べよ
correct_answer: 産業革命は、18世紀後半にイギリスから始まった技術革新による産業構造の変化および経済発展のことである。
students_answer: 産業革命は、15世紀後半にドイツから始まった主に農業分野に関する技術革新のことである。

correctness: 0.7697879672050476
rank: 1 -> 0.3845628499984741, 産業革命は
rank: 2 -> 0.3822498619556427, 産業革命は、
rank: 3 -> 0.32818105816841125, 革命は、15
rank: 4 -> 0.2389124631881714, は、15世紀
rank: 6 -> 0.1726365089416504, 、15世紀後半
rank: 8 -> 0.15859109163284302, 15世紀後半に
rank: 9 -> 0.13125938177108765, 世紀後半にドイツ
rank: 13 -> 0.1113702654838562, 後半にドイツから
rank: 16 -> 0.09778463840484619, にドイツから始まった
rank: 14 -> 0.10932236909866333, ドイツから始まった主に
rank: 15 -> 0.10312217473983765, から始まった主に農業
rank: 12 -> 0.11316812038421631, 始まった主に農業分野
rank: 17 -> 0.07674592733383179, 主に農業分野に関する
rank: 18 -> 0.07543438673019409, 農業分野に関する技術
rank: 11 -> 0.119717538356781, 分野に関する技術革新
rank: 10 -> 0.12682265043258667, に関する技術革新のこと
rank: 7 -> 0.15909916162490845, 技術革新のことである
rank: 5 -> 0.1732158064842224, 革新のことである。

```
