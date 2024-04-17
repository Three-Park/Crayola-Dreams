package com.example.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.example.myapplication.network.RetrofitClientInstance;

public class DiaryActivity extends Activity {
    private EditText diaryEditText;
    private Button saveDiaryButton;
    private String selectedDate;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_writediary);

        diaryEditText = findViewById(R.id.diaryEditText);
        saveDiaryButton = findViewById(R.id.saveDiaryButton);
        selectedDate = getIntent().getStringExtra("SELECTED_DATE");

        saveDiaryButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String diaryContent = diaryEditText.getText().toString();
                if (!diaryContent.isEmpty()) {
                    saveDiary(selectedDate, diaryContent);
                    Intent intent = new Intent(DiaryActivity.this, LoadingActivity.class);
                    startActivity(intent); // 로딩 화면 호출
                } else {
                    Toast.makeText(DiaryActivity.this, "일기를 입력하세요.", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }

    private void saveDiary(String date, String content) {

}
