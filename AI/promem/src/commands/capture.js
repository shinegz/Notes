'use strict';
const { runPythonScript, parseArgs } = require('../utils');

module.exports = function capture(args) {
    const parsed = parseArgs(args);
    
    if (parsed.help || parsed.h) {
        console.log(`
Usage: promem capture [options]

Capture knowledge from recent git commits.

Options:
  --since <ref>  Git ref to start from (default: latest commit)
  --help, -h     Show help
`);
        return;
    }
    
    const scriptArgs = [];
    if (parsed.since) scriptArgs.push('--since', parsed.since);
    
    runPythonScript('capture_from_commit.py', scriptArgs);
};
