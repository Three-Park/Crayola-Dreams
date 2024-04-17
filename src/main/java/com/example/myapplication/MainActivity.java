package com.example.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.widget.CalendarView;

import java.text.SimpleDateFormat;
import java.util.Locale;

public class MainActivity extends Activity {
    private CalendarView calendarView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        calendarView = findViewById(R.id.calendarView);
        calendarView.setOnDateChangeListener(new CalendarView.OnDateChangeListener() {
            @Override
            public void onSelectedDayChange(CalendarView view, int year, int month, int dayOfMonth) {
                // 날짜를 String 형식으로 변환
                String selectedDate = formatDate(year, month, dayOfMonth);

                // DateActivity로 이동
                Intent intent = new Intent(MainActivity.this, DateActivity.class);
                intent.putExtra("SELECTED_DATE", selectedDate);
                startActivity(intent);
            }
        });
    }

    private String formatDate(int year, int month, int dayOfMonth) {
        // CalendarView에서 month 값은 0부터 시작하므로 +1을 해줍니다.
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.getDefault());
        return sdf.format(new java.util.Date(year - 1900, month, dayOfMonth));
    }
}
