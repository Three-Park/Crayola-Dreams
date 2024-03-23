# About Our Project
### :book: Fairy Taiary: 일기 속 소중한 순간을 동화 같은 그림으로 담아내는 AI 일기 서비스
해당 서비스는 바쁘게 살아가는 현대 사회 속 자신의 하루를 되짚어 볼 여유가 없는 현대인들을 타겟으로 삼았으며, 그들의 스트레스 해소를 위한 AI그림일기 서비스이다.<br>
해당 서비스를 통해 언제 어디서든 일기를 작성하며 자신의 하루를 기록함으로써 감정이나 생각을 정리하며 스트레스를 해소할 수 있다.<br> 
또한 동화같은 그림체 더해진 일기를 통해 동심을 자극하여 현실 사회를 살아가며 부족해진 감성을 채워주는 긍정적인 효과를 제공하고자 한다.

#### 
<details>
<summary><h1>⚙️About AI</h1></summary>
<div markdown="1">
<h2> 💡사용자 일기 다중 감정 분석</h2>
<h3>사용 모델 : KoBERT</h3>
<h4>Dataset : https://aihub.or.kr/aihubdata/data/view.do?currMenu=&topMenu=&aihubDataSe=data&dataSetSn=86 </h4>
<h4>많은 BERT 모델 중에서도 KoBERT를 사용한 이유는 "한국어"에 대해 많은 사전 학습이 이루어져 있고, 감정을 분석할 때, 긍정과 부정만으로 분류하는 것이 아닌 다중 분류가 가능한 것이 강점 존재<br><br> 따라서, 이러한 이유로 KoBERT 모델을 최종 모델로 선택을 하였고, 모델 구조 Customizing 및 FineTuning을 진행 </h4><br>
<h3>결과</h3>
  
  ![image](https://github.com/Three-Park/Crayola-Dreams/assets/79118751/20fa1c9b-106c-4ef6-bde7-15164dcdd014)


<h2> 💡일기 기반 자동 코멘트 생성</h2>
<h3>사용 모델 : KoGPT2</h3>
<h4>Dataset : https://github.com/songys/Chatbot_data </h4>
<h4>KoGPT2 모델은 문장을 "생성"해내는 모델이다. 따라서 일기 내용에 대한 코멘트를 달도록 구현하기 위해 입력 받은 내용에 대해 위로하거나 공감하거나 부드러운 표현으로 반응하고 문장을 생성해내도록 FineTuning을 진행</h4><br>

<h3>결과</h3>

![image](https://github.com/Three-Park/Crayola-Dreams/assets/79118751/c98495e2-2f9b-4f54-8d83-af7d3f07b0e8)

</details>
</div>


