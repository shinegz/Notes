'use strict';

const { findPromemData, colors, parseArgs } = require('../utils');
const fs = require('fs');
const path = require('path');

/**
 * 查找 .promem 目录（优先查找当前目录，再向上查找）
 */
function findPromemDir(startDir = process.cwd()) {
    let dir = startDir;
    while (dir !== path.dirname(dir)) {
        const promemDir = path.join(dir, '.promem');
        if (fs.existsSync(promemDir)) {
            return promemDir;
        }
        dir = path.dirname(dir);
    }
    return null;
}

/**
 * log 命令 - 查看 ProMem 运行日志
 */
module.exports = function log(args) {
    const parsed = parseArgs(args);
    
    if (parsed.help || parsed.h) {
        console.log(`
Usage: promem log [options]

查看 ProMem 运行日志

Options:
  --tail N        显示最近 N 条（默认 20）
  --stats         显示统计摘要
  --filter TYPE   按事件类型过滤（CAPTURE/SKIP/CLASSIFY/DUPLICATE/SEARCH/COMPACT/ARCHIVE/EVOLVE/ERROR）
  --since DATE    显示指定日期之后的日志（格式 YYYY-MM-DD）
  --help, -h      显示帮助

Examples:
  promem log                    # 显示最近 20 条日志
  promem log --tail 50          # 显示最近 50 条
  promem log --stats            # 显示统计摘要
  promem log --filter CAPTURE   # 只看捕获日志
  promem log --since 2026-03-20 # 显示 3 月 20 日之后的日志
        `);
        return;
    }
    
    // 优先查找当前目录的 .promem
    const promemDir = findPromemDir();
    if (!promemDir) {
        console.error(colors.red('Error: .promem/ not found'));
        process.exit(1);
    }
    
    const logPath = path.join(promemDir, 'promem.log');
    
    if (!fs.existsSync(logPath)) {
        console.log(colors.yellow('No logs yet. Logs are generated as ProMem operates.'));
        console.log(colors.dim('Try running: promem capture'));
        return;
    }
    
    const content = fs.readFileSync(logPath, 'utf8');
    const lines = content.trim().split('\n').filter(Boolean);
    
    if (lines.length === 0) {
        console.log(colors.yellow('Log file is empty.'));
        return;
    }
    
    if (parsed.stats) {
        // 统计模式
        showStats(lines, parsed.since);
        return;
    }
    
    // 过滤
    let filtered = lines;
    if (parsed.filter) {
        const type = parsed.filter.toUpperCase();
        filtered = filtered.filter(l => {
            // 匹配格式: [timestamp] EVENT_TYPE module |
            const match = l.match(/\]\s+(\w+)\s+/);
            return match && match[1] === type;
        });
    }
    if (parsed.since) {
        filtered = filtered.filter(l => {
            const match = l.match(/\[(\d{4}-\d{2}-\d{2})/);
            return match && match[1] >= parsed.since;
        });
    }
    
    // tail
    const n = parseInt(parsed.tail) || 20;
    const display = filtered.slice(-n);
    
    if (display.length === 0) {
        console.log(colors.yellow('No matching log entries.'));
        return;
    }
    
    // 彩色输出
    console.log(colors.bold('\n📋 ProMem 运行日志\n'));
    display.forEach(line => {
        if (line.includes('] CAPTURE ')) console.log(colors.green(line));
        else if (line.includes('] SKIP ')) console.log(colors.dim(line));
        else if (line.includes('] CLASSIFY ')) console.log(colors.cyan(line));
        else if (line.includes('] DUPLICATE ')) console.log(colors.yellow(line));
        else if (line.includes('] ERROR ')) console.log(colors.red(line));
        else if (line.includes('] SEARCH ')) console.log(colors.cyan(line));
        else if (line.includes('] COMPACT ')) console.log(colors.yellow(line));
        else if (line.includes('] ARCHIVE ')) console.log(colors.yellow(line));
        else if (line.includes('] EVOLVE ')) console.log(colors.magenta ? colors.magenta(line) : colors.cyan(line));
        else console.log(line);
    });
    
    if (filtered.length > n) {
        console.log(colors.dim(`\n... ${filtered.length - n} more entries (use --tail ${filtered.length} to see all)`));
    }
    console.log('');
};

