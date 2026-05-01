'use strict';
const { runPythonScript, parseArgs } = require('../utils');

module.exports = function compact(args) {
    const parsed = parseArgs(args);
    
    if (parsed.help || parsed.h) {
        console.log(`
Usage: promem compact [options]

Compress memories into structured summaries.

Options:
  --all            Compact all categories
  --category <cat> Compact specific category
  --check          Only check stats (no compression)
  --force          Force compact (ignore threshold)
  --help, -h       Show help
`);
        return;
    }
    
    const scriptArgs = [];
    if (parsed.all) scriptArgs.push('--all');
    if (parsed.category) scriptArgs.push('--category', parsed.category);
    if (parsed.check) scriptArgs.push('--check');
    if (parsed.force) scriptArgs.push('--force');
    
    runPythonScript('compact.py', scriptArgs);
};
