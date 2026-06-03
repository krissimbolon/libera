import sys
sys.stdout.reconfigure(encoding='utf-8')
from PyPDF2 import PdfReader

reader = PdfReader(r'laut-bercerita.pdf')
print(f'Total pages: {len(reader.pages)}')

# Check page 0 metadata
page = reader.pages[0]
print(f'Page keys: {page.keys()}')
print(f'MediaBox: {page.mediabox}')

# Try all pages for any text
found_text = False
for i in range(len(reader.pages)):
    text = reader.pages[i].extract_text()
    if text and text.strip():
        print(f'\nFound text on page {i+1}:')
        print(text[:500])
        found_text = True
        if i > 20:
            break

if not found_text:
    print('\nNo extractable text found - PDF likely contains scanned images.')
    # Check if there are annotations or forms
    print(f'\nMetadata: {reader.metadata}')
