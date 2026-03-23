#!/usr/bin/env python3
"""
ProMem Git Hooks 安装脚本

将 .promem/hooks/ 下的所有 hook 脚本安装到 .git/hooks/
支持安装、卸载和备份恢复功能。

用法:
    python .promem/scripts/install_hooks.py [--repo-root <path>] [--uninstall]

选项:
    --repo-root: Git 仓库根目录（默认当前目录）
    --uninstall: 卸载 ProMem hooks（恢复备份）
"""

import argparse
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional


BACKUP_SUFFIX = ".promem-backup"
DEVMEM_MARKER = "# ProMem"


def get_git_root(repo_root: Path) -> Optional[Path]:
    """获取 Git 仓库根目录"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError:
        return None


def is_promem_hook(hook_path: Path) -> bool:
    """检查一个 hook 文件是否是 ProMem 安装的"""
    if not hook_path.exists():
        return False
    try:
        content = hook_path.read_text(encoding="utf-8")
        return DEVMEM_MARKER in content
    except Exception:
        return False


def set_executable(path: Path) -> None:
    """设置文件为可执行"""
    current_mode = path.stat().st_mode
    path.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def install_hook(source: Path, dest: Path) -> dict:
    """
    安装单个 hook 脚本
    
    Returns:
        dict: 安装结果信息
    """
    result = {
        "name": source.name,
        "action": None,
        "backup": None,
        "success": False,
        "error": None,
    }
    
    try:
        # 如果目标已存在
        if dest.exists():
            # 检查是否是我们自己安装的
            if is_promem_hook(dest):
                # 是我们的 hook，直接覆盖更新
                result["action"] = "updated"
            else:
                # 是用户原有的 hook，需要备份
                backup_path = dest.with_suffix(dest.suffix + BACKUP_SUFFIX)
                shutil.copy2(dest, backup_path)
                result["backup"] = str(backup_path.name)
                result["action"] = "installed (backup created)"
        else:
            result["action"] = "installed"
        
        # 复制 hook 文件
        shutil.copy2(source, dest)
        
        # 设置可执行权限
        set_executable(dest)
        
        result["success"] = True
        
    except Exception as e:
        result["error"] = str(e)
        result["action"] = "failed"
    
    return result


def uninstall_hook(hook_name: str, git_hooks_dir: Path) -> dict:
    """
    卸载单个 hook 脚本
    
    Returns:
        dict: 卸载结果信息
    """
    result = {
        "name": hook_name,
        "action": None,
        "success": False,
        "error": None,
    }
    
    hook_path = git_hooks_dir / hook_name
    backup_path = git_hooks_dir / f"{hook_name}{BACKUP_SUFFIX}"
    
    try:
        if not hook_path.exists():
            result["action"] = "not found"
            result["success"] = True
            return result
        
        # 检查是否是 ProMem 安装的
        if not is_promem_hook(hook_path):
            result["action"] = "skipped (not ProMem hook)"
            result["success"] = True
            return result
        
        # 删除 ProMem hook
        hook_path.unlink()
        
        # 检查是否有备份需要恢复
        if backup_path.exists():
            shutil.move(backup_path, hook_path)
            result["action"] = "removed (backup restored)"
        else:
            result["action"] = "removed"
        
        result["success"] = True
        
    except Exception as e:
        result["error"] = str(e)
        result["action"] = "failed"
    
    return result


def find_promem_dir(start_path: Path) -> Optional[Path]:
    """从给定路径向上查找 .promem 目录"""
    current = start_path.resolve()
    while current != current.parent:
        promem_dir = current / ".promem"
        if promem_dir.exists() and promem_dir.is_dir():
            return promem_dir
        current = current.parent
    return None


def install_hooks(repo_root: Path) -> int:
    """安装所有 ProMem hooks"""
    print(f"[ProMem] Installing hooks for repository: {repo_root}")
    print()
    
    # 验证 Git 仓库
    git_root = get_git_root(repo_root)
    if not git_root:
        print("Error: Not a Git repository", file=sys.stderr)
        return 1
    
    git_hooks_dir = git_root / ".git" / "hooks"
    
    # 从 repo_root 开始查找 .promem 目录
    promem_dir = find_promem_dir(repo_root)
    if not promem_dir:
        # 回退到 repo_root 下查找
        promem_dir = repo_root / ".promem"
    promem_hooks_dir = promem_dir / "hooks"
    
    # 检查 promem hooks 目录
    if not promem_hooks_dir.exists():
        print(f"Error: ProMem hooks directory not found: {promem_hooks_dir}", file=sys.stderr)
        return 1
    
    # 确保 .git/hooks 目录存在
    git_hooks_dir.mkdir(parents=True, exist_ok=True)
    
    # 获取所有 hook 文件（排除隐藏文件如 .gitkeep）
    hooks = [f for f in promem_hooks_dir.iterdir() if f.is_file() and not f.name.startswith(".")]
    
    if not hooks:
        print("No hooks found in .promem/hooks/")
        return 0
    
    print(f"Found {len(hooks)} hook(s) to install:")
    print()
    
    success_count = 0
    failed_count = 0
    
    for hook_source in sorted(hooks):
        hook_dest = git_hooks_dir / hook_source.name
        result = install_hook(hook_source, hook_dest)
        
        if result["success"]:
            success_count += 1
            status = "✓"
            detail = result["action"]
            if result["backup"]:
                detail += f" - original saved as {result['backup']}"
        else:
            failed_count += 1
            status = "✗"
            detail = f"failed: {result['error']}"
        
        print(f"  {status} {result['name']}: {detail}")
    
    print()
    print(f"Installation complete: {success_count} succeeded, {failed_count} failed")
    
    if success_count > 0:
        print()
        print("Hooks are now active. They will run automatically on Git operations.")
    
    return 0 if failed_count == 0 else 1


def uninstall_hooks(repo_root: Path) -> int:
    """卸载所有 ProMem hooks"""
    print(f"[ProMem] Uninstalling hooks for repository: {repo_root}")
    print()
    
    # 验证 Git 仓库
    git_root = get_git_root(repo_root)
    if not git_root:
        print("Error: Not a Git repository", file=sys.stderr)
        return 1
    
    git_hooks_dir = git_root / ".git" / "hooks"
    
    # 从 repo_root 开始查找 .promem 目录
    promem_dir = find_promem_dir(repo_root)
    if promem_dir:
        promem_hooks_dir = promem_dir / "hooks"
    else:
        promem_hooks_dir = repo_root / ".promem" / "hooks"
    
    if not git_hooks_dir.exists():
        print("No .git/hooks directory found. Nothing to uninstall.")
        return 0
    
    # 获取 promem hooks 的名称列表
    if promem_hooks_dir.exists():
        hook_names = [f.name for f in promem_hooks_dir.iterdir() if f.is_file() and not f.name.startswith(".")]
    else:
        # 如果 promem hooks 目录不存在，尝试从 .git/hooks 中查找 ProMem hooks
        hook_names = [f.name for f in git_hooks_dir.iterdir() if f.is_file() and is_promem_hook(f)]
    
    if not hook_names:
        print("No ProMem hooks found to uninstall.")
        return 0
    
    print(f"Found {len(hook_names)} hook(s) to uninstall:")
    print()
    
    success_count = 0
    failed_count = 0
    
    for hook_name in sorted(hook_names):
        result = uninstall_hook(hook_name, git_hooks_dir)
        
        if result["success"]:
            success_count += 1
            status = "✓"
            detail = result["action"]
        else:
            failed_count += 1
            status = "✗"
            detail = f"failed: {result['error']}"
        
        print(f"  {status} {result['name']}: {detail}")
    
    print()
    print(f"Uninstallation complete: {success_count} succeeded, {failed_count} failed")
    
    return 0 if failed_count == 0 else 1


def main():
    parser = argparse.ArgumentParser(
        description="安装或卸载 ProMem Git Hooks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 安装 hooks（在仓库根目录下运行）
  python .promem/scripts/install_hooks.py

  # 指定仓库路径安装
  python .promem/scripts/install_hooks.py --repo-root /path/to/repo

  # 卸载 hooks
  python .promem/scripts/install_hooks.py --uninstall

功能说明:
  安装模式:
    - 将 .promem/hooks/ 下的所有脚本复制到 .git/hooks/
    - 自动设置可执行权限 (chmod +x)
    - 如果目标已存在非 ProMem hook，会先备份为 {name}.promem-backup
    - 如果目标是 ProMem hook，直接覆盖更新

  卸载模式:
    - 删除 .git/hooks/ 中由 ProMem 安装的 hooks
    - 如果存在备份文件，自动恢复
""",
    )
    
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Git 仓库根目录（默认: 当前目录）",
    )
    
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="卸载 ProMem hooks 并恢复备份",
    )
    
    args = parser.parse_args()
    
    # 验证路径
    if not args.repo_root.exists():
        print(f"Error: Path does not exist: {args.repo_root}", file=sys.stderr)
        sys.exit(1)
    
    # 执行安装或卸载
    if args.uninstall:
        exit_code = uninstall_hooks(args.repo_root)
    else:
        exit_code = install_hooks(args.repo_root)
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
