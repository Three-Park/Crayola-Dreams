package com.example.myapplication;

import android.app.Activity;
import android.os.Bundle;

public class LoadingActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_loading);

        // 여기서 서버로 일기 내용을 전송하고, 그림 변환을 완료할 때까지 기다립니다.
        // 일단은 예시로 Thread를 사용해 딜레이를 줍니다. 실제로는 서버의 응답을 기다려야 합니다.
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    // 예시로 5초간 대기한다고 가정
                    Thread.sleep(5000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                // 그림 생성이 완료되면 다음 화면으로 이동하거나 결과를 표시
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        // 결과 화면으로 이동 또는 결과 표시
                        finish(); // 로딩 화면 종료
                    }
                });
            }
        }).start();
    }
}
