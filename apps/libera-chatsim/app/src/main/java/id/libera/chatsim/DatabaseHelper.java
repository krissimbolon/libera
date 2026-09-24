package id.libera.chatsim;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class DatabaseHelper extends SQLiteOpenHelper {
    public static final String DB_NAME = "libera_messages.db";
    private static final int DB_VERSION = 1;
    public static final String RAKA = "AKT-RAKA";

    private final Context context;

    public DatabaseHelper(Context context) {
        super(context, DB_NAME, null, DB_VERSION);
        this.context = context.getApplicationContext();
    }

    @Override
public void onConfigure(SQLiteDatabase db) {
    super.onConfigure(db);
    db.disableWriteAheadLogging();
    db.execSQL("PRAGMA synchronous=FULL");
    db.setForeignKeyConstraintsEnabled(true);
}

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL("CREATE TABLE chats (" +
                "chat_id TEXT PRIMARY KEY," +
                "peer_id TEXT NOT NULL," +
                "peer_name TEXT NOT NULL," +
                "last_timestamp TEXT NOT NULL," +
                "last_text TEXT NOT NULL," +
                "message_count INTEGER NOT NULL)");
        db.execSQL("CREATE TABLE messages (" +
                "message_id TEXT PRIMARY KEY," +
                "chat_id TEXT NOT NULL," +
                "segment_id TEXT NOT NULL," +
                "timestamp TEXT NOT NULL," +
                "sender_id TEXT NOT NULL," +
                "recipient_id TEXT NOT NULL," +
                "sender_name TEXT NOT NULL," +
                "recipient_name TEXT NOT NULL," +
                "message_text TEXT NOT NULL," +
                "message_type TEXT NOT NULL," +
                "reply_to_message_id TEXT," +
                "FOREIGN KEY(chat_id) REFERENCES chats(chat_id) DEFERRABLE INITIALLY DEFERRED)");
        db.execSQL("CREATE INDEX idx_messages_chat_time ON messages(chat_id, timestamp)");
        db.execSQL("CREATE INDEX idx_messages_sender ON messages(sender_id)");
        db.execSQL("CREATE INDEX idx_messages_segment ON messages(segment_id)");
        db.execSQL("CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)");
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        throw new IllegalStateException("Evidence DB schema upgrade is intentionally unsupported. Re-seed DEV-SIM-001.");
    }

    public boolean isSeeded() {
        SQLiteDatabase db = getReadableDatabase();
        try (Cursor c = db.rawQuery("SELECT COUNT(*) FROM messages", null)) {
            return c.moveToFirst() && c.getInt(0) > 0;
        }
    }

    public SeedResult ensureSeeded() throws Exception {
        if (isSeeded()) {
            return currentCounts();
        }

        SQLiteDatabase db = getWritableDatabase();
        Map<String, ChatAccumulator> chats = new LinkedHashMap<>();
        int messageCount = 0;

        db.beginTransaction();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(
                context.getAssets().open("messages_seed.jsonl"), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.trim().isEmpty()) continue;
                JSONObject j = new JSONObject(line);

                String messageId = j.getString("message_id");
                String chatId = j.getString("chat_id");
                String peerId = j.getString("peer_id");
                String peerName = j.getString("peer_name");
                String timestamp = j.getString("timestamp");
                String text = j.getString("message_text");

                ChatAccumulator acc = chats.get(chatId);
                if (acc == null) {
                    acc = new ChatAccumulator(chatId, peerId, peerName);
                    chats.put(chatId, acc);
                }
                acc.count++;
                if (acc.lastTimestamp == null || timestamp.compareTo(acc.lastTimestamp) > 0) {
                    acc.lastTimestamp = timestamp;
                    acc.lastText = text;
                }

                ContentValues v = new ContentValues();
                v.put("message_id", messageId);
                v.put("chat_id", chatId);
                v.put("segment_id", j.getString("segment_id"));
                v.put("timestamp", timestamp);
                v.put("sender_id", j.getString("sender_id"));
                v.put("recipient_id", j.getString("recipient_id"));
                v.put("sender_name", j.getString("sender_name"));
                v.put("recipient_name", j.getString("recipient_name"));
                v.put("message_text", text);
                v.put("message_type", j.optString("message_type", "text"));
                v.put("reply_to_message_id", j.optString("reply_to_message_id", ""));
                db.insertOrThrow("messages", null, v);
                messageCount++;
            }

            for (ChatAccumulator acc : chats.values()) {
                ContentValues v = new ContentValues();
                v.put("chat_id", acc.chatId);
                v.put("peer_id", acc.peerId);
                v.put("peer_name", acc.peerName);
                v.put("last_timestamp", acc.lastTimestamp);
                v.put("last_text", acc.lastText == null ? "" : acc.lastText);
                v.put("message_count", acc.count);
                db.insertOrThrow("chats", null, v);
            }

            putMetadata(db, "device_id", "DEV-SIM-001");
            putMetadata(db, "simulated_owner", "Raka Pradana");
            putMetadata(db, "seed_format", "LIBERA_CHAT_SIM_V1");
            putMetadata(db, "message_count", String.valueOf(messageCount));
            putMetadata(db, "chat_count", String.valueOf(chats.size()));
            db.setTransactionSuccessful();
        } finally {
            db.endTransaction();
        }
        return new SeedResult(messageCount, chats.size());
    }

    private void putMetadata(SQLiteDatabase db, String key, String value) {
        ContentValues v = new ContentValues();
        v.put("key", key);
        v.put("value", value);
        db.insertOrThrow("metadata", null, v);
    }

    public SeedResult currentCounts() {
        SQLiteDatabase db = getReadableDatabase();
        int messages = 0;
        int chats = 0;
        try (Cursor c = db.rawQuery("SELECT COUNT(*) FROM messages", null)) {
            if (c.moveToFirst()) messages = c.getInt(0);
        }
        try (Cursor c = db.rawQuery("SELECT COUNT(*) FROM chats", null)) {
            if (c.moveToFirst()) chats = c.getInt(0);
        }
        return new SeedResult(messages, chats);
    }

    public List<ChatRow> listChats() {
        ArrayList<ChatRow> out = new ArrayList<>();
        SQLiteDatabase db = getReadableDatabase();
        try (Cursor c = db.rawQuery(
                "SELECT chat_id, peer_name, last_timestamp, last_text, message_count " +
                        "FROM chats ORDER BY last_timestamp DESC", null)) {
            while (c.moveToNext()) {
                out.add(new ChatRow(
                        c.getString(0), c.getString(1), c.getString(2),
                        c.getString(3), c.getInt(4)));
            }
        }
        return out;
    }

    public List<MessageRow> listMessages(String chatId) {
        ArrayList<MessageRow> out = new ArrayList<>();
        SQLiteDatabase db = getReadableDatabase();
        try (Cursor c = db.rawQuery(
                "SELECT message_id, segment_id, timestamp, sender_id, recipient_id, " +
                        "sender_name, recipient_name, message_text, message_type, reply_to_message_id " +
                        "FROM messages WHERE chat_id=? ORDER BY timestamp, message_id",
                new String[]{chatId})) {
            while (c.moveToNext()) {
                out.add(new MessageRow(
                        c.getString(0), c.getString(1), c.getString(2),
                        c.getString(3), c.getString(4), c.getString(5),
                        c.getString(6), c.getString(7), c.getString(8), c.getString(9)));
            }
        }
        return out;
    }

    private static class ChatAccumulator {
        final String chatId;
        final String peerId;
        final String peerName;
        String lastTimestamp;
        String lastText;
        int count;

        ChatAccumulator(String chatId, String peerId, String peerName) {
            this.chatId = chatId;
            this.peerId = peerId;
            this.peerName = peerName;
        }
    }

    public static class SeedResult {
        public final int messages;
        public final int chats;
        public SeedResult(int messages, int chats) {
            this.messages = messages;
            this.chats = chats;
        }
    }

    public static class ChatRow {
        public final String chatId;
        public final String peerName;
        public final String lastTimestamp;
        public final String lastText;
        public final int messageCount;

        public ChatRow(String chatId, String peerName, String lastTimestamp, String lastText, int messageCount) {
            this.chatId = chatId;
            this.peerName = peerName;
            this.lastTimestamp = lastTimestamp;
            this.lastText = lastText;
            this.messageCount = messageCount;
        }
    }

    public static class MessageRow {
        public final String messageId;
        public final String segmentId;
        public final String timestamp;
        public final String senderId;
        public final String recipientId;
        public final String senderName;
        public final String recipientName;
        public final String text;
        public final String type;
        public final String replyTo;

        public MessageRow(String messageId, String segmentId, String timestamp,
                          String senderId, String recipientId, String senderName,
                          String recipientName, String text, String type, String replyTo) {
            this.messageId = messageId;
            this.segmentId = segmentId;
            this.timestamp = timestamp;
            this.senderId = senderId;
            this.recipientId = recipientId;
            this.senderName = senderName;
            this.recipientName = recipientName;
            this.text = text;
            this.type = type;
            this.replyTo = replyTo;
        }
    }
}
