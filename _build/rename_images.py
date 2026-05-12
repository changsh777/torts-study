"""
rename_images.py — Jenspark 이미지 파일명 의미화
asset_4346n4goq_1778393192945.png  →  battery_ko_info.png
image_classification.json 자동 업데이트
"""
import sys, json, os, shutil
sys.stdout.reconfigure(encoding='utf-8')

IMG_DIR  = r'F:\mbe\images'
CLS_JSON = r'F:\mbe\_extracted\image_classification.json'

data = json.load(open(CLS_JSON, 'r', encoding='utf-8'))
mapping = data['topic_mapping']

renamed, skipped, missing = [], [], []

for topic, types in mapping.items():
    for img_type, old_name in list(types.items()):
        new_name = f'{topic}_{img_type}.png'

        old_path = os.path.join(IMG_DIR, old_name)
        new_path = os.path.join(IMG_DIR, new_name)

        if old_name == new_name:
            skipped.append(new_name)
            continue

        if not os.path.exists(old_path):
            missing.append(old_name)
            print(f'  ⚠ 없음: {old_name}')
            continue

        if os.path.exists(new_path):
            # 이미 같은 이름 존재 → 덮어쓰기 (같은 파일일 것)
            os.remove(new_path)

        os.rename(old_path, new_path)
        data['topic_mapping'][topic][img_type] = new_name
        renamed.append(f'{old_name:45s} → {new_name}')
        print(f'  ✓ {old_name} → {new_name}')

# image_classification.json 업데이트
data['_comment'] = 'Claude vision 자동 분류 결과 — 파일명 의미화 완료'
json.dump(data, open(CLS_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print(f'\n✅ 변환 완료: {len(renamed)}개 / 스킵: {len(skipped)}개 / 없음: {len(missing)}개')
print(f'→ {CLS_JSON} 업데이트됨')
print('\n다음 단계: python F:\\mbe\\_build\\builder_v8.py  (HTML 재빌드)')
