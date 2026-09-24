package id.libera.chatsim;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class MainActivity extends Activity {
    private DatabaseHelper db;
    private ChatAdapter adapter;
    private TextView subtitle;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        db = new DatabaseHelper(this);

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(Color.rgb(245, 247, 248));

        TextView title = new TextView(this);
        title.setText("LIBERA ChatSim");
        title.setTextSize(22);
        title.setTextColor(Color.WHITE);
        title.setGravity(Gravity.CENTER_VERTICAL);
        title.setPadding(dp(18), dp(12), dp(18), dp(2));
        title.setBackgroundColor(Color.rgb(7, 94, 84));
        root.addView(title, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, dp(48)));

        subtitle = new TextView(this);
        subtitle.setText("DEV-001 • simulated Raka handset");
        subtitle.setTextSize(12);
        subtitle.setTextColor(Color.rgb(225, 245, 242));
        subtitle.setPadding(dp(18), 0, dp(18), dp(10));
        subtitle.setBackgroundColor(Color.rgb(7, 94, 84));
        root.addView(subtitle, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, dp(32)));

        EditText search = new EditText(this);
        search.setHint("Cari chat...");
        search.setSingleLine(true);
        search.setPadding(dp(14), dp(8), dp(14), dp(8));
        LinearLayout.LayoutParams searchLp = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, dp(52));
        searchLp.setMargins(dp(12), dp(10), dp(12), dp(6));
        root.addView(search, searchLp);

        ListView list = new ListView(this);
        list.setDividerHeight(1);
        root.addView(list, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f));

        setContentView(root);

        try {
            DatabaseHelper.SeedResult seeded = db.ensureSeeded();
            subtitle.setText("DEV-001 • Raka Pradana • " + seeded.chats +
                    " chats • " + seeded.messages + " messages");
            adapter = new ChatAdapter(db.listChats());
            list.setAdapter(adapter);
        } catch (Exception e) {
            subtitle.setText("DEV-001 • seed unavailable");
            Toast.makeText(this,
                    "Seed gagal dimuat. Jalankan tools/build_demo_seed.py sebelum build.\n" + e.getMessage(),
                    Toast.LENGTH_LONG).show();
            adapter = new ChatAdapter(new ArrayList<>());
            list.setAdapter(adapter);
        }

        list.setOnItemClickListener((parent, view, position, id) -> {
            DatabaseHelper.ChatRow row = adapter.getItem(position);
            Intent intent = new Intent(this, ChatActivity.class);
            intent.putExtra("chat_id", row.chatId);
            intent.putExtra("peer_name", row.peerName);
            startActivity(intent);
        });

        search.addTextChangedListener(new TextWatcher() {
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {}
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                adapter.filter(s.toString());
            }
            public void afterTextChanged(Editable s) {}
        });
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }

    private class ChatAdapter extends BaseAdapter {
        private final List<DatabaseHelper.ChatRow> all;
        private final List<DatabaseHelper.ChatRow> shown;

        ChatAdapter(List<DatabaseHelper.ChatRow> rows) {
            all = new ArrayList<>(rows);
            shown = new ArrayList<>(rows);
        }

        void filter(String q) {
            shown.clear();
            String needle = q.trim().toLowerCase(Locale.ROOT);
            for (DatabaseHelper.ChatRow r : all) {
                if (needle.isEmpty() || r.peerName.toLowerCase(Locale.ROOT).contains(needle)) {
                    shown.add(r);
                }
            }
            notifyDataSetChanged();
        }

        public int getCount() { return shown.size(); }
        public DatabaseHelper.ChatRow getItem(int position) { return shown.get(position); }
        public long getItemId(int position) { return position; }

        public View getView(int position, View convertView, ViewGroup parent) {
            DatabaseHelper.ChatRow row = getItem(position);

            LinearLayout wrap = new LinearLayout(MainActivity.this);
            wrap.setOrientation(LinearLayout.VERTICAL);
            wrap.setPadding(dp(18), dp(10), dp(18), dp(10));
            wrap.setBackgroundColor(Color.WHITE);

            LinearLayout top = new LinearLayout(MainActivity.this);
            top.setOrientation(LinearLayout.HORIZONTAL);

            TextView name = new TextView(MainActivity.this);
            name.setText(row.peerName);
            name.setTextSize(17);
            name.setTextColor(Color.rgb(25, 35, 40));
            name.setTypeface(null, android.graphics.Typeface.BOLD);
            top.addView(name, new LinearLayout.LayoutParams(0, dp(26), 1f));

            TextView time = new TextView(MainActivity.this);
            String ts = row.lastTimestamp;
            String shortTs = ts.length() >= 16 ? ts.substring(5, 10) + " " + ts.substring(11, 16) : ts;
            time.setText(shortTs);
            time.setTextSize(11);
            time.setTextColor(Color.GRAY);
            time.setGravity(Gravity.RIGHT);
            top.addView(time, new LinearLayout.LayoutParams(dp(92), dp(26)));

            wrap.addView(top);

            TextView last = new TextView(MainActivity.this);
            String preview = row.lastText.replace("\n", " ");
            if (preview.length() > 70) preview = preview.substring(0, 67) + "...";
            last.setText(preview + "   ·   " + row.messageCount + " pesan");
            last.setTextSize(13);
            last.setTextColor(Color.DKGRAY);
            last.setMaxLines(2);
            wrap.addView(last);

            return wrap;
        }
    }
}
