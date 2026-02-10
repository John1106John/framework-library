#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Framework 格式驗證工具
用於驗證架構是否符合標準格式規範
"""

import sys
import io
import json
from pathlib import Path
import yaml

# Windows 編碼處理
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 標準格式規範
REQUIRED_SPEC_FIELDS = {
    "metadata": ["name", "version", "description", "author", "created_at", "updated_at"],
    "system_overview": ["name", "purpose", "tech_stack"],
    "architecture": ["design_principle", "components"],
    "directory_structure": ["description", "layout"],
    "integration_guide": []
}

REQUIRED_FILES = [
    "{framework_name}_spec.yaml",
    "AI_INTEGRATION_PROMPT.md",
    "README.md"
]

def load_yaml(file_path):
    """載入 YAML 檔案"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        return None, str(e)

def validate_spec_yaml(spec_path):
    """驗證 spec.yaml 格式"""
    errors = []
    warnings = []

    # 讀取 spec 文件
    spec_data = load_yaml(spec_path)
    if isinstance(spec_data, tuple):
        errors.append(f"無法載入 spec.yaml: {spec_data[1]}")
        return errors, warnings

    # 檢查必須的頂層字段
    for top_field, sub_fields in REQUIRED_SPEC_FIELDS.items():
        if top_field not in spec_data:
            errors.append(f"缺少必須字段: {top_field}")
        elif sub_fields:
            # 檢查子字段
            for sub_field in sub_fields:
                if sub_field not in spec_data[top_field]:
                    errors.append(f"缺少必須子字段: {top_field}.{sub_field}")

    # 檢查 metadata 的格式
    if "metadata" in spec_data:
        metadata = spec_data["metadata"]
        if "version" in metadata:
            # 檢查版本號格式（應為 x.y.z）
            version = metadata["version"]
            if not isinstance(version, str) or len(version.split('.')) != 3:
                warnings.append(f"版本號格式建議為 x.y.z，當前為: {version}")

    # 檢查 tech_stack 是否包含必要資訊
    if "system_overview" in spec_data and "tech_stack" in spec_data["system_overview"]:
        tech_stack = spec_data["system_overview"]["tech_stack"]
        if "language" not in tech_stack:
            warnings.append("system_overview.tech_stack 建議包含 language 字段")
        if "dependencies" not in tech_stack:
            warnings.append("system_overview.tech_stack 建議包含 dependencies 字段")

    return errors, warnings

def validate_framework_files(framework_dir):
    """驗證必須檔案是否存在"""
    errors = []
    warnings = []

    framework_path = Path(framework_dir)
    if not framework_path.exists():
        errors.append(f"架構目錄不存在: {framework_dir}")
        return errors, warnings

    # 找出 spec.yaml 文件（以 _spec.yaml 結尾）
    spec_files = list(framework_path.glob("*_spec.yaml"))
    if not spec_files:
        errors.append("未找到 spec.yaml 檔案（檔名應為 *_spec.yaml）")
        return errors, warnings

    spec_file = spec_files[0]
    framework_name = spec_file.stem.replace("_spec", "")

    # 檢查必須檔案
    required_files = [
        f"{framework_name}_spec.yaml",
        "AI_INTEGRATION_PROMPT.md",
        "README.md"
    ]

    for required_file in required_files:
        file_path = framework_path / required_file
        if not file_path.exists():
            errors.append(f"缺少必須檔案: {required_file}")

    # 檢查可選但建議的檔案/目錄
    if not (framework_path / "templates").exists():
        warnings.append("建議提供 templates/ 目錄（如適用）")

    if not (framework_path / "examples").exists():
        warnings.append("建議提供 examples/ 目錄（如適用）")

    return errors, warnings

