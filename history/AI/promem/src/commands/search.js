'use strict';
const { runPythonScript, parseArgs } = require('../utils');

module.exports = function search(args) {
    const parsed = parseArgs(args);
    
    if (parsed.help || parsed.h || args.length === 0) {
        console.log(`
Usage: promem search <query> [options]

Search project memories.

Options:
  --top-k <n>   Number of results (default: 3)
  --help, -h    Show help

Examples:
  promem search "状态管理"
  promem search "login bug" --top-k 5
`);
        return;
    }
    
    const query = parsed._.join(' ');
    const scriptArgs = ['--query', query];
    
    if (parsed['top-k']) {
        scriptArgs.push('--top-k', parsed['top-k']);
    }
    
    runPythonScript('index_memory.py', scriptArgs);
};
