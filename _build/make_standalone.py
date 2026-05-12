"""
make_standalone.py — 이미지를 HTML 안에 base64 embed
images/ 폴더 없이 어디서나 열 수 있는 단독 HTML 생성

입력: F:\mbe\Torts_단권화_v8.html
출력: F:\mbe\Torts_단권화_v8_standalone.html

PNG → WebP(quality=85) 변환으로 88MB → 약 15MB로 압축

사용법:
  python F:\mbe\_build\make_standalone.py
"""
import sys, os, re, base64, io
sys.stdout.reconfigure(encoding='utf-8')

try:
    from PIL import Image
except ImportError:
    print('Pillow 없음 → pip install Pillow')
    sys.exit(1)

SRC  = r'F:\mbe\Torts_단권화_v8.html'
DST  = r'F:\mbe\Torts_단권화_v8_standalone.html'
IMG_DIR = r'F:\mbe\images'
WEBP_QUALITY = 85

def png_to_webp_b64(png_path: str) -> str:
    """PNG 파일 → WebP base64 data URI"""
    img = Image.open(png_path)
    buf = io.BytesIO()
    img.save(buf, format='WEBP', quality=WEBP_QUALITY)
    b64 = base64.b64encode(buf.getvalue()).decode('ascii')
    return f'data:image/webp;base64,{b64}'

def main():
    print(f'읽는 중: {SRC}')
    with open(SRC, 'r', encoding='utf-8') as f:
        html = f.read()

    # src="images/xxx.png" 패턴 전체 수집
    pattern = re.compile(r'src="images/([^"]+\.png)"')
    matches = pattern.findall(html)
    unique = sorted(set(matches))
    print(f'이미지 참조 {len(matches)}개 ({len(unique)}종 고유)')

    # 캐시: 같은 파일 여러 번 등장해도 한 번만 변환
    cache = {}
    missing = []

    for i, fn in enumerate(unique, 1):
        path = os.path.join(IMG_DIR, fn)
        if not os.path.exists(path):
            missing.append(fn)
            print(f'  [{i:3d}/{len(unique)}] ⚠ 없음: {fn}')
            continue
        orig_kb = os.path.getsize(path) // 1024
        data_uri = png_to_webp_b64(path)
        webp_kb  = len(data_uri) * 3 // 4 // 1024  # base64 → bytes 역산
        cache[fn] = data_uri
        print(f'  [{i:3d}/{len(unique)}] {fn[:45]:45s}  {orig_kb:4d}KB → {webp_kb:3d}KB')

    # HTML 치환
    def replacer(m):
        fn = m.group(1)
        if fn in cache:
            return f'src="{cache[fn]}"'
        return m.group(0)  # 없는 파일은 원본 유지

    html_out = pattern.sub(replacer, html)

    with open(DST, 'w', encoding='utf-8') as f:
        f.write(html_out)

    kb = os.path.getsize(DST) // 1024
    print(f'\n✅ standalone 완료: {DST}')
    print(f'   파일 크기: {kb:,} KB  ({kb/1024:.1f} MB)')
    if missing:
        print(f'   ⚠ 없는 이미지 {len(missing)}개 (원본 경로 유지): {missing}')

if __name__ == '__main__':
    main()
