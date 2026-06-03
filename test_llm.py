import ollama

def test_local_llm():
    print("Menghubungi Local LLM (Gemma:2b)...")
    
    # Prompt sederhana untuk memastikan model bisa merespons
    prompt_text = "Jelaskan apa itu forensik digital dalam satu kalimat singkat."
    
    try:
        # Memanggil model secara lokal
        response = ollama.chat(model='gemma:2b', messages=[
            {
                'role': 'user',
                'content': prompt_text
            }
        ])
        
        print("\n=== RESPON DARI MODEL ===")
        print(response['message']['content'])
        print("=========================\n")
        print("Status: BERHASIL! Koneksi Python ke Local LLM aman.")
        print("Kita siap melanjutkan ke Tahap 2: Sintesis Dataset!")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nPemecahan Masalah:")
        print("1. Pastikan aplikasi Ollama sudah terbuka/berjalan di background laptopmu.")
        print("2. Pastikan kamu sudah menjalankan perintah 'ollama pull gemma:2b' di terminal.")
        print("3. Pastikan library python sudah diinstall: 'pip install ollama'")

if __name__ == "__main__":
    test_local_llm()