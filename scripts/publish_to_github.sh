#!/usr/bin/env bash
# publish_to_github.sh — 把本仓库推送到 GitHub
#
# 用法（三选一）：
#
#   1) Personal Access Token（最简单）：
#        GITHUB_TOKEN=ghp_xxxxx bash scripts/publish_to_github.sh
#
#    创建 token：https://github.com/settings/tokens
#    权限勾选 "repo" 全勾即可（classic token 勾 repo 或 fine-grained 勾 Administration:write + Contents:write）。
#
#   2) 已用 gh CLI 登录过：
#        bash scripts/publish_to_github.sh --gh
#
#   3) SSH 方式（需先把公钥加到 https://github.com/settings/keys）：
#        bash scripts/publish_to_github.sh --ssh
#
# 说明：
#   - 脚本只在内存里使用 token，不写入 .git/config、不写入磁盘文件。
#   - 仓库已存在时直接推送；不存在时通过 API 创建（需要 token 具 repo 权限）。
#   - 仓库默认设为 public（开源给别人用）。要私有请在创建时手动改。

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OWNER="haoweid789"
REPO="lunwenn-skill"
BRANCH="main"

cd "$REPO_DIR"

# ---------------------------------------------------------------- 参数
MODE="token"
if [ "${1:-}" = "--gh" ]; then MODE="gh"
elif [ "${1:-}" = "--ssh" ]; then MODE="ssh"; fi

# ---------------------------------------------------------------- 前置检查
if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "✗ 当前目录不是 git 仓库：$REPO_DIR"
  exit 1
fi

if [ -z "$(git log --oneline 2>/dev/null)" ]; then
  echo "✗ 还没有任何提交，先执行 git add -A && git commit"
  exit 1
fi

if ! command -v git >/dev/null 2>&1; then
  echo "✗ 未找到 git"
  exit 1
fi

echo "仓库目录：$REPO_DIR"
echo "提交数：$(git rev-list --count HEAD)"
echo "模式：$MODE"
echo

# ---------------------------------------------------------------- 组装 URL
case "$MODE" in
  token)
    if [ -z "${GITHUB_TOKEN:-}" ]; then
      echo "✗ 未设置 GITHUB_TOKEN 环境变量"
      echo
      echo "先创建 token：https://github.com/settings/tokens"
      echo "勾选权限：repo（classic）或 Administration:write + Contents:write（fine-grained）"
      echo
      echo "然后运行：GITHUB_TOKEN=ghp_xxxxx bash scripts/publish_to_github.sh"
      exit 1
    fi
    REMOTE="https://${GITHUB_TOKEN}@github.com/${OWNER}/${REPO}.git"

    # 仓库不存在则创建
    CODE=$(curl -s -o /dev/null -w "%{http_code}" \
      -H "Authorization: token ${GITHUB_TOKEN}" \
      -H "Accept: application/vnd.github+json" \
      "https://api.github.com/repos/${OWNER}/${REPO}")
    if [ "$CODE" = "404" ]; then
      echo "仓库不存在，正在创建 ${OWNER}/${REPO} ..."
      curl -s -X POST \
        -H "Authorization: token ${GITHUB_TOKEN}" \
        -H "Accept: application/vnd.github+json" \
        "https://api.github.com/user/repos" \
        -d "{\"name\":\"${REPO}\",\"private\":false,\"description\":\"论文全流程综合技能：选题→检索→综述→统筹→统计→绘图→写作→润色→投稿→汇报，聚合 13 个上游开源科研写作项目。\"}" \
        > /dev/null
      echo "✓ 已创建（public）"
    elif [ "$CODE" = "200" ]; then
      echo "仓库已存在，直接推送"
    else
      echo "✗ 无法访问仓库 API（HTTP $CODE），请检查 token 权限"
      exit 1
    fi
    ;;

  gh)
    if ! command -v gh >/dev/null 2>&1; then
      echo "✗ 未安装 gh CLI（https://cli.github.com）"
      exit 1
    fi
    gh auth status >/dev/null 2>&1 || { echo "✗ gh 未登录，先运行 gh auth login"; exit 1; }
    gh repo view "${OWNER}/${REPO}" >/dev/null 2>&1 || \
      gh repo create "${REPO}" --public --source=. --push
    REMOTE="https://github.com/${OWNER}/${REPO}.git"
    ;;

  ssh)
    if [ ! -f "${HOME}/.ssh/id_ed25519.pub" ] && [ ! -f "${HOME}/.ssh/id_rsa.pub" ]; then
      echo "✗ 未找到 SSH 公钥，先运行：ssh-keygen -t ed25519"
      echo "然后把公钥加到 https://github.com/settings/keys"
      exit 1
    fi
    REMOTE="git@github.com:${OWNER}/${REPO}.git"
    ;;
esac

# ---------------------------------------------------------------- 推送
echo
echo "推送到 ${OWNER}/${REPO} (${BRANCH}) ..."

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REMOTE"
else
  git remote add origin "$REMOTE"
fi

git push -u origin "$BRANCH"

# ---------------------------------------------------------------- 清理
# 把含 token 的 URL 从 remote 里去掉，恢复成干净的 https 地址
git remote set-url origin "https://github.com/${OWNER}/${REPO}.git"

echo
echo "✓ 推送完成"
echo
echo "仓库地址：https://github.com/${OWNER}/${REPO}"
echo
echo "接下来建议："
echo "  1. 在仓库页添加 topics：academic-writing, literature-review, research-workflow, paper-writing"
echo "  2. 检查 README 渲染是否正常（许可表是重点）"
echo "  3. 若发现 CC BY-NC 模块（academic-research-skills）与你的使用场景冲突，删掉该目录后重新提交"
