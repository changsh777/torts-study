import shutil, os

SRC = r'F:\mbe\KTK\images'
DST = r'F:\mbe\images'

MAPPING = {
    # prac batch (_1778480342545)
    'asset_1ese6m1xi_1778480342545.png': 'conversion_en_prac.png',
    'asset_2mdeexu0n_1778480342545.png': 'duress_ko_prac.png',
    'asset_3208mzzdl_1778480342545.png': 'duress_en_prac.png',
    'asset_4demx7d4w_1778480342545.png': 'breach_ko_prac.png',
    'asset_4itx37mde_1778480342545.png': 'assault_en_prac.png',
    'asset_4tjjtmd24_1778480342545.png': 'breach_child_ko_prac.png',
    'asset_5ub3ay3pz_1778480342545.png': 'necessity_en_prac.png',
    'asset_69cxiny97_1778480342545.png': 'battery_ko_prac.png',
    'asset_6ik0ckbp6_1778480342545.png': 'duty_special_en_prac.png',
    'asset_6m3mqj2ub_1778480342545.png': 'comp_neg_en_info.png',
    'asset_71fdmr8ki_1778480342545.png': 'causation_ko_info.png',
    'asset_79hdz8ynx_1778480342545.png': 'pl_design_ko_info.png',
    'asset_7b4cqsgoy_1778480342545.png': 'strict_liability_en_info.png',
    'asset_7wph1ai5z_1778480342545.png': 'strict_liability_ko_info.png',
    'asset_8f1xddua0_1778480342545.png': 'pl_design_en_info.png',
    'asset_8srbghfyd_1778480342545.png': 'consent_en_prac.png',
    'asset_eauvutxy2_1778480342545.png': 'breach_ko_info.png',
    'asset_eelqd8ffw_1778480342545.png': 'fi_en_prac.png',
    'asset_eq4691x89_1778480342545.png': 'assault_ko_prac.png',
    'asset_f7cj8vwsl_1778480342545.png': 'duty_premises_ko_info.png',
    'asset_ipwpqkc3p_1778480342545.png': 'informed_consent_ko_info.png',
    'asset_jm7m01ccc_1778480342545.png': 'breach_en_prac.png',
    'asset_jszghfomw_1778480342545.png': 'iied_ko_prac.png',
    'asset_n9zynmakv_1778480342545.png': 'fi_ko_prac.png',
    'asset_nggbzztx1_1778480342545.png': 'informed_consent_ko_prac.png',
    'asset_npkqlgyod_1778480342545.png': 'necessity_ko_prac.png',
    'asset_pj4e0vdl4_1778480342545.png': 'breach_child_en_prac.png',
    'asset_pwgps8r3z_1778480342545.png': 'privacy_en_prac.png',
    'asset_qbr8qmg7l_1778480342545.png': 'causation_en_info.png',
    'asset_qxgdl2s5w_1778480342545.png': 'comp_neg_ko_info.png',
    'asset_rix19c9wl_1778480342545.png': 'duty_premises_en_info.png',
    'asset_rjppz8i5c_1778480342545.png': 'consent_ko_prac.png',
    'asset_us2lasksp_1778480342545.png': 'breach_ko_prac2.png',
    'asset_xu0ja0bdq_1778480342545.png': 'informed_consent_en_info.png',
    'asset_ypgv8cvcq_1778480342545.png': 'battery_en_prac.png',
    'asset_yvhkqoy1y_1778480342545.png': 'conversion_ko_prac.png',
    # info batch (_1778476268315)
    'asset_4u4uj88iw_1778476268315.png': 'trespass_land_ko_info.png',
    'asset_785h2t6d4_1778476268315.png': 'nuisance_ko_info.png',
    'asset_f23moh94t_1778476268315.png': 'pl_warning_ko_info.png',
    'asset_lx2nfnn52_1778476268315.png': 'pl_manufacturing_ko_info.png',
    'asset_wtqfnzokz_1778476268315.png': 'trespass_land_en_info.png',
    'asset_ye1ryz554_1778476268315.png': 'pl_warning_en_info.png',
    'asset_yfmf37h3u_1778476268315.png': 'defamation_en_info.png',
    'asset_zh83pev50_1778476268315.png': 'pl_manufacturing_en_info.png',
}

copied, named, missing = 0, 0, 0

# 1) asset_* files via mapping
for src_name, dst_name in MAPPING.items():
    src_path = os.path.join(SRC, src_name)
    dst_path = os.path.join(DST, dst_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        print(f"  OK  {src_name} -> {dst_name}")
        copied += 1
    else:
        print(f"  MISS {src_name}")
        missing += 1

# 2) already-named files (non-asset_*)
for fname in os.listdir(SRC):
    if not fname.startswith('asset_') and fname.endswith('.png'):
        shutil.copy2(os.path.join(SRC, fname), os.path.join(DST, fname))
        print(f"  NAMED {fname}")
        named += 1

print(f"\n=== 완료: asset {copied}개 + named {named}개 복사, miss {missing}개 ===")

# 3) 여전히 없는 파일 체크
EXPECTED_MISSING = [
    'defamation_en_prac.png',
    'pl_manufacturing_en_prac.png', 'pl_manufacturing_ko_prac.png',
    'pl_warning_en_prac.png', 'pl_warning_ko_prac.png',
    'trespass_land_en_prac.png', 'trespass_land_ko_prac.png',
]
still_missing = [f for f in EXPECTED_MISSING if not os.path.exists(os.path.join(DST, f))]
if still_missing:
    print(f"\n⚠ 아직 없는 prac 이미지 ({len(still_missing)}개):")
    for f in still_missing:
        print(f"  - {f}")
