package id.libera.chatsim;

import android.app.Activity;
import android.app.AlertDialog;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;

import java.util.List;

public class ChatActivity extends Activity {
    private DatabaseHelper db;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        String chatId = getIntent().getStringExtra("chat_id");
        String peerName = getIntent().getStringExtra("peer_name");
        db = new DatabaseHelper(this);

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(Color.rgb(236, 229, 221));

        LinearLayout header = new LinearLayout(this);
        header.setOrientation(LinearLayout.HORIZONTAL);
        header.setGravity(Gravity.CENTER_VERTICAL);
        header.setPadding(dp(8), dp(6), dp(12), dp(6));
        header.setBackgroundColor(Color.rgb(7, 94, 84));

        TextView back = new TextView(this);
        back.setText("‹");
        back.setTextSize(38);
        back.setTextColor(Color.WHITE);
        back.setGravity(Gravity.CENTER);
        back.setOnClickListener(v -> finish());
        header.addView(back, new LinearLayout.LayoutParams(dp(52), dp(52)));

        LinearLayout names = new LinearLayout(this);
        names.setOrientation(LinearLayout.VERTICAL);
        TextView name = new TextView(this);
        name.setText(peerName == null ? chatId : peerName);
        name.setTextColor(Color.WHITE);
        name.setTextSize(19);
        name.setTypeface(null, android.graphics.Typeface.BOLD);
        names.addView(name);
        TextView hint = new TextView(this);
        hint.setText("DEV-SIM-001 • tahan pesan untuk metadata pesan");
        hint.setTextColor(Color.rgb(210, 235, 232));
        hint.setTextSize(11);
        names.addView(hint);
        header.addView(names, new LinearLayout.LayoutParams(0, dp(56), 1f));

        root.addView(header);

        ListView list = new ListView(this);
        list.setDivider(null);
        list.setDividerHeight(0);
        list.setTranscriptMode(ListView.TRANSCRIPT_MODE_NORMAL);
        root.addView(list, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f));

        setContentView(root);

        List<DatabaseHelper.MessageRow> messages = db.listMessages(chatId);
        MessageAdapter adapter = new MessageAdapter(messages);
        list.setAdapter(adapter);
        if (!messages.isEmpty()) {
            list.setSelection(messages.size() - 1);
        }

        list.setOnItemLongClickListener((parent, view, position, id) -> {
            DatabaseHelper.MessageRow m = adapter.getItem(position);
            new AlertDialog.Builder(this)
                    .setTitle("Metadata pesan sumber")
                    .setMessage(
                            "message_id: " + m.messageId + "\n" +
                            "segment_id: " + m.segmentId + "\n" +
                            "timestamp: " + m.timestamp + "\n" +
                            "sender: " + m.senderId + "\n" +
                            "recipient: " + m.recipientId +
                            (m.replyTo.isEmpty() ? "" : "\nreply_to: " + m.replyTo))
                    .setPositiveButton("OK", null)
                    .show();
            return true;
        });
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }

    private class MessageAdapter extends BaseAdapter {
        private final List<DatabaseHelper.MessageRow> rows;

        MessageAdapter(List<DatabaseHelper.MessageRow> rows) {
            this.rows = rows;
        }

        public int getCount() { return rows.size(); }
        public DatabaseHelper.MessageRow getItem(int position) { return rows.get(position); }
        public long getItemId(int position) { return position; }

        public View getView(int position, View convertView, ViewGroup parent) {
            DatabaseHelper.MessageRow m = getItem(position);
            boolean mine = DatabaseHelper.RAKA.equals(m.senderId);

            LinearLayout outer = new LinearLayout(ChatActivity.this);
            outer.setGravity(mine ? Gravity.RIGHT : Gravity.LEFT);
            outer.setPadding(dp(10), dp(3), dp(10), dp(3));

            LinearLayout bubble = new LinearLayout(ChatActivity.this);
            bubble.setOrientation(LinearLayout.VERTICAL);
            bubble.setPadding(dp(11), dp(7), dp(11), dp(6));

            GradientDrawable bg = new GradientDrawable();
            bg.setCornerRadius(dp(10));
            bg.setColor(mine ? Color.rgb(220, 248, 198) : Color.WHITE);
            bubble.setBackground(bg);

            TextView text = new TextView(ChatActivity.this);
            text.setText(m.text);
            text.setTextSize(15);
            text.setTextColor(Color.rgb(30, 30, 30));
            bubble.addView(text, new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.WRAP_CONTENT,
                    ViewGroup.LayoutParams.WRAP_CONTENT));

            TextView meta = new TextView(ChatActivity.this);
            String hhmm = m.timestamp.length() >= 16 ? m.timestamp.substring(11, 16) : m.timestamp;
            meta.setText(hhmm);
            meta.setTextSize(10);
            meta.setTextColor(Color.GRAY);
            meta.setGravity(Gravity.RIGHT);
            bubble.addView(meta, new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, dp(17)));

            LinearLayout.LayoutParams bubbleLp = new LinearLayout.LayoutParams(
                    0, ViewGroup.LayoutParams.WRAP_CONTENT);
            bubbleLp.weight = 0.82f;
            outer.addView(bubble, bubbleLp);

            View spacer = new View(ChatActivity.this);
            LinearLayout.LayoutParams spacerLp = new LinearLayout.LayoutParams(
                    0, 1);
            spacerLp.weight = 0.18f;
            if (mine) {
                outer.addView(spacer, 0, spacerLp);
            } else {
                outer.addView(spacer, spacerLp);
            }
            return outer;
        }
    }
}
