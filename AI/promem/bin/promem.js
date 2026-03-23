#!/usr/bin/env node
'use strict';

const commands = {
    init: require('../src/commands/init'),
    search: require('../src/commands/search'),
    capture: require('../src/commands/capture'),
    compact: require('../src/commands/compact'),
    evolve: require('../src/commands/evolve'),
    score: require('../src/commands/score'),
    hooks: require('../src/commands/hooks'),
    log: require('../src/commands/log'),
};

const command = process.argv[2];
const args = process.argv.slice(3);

if (command === '--version' || command === '-v') {
    const pkg = require('../package.json');
    console.log(`promem v${pkg.version}`);
    process.exit(0);
}

if (!command || command === '--help' || command === '-h') {
    printHelp();
    process.exit(0);
}

if (!commands[command]) {
    console.error(`Unknown command: ${command}`);
    printHelp();
    process.exit(1);
}

commands[command](args);

function printHelp() {
    console.log(`
ProMem - 为 AI Agent 设计的项目记忆系统

Usage: promem <command> [options]

Commands:
  init                初始化 ProMem（创建 .promem/ 目录，安装 Git Hooks）
  search <query>      搜索项目记忆
  capture             从最近 commit 捕获知识
  compact [--all]     压缩记忆
  evolve              检查知识进化建议
  score               查看知识重要性评分
  hooks <action>      管理 Git Hooks（install/uninstall）
  log                 查看运行日志

Options:
  --help, -h          显示帮助信息
  --version, -v       显示版本号

Examples:
  npx promem init                    在当前项目初始化 ProMem
  npx promem search "状态管理"        搜索相关记忆
  npx promem capture                 从 commit 捕获知识
  npx promem evolve                  检查进化建议
  npx promem log --stats             查看运行统计
`);
}
