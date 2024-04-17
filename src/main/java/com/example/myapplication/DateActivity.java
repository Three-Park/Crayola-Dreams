package com.example.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class DateActivity extends Activity {
    private TextView selectedDateTextView;
    private TextView diaryTextView;
    private Button addDiaryButton;
    private String selectedDate;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_date);

        selectedDateTextView = findViewById(R.id.selectedDateTextView);
        diaryTextView = findViewById(R.id.diaryTextView);
        addDiaryButton = findViewById(R.id.addDiaryButton);
        selectedDate = getIntent().getStringExtra("SELECTED_DATE");

        // 선택한 날짜를 표시
        selectedDateTextView.setText(selectedDate);

        // 데이터베이스에서 일기 조회
        String diary = fetchDiary(selectedDate);

        if (diary != null) {
            diaryTextView.setText(diary);
            diaryTextView.setVisibility(View.VISIBLE);
            addDiaryButton.setVisibility(View.GONE);
        } else {
            diaryTextView.setVisibility(View.GONE);
            addDiaryButton.setVisibility(View.VISIBLE);
        }

        addDiaryButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(DateActivity.this, DiaryActivity.class);
                intent.putExtra("SELECTED_DATE", selectedDate);
                startActivity(intent);
            }
        });
    }

    private String fetchDiary(String date) {
        // 데이터베이스에서 날짜에 해당하는 일기 가져오기
        // 예: return database.getDiary(date);
        return null; // 실제 구현 필요
    }
}