/**
 * 显示统计摘要
 */
function showStats(lines, since) {
    let filtered = lines;
    if (since) {
        filtered = filtered.filter(l => {
            const match = l.match(/\[(\d{4}-\d{2}-\d{2})/);
            return match && match[1] >= since;
        });
    }
    
    const counts = {};
    const skipReasons = {};
    const categories = {};
    let errorCount = 0;
    
    filtered.forEach(line => {
        // 统计事件类型
        const typeMatch = line.match(/\]\s+(\w+)\s+/);
        if (typeMatch) {
            const type = typeMatch[1];
            counts[type] = (counts[type] || 0) + 1;
            
            if (type === 'ERROR') {
                errorCount++;
            }
        }
        
        // 统计跳过原因
        if (line.includes('] SKIP ') || line.includes('] DUPLICATE ')) {
            const reasonMatch = line.match(/reason=(\S+)/);
            if (reasonMatch) {
                const reason = reasonMatch[1];
                skipReasons[reason] = (skipReasons[reason] || 0) + 1;
            }
        }
        
        // 统计捕获分类
        if (line.includes('] CAPTURE ') || line.includes('] CLASSIFY ')) {
            const catMatch = line.match(/category=(\w+)/);
            if (catMatch) {
                const cat = catMatch[1];
                categories[cat] = (categories[cat] || 0) + 1;
            }
        }
    });
    
    console.log(colors.bold('\n📊 ProMem 运行统计\n'));
    console.log(colors.dim(`日志条目: ${filtered.length}${since ? ` (since ${since})` : ''}\n`));
    
    // 事件分布
    console.log(colors.bold('事件分布:'));
    const maxCount = Math.max(...Object.values(counts), 1);
    Object.entries(counts).sort((a, b) => b[1] - a[1]).forEach(([type, count]) => {
        const barLen = Math.ceil((count / maxCount) * 30);
        const bar = '█'.repeat(Math.min(barLen, 30));
        const typeColor = getTypeColor(type);
        console.log(`  ${type.padEnd(12)} ${String(count).padStart(4)}  ${typeColor(bar)}`);
    });
    
    // 捕获分类
    if (Object.keys(categories).length > 0) {
        console.log(colors.bold('\n捕获分类:'));
        Object.entries(categories).sort((a, b) => b[1] - a[1]).forEach(([cat, count]) => {
            console.log(`  ${cat.padEnd(15)} ${count}`);
        });
    }
    
    // 跳过原因
    if (Object.keys(skipReasons).length > 0) {
        console.log(colors.bold('\n跳过原因:'));
        Object.entries(skipReasons).sort((a, b) => b[1] - a[1]).forEach(([reason, count]) => {
            console.log(`  ${reason.padEnd(20)} ${count}`);
        });
    }
    
    // 捕获率
    const captured = counts['CAPTURE'] || 0;
    const skipped = (counts['SKIP'] || 0) + (counts['DUPLICATE'] || 0);
    const total = captured + skipped;
    if (total > 0) {
        const rate = ((captured / total) * 100).toFixed(1);
        console.log(colors.bold(`\n捕获率: ${rate}% (${captured}/${total})`));
    }
    
    // 错误统计
    if (errorCount > 0) {
        console.log(colors.red(`\n⚠️  错误数: ${errorCount}`));
    }
    
    console.log('');
}

/**
 * 获取事件类型对应的颜色函数
 */
function getTypeColor(type) {
    switch (type) {
        case 'CAPTURE': return colors.green;
        case 'SKIP': return colors.dim;
        case 'CLASSIFY': return colors.cyan;
        case 'DUPLICATE': return colors.yellow;
        case 'ERROR': return colors.red;
        case 'SEARCH': return colors.cyan;
        case 'COMPACT': return colors.yellow;
        case 'ARCHIVE': return colors.yellow;
        case 'EVOLVE': return colors.magenta || colors.cyan;
        default: return (s) => s;
    }
}
