'use strict';

const { execSync, spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

/**
 * 查找项目根目录（向上查找 .git 或 .promem 目录）
 */
function findProjectRoot(startDir = process.cwd()) {
    let dir = startDir;
    while (dir !== path.dirname(dir)) {
        if (fs.existsSync(path.join(dir, '.git'))) {
            return dir;
        }
        // Also check for .promem for non-git projects
        if (fs.existsSync(path.join(dir, '.promem'))) {
            return dir;
        }
        dir = path.dirname(dir);
    }
    return null;
}

/**
 * 查找用户项目的 .promem 数据目录
 */
function findPromemData(startDir = process.cwd()) {
    const projectRoot = findProjectRoot(startDir);
    if (!projectRoot) return null;
    const promemDir = path.join(projectRoot, '.promem');
    return fs.existsSync(promemDir) ? promemDir : null;
}

/**
 * 查找 npm 包内的 scripts 目录
 */
function findScriptsDir() {
    return path.resolve(__dirname, 'scripts');
}

/**
 * 查找 npm 包内的 hooks 目录
 */
function findHooksDir() {
    return path.resolve(__dirname, 'templates', 'hooks');
}

/**
 * 查找 npm 包内的 templates 目录
 */
function findTemplatesDir() {
    return path.resolve(__dirname, 'templates');
}

/**
 * 查找 npm 包内的 integrations 目录
 */
function findIntegrationsDir() {
    return path.resolve(__dirname, 'templates', 'integrations');
}

/**
 * 检查 python3 是否可用
 */
function checkPython() {
    try {
        execSync('python3 --version', { stdio: 'pipe' });
        return true;
    } catch {
        return false;
    }
}

/**
 * 执行 Python 脚本，实时输出
 */
function runPythonScript(scriptName, args = [], options = {}) {
    const scriptsDir = findScriptsDir();
    const scriptPath = path.join(scriptsDir, scriptName);
    
    if (!fs.existsSync(scriptPath)) {
        console.error(`Error: Script not found: ${scriptPath}`);
        process.exit(1);
    }
    
    // 自动注入 --memory-root（如果脚本支持且未指定）
    if (!args.includes('--memory-root')) {
        const promemData = findPromemData();
        if (promemData) {
            const memoryRoot = path.join(promemData, 'memory');
            if (fs.existsSync(memoryRoot)) {
                args.push('--memory-root', memoryRoot);
            }
        }
    }
    
    const child = spawn('python3', [scriptPath, ...args], {
        stdio: 'inherit',
        cwd: options.cwd || findProjectRoot()
    });
    
    child.on('close', (code) => {
        process.exit(code || 0);
    });
    
    child.on('error', (err) => {
        console.error(`Failed to execute: ${err.message}`);
        process.exit(2);
    });
}

/**
 * 解析命令行参数为 key-value
 */
function parseArgs(args) {
    const parsed = { _: [] };
    for (let i = 0; i < args.length; i++) {
        if (args[i].startsWith('--')) {
            const key = args[i].slice(2);
            if (i + 1 < args.length && !args[i + 1].startsWith('-')) {
                parsed[key] = args[i + 1];
                i++;
            } else {
                parsed[key] = true;
            }
        } else if (args[i].startsWith('-')) {
            const key = args[i].slice(1);
            parsed[key] = true;
        } else {
            parsed._.push(args[i]);
        }
    }
    return parsed;
}

/**
 * 彩色输出（不依赖 chalk，用 ANSI 转义码）
 */
const colors = {
    green: (text) => `\x1b[32m${text}\x1b[0m`,
    red: (text) => `\x1b[31m${text}\x1b[0m`,
    yellow: (text) => `\x1b[33m${text}\x1b[0m`,
    cyan: (text) => `\x1b[36m${text}\x1b[0m`,
    bold: (text) => `\x1b[1m${text}\x1b[0m`,
    dim: (text) => `\x1b[2m${text}\x1b[0m`,
};

module.exports = {
    findProjectRoot,
    findPromemData,
    findScriptsDir,
    findHooksDir,
    findTemplatesDir,
    findIntegrationsDir,
    checkPython,
    runPythonScript,
    parseArgs,
    colors,
};