def validate_frameworks_json(frameworks_json_path, frameworks_dir):
    """驗證 FRAMEWORKS.json 與實際架構的一致性"""
    errors = []
    warnings = []

    # 讀取 FRAMEWORKS.json
    try:
        with open(frameworks_json_path, 'r', encoding='utf-8') as f:
            frameworks_data = json.load(f)
    except Exception as e:
        errors.append(f"無法載入 FRAMEWORKS.json: {e}")
        return errors, warnings

    # 檢查必須字段
    if "frameworks" not in frameworks_data:
        errors.append("FRAMEWORKS.json 缺少 frameworks 陣列")
        return errors, warnings

    # 驗證每個架構
    frameworks = frameworks_data["frameworks"]
    frameworks_path = Path(frameworks_dir)

    for framework in frameworks:
        # 檢查必須字段
        required_fields = ["id", "name", "version", "description", "path", "files"]
        for field in required_fields:
            if field not in framework:
                errors.append(f"架構 {framework.get('id', 'unknown')} 缺少必須字段: {field}")

        # 檢查路徑是否存在
        if "path" in framework:
            framework_path = frameworks_path.parent / framework["path"]
            if not framework_path.exists():
                errors.append(f"架構路徑不存在: {framework['path']}")

        # 檢查檔案是否存在
        if "files" in framework and "path" in framework:
            files = framework["files"]
            framework_path = frameworks_path.parent / framework["path"]

            for file_type, file_name in files.items():
                file_path = framework_path / file_name
                if not file_path.exists():
                    errors.append(f"架構 {framework['id']} 的檔案不存在: {file_name}")

    return errors, warnings

def validate_framework(framework_dir):
    """驗證單個架構"""
    print(f"\n{'='*60}")
    print(f"驗證架構: {framework_dir}")
    print(f"{'='*60}\n")

    all_errors = []
    all_warnings = []

    # 驗證檔案結構
    print("📁 驗證檔案結構...")
    errors, warnings = validate_framework_files(framework_dir)
    all_errors.extend(errors)
    all_warnings.extend(warnings)

    if errors:
        for error in errors:
            print(f"  ❌ {error}")
    else:
        print("  ✅ 檔案結構完整")

    for warning in warnings:
        print(f"  ⚠️  {warning}")

    # 驗證 spec.yaml 格式
    print("\n📋 驗證 spec.yaml 格式...")
    framework_path = Path(framework_dir)
    spec_files = list(framework_path.glob("*_spec.yaml"))

    if spec_files:
        errors, warnings = validate_spec_yaml(spec_files[0])
        all_errors.extend(errors)
        all_warnings.extend(warnings)

        if errors:
            for error in errors:
                print(f"  ❌ {error}")
        else:
            print("  ✅ spec.yaml 格式正確")

        for warning in warnings:
            print(f"  ⚠️  {warning}")

    # 總結
    print(f"\n{'='*60}")
    if all_errors:
        print(f"❌ 驗證失敗！發現 {len(all_errors)} 個錯誤")
        return False
    elif all_warnings:
        print(f"⚠️  驗證通過，但有 {len(all_warnings)} 個警告")
        return True
    else:
        print("✅ 驗證完全通過！")
        return True

def validate_all_frameworks(repo_root):
    """驗證所有架構"""
    repo_path = Path(repo_root)
    frameworks_dir = repo_path / "frameworks"

    if not frameworks_dir.exists():
        print(f"❌ 找不到 frameworks 目錄: {frameworks_dir}")
        return False

    # 驗證 FRAMEWORKS.json
    print(f"\n{'='*60}")
    print("驗證 FRAMEWORKS.json")
    print(f"{'='*60}\n")

    frameworks_json = repo_path / "FRAMEWORKS.json"
    if frameworks_json.exists():
        errors, warnings = validate_frameworks_json(frameworks_json, frameworks_dir)

        if errors:
            for error in errors:
                print(f"  ❌ {error}")
        else:
            print("  ✅ FRAMEWORKS.json 格式正確")

        for warning in warnings:
            print(f"  ⚠️  {warning}")
    else:
        print("  ❌ 找不到 FRAMEWORKS.json")
        return False

    # 驗證每個架構
    all_passed = True
    framework_dirs = [d for d in frameworks_dir.iterdir() if d.is_dir()]

    for framework_dir in framework_dirs:
        passed = validate_framework(framework_dir)
        all_passed = all_passed and passed

    # 最終總結
    print(f"\n{'='*60}")
    print("最終報告")
    print(f"{'='*60}\n")

    if all_passed:
        print("✅ 所有架構驗證通過！")
        return True
    else:
        print("❌ 部分架構驗證失敗，請修正上述錯誤")
        return False

def main():
    """主程式"""
    if len(sys.argv) > 1:
        # 驗證指定的架構
        framework_dir = sys.argv[1]
        passed = validate_framework(framework_dir)
        sys.exit(0 if passed else 1)
    else:
        # 驗證所有架構
        repo_root = Path(__file__).parent
        passed = validate_all_frameworks(repo_root)
        sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()
