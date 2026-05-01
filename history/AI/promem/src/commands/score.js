'use strict';
const { runPythonScript, parseArgs } = require('../utils');

module.exports = function score(args) {
    const parsed = parseArgs(args);
    
    if (parsed.help || parsed.h) {
        console.log(`
Usage: promem score [options]

Knowledge importance scoring and smart supply.

Options:
  --suggest --context <text>  Get knowledge suggestions for context
  --cite <file>               Record a citation
  --archive [file]            Archive memories (auto if no file specified)
  --dry-run                   Preview archive without executing (use with --archive)
  --gaps                      Detect knowledge gaps
  --help, -h                  Show help

Examples:
  promem score                         # Show all memory scores
  promem score --archive --dry-run     # Preview auto-archive
  promem score --archive               # Execute auto-archive
  promem score --archive decisions/xxx.md  # Archive specific file
`);
        return;
    }
    
    const scriptArgs = [];
    if (parsed.suggest) {
        scriptArgs.push('--suggest');
        if (parsed.context) scriptArgs.push('--context', parsed.context);
    } else if (parsed.cite) {
        scriptArgs.push('--cite', parsed.cite);
    } else if (parsed.archive !== undefined) {
        if (parsed.archive === true || parsed.archive === '') {
            // --archive without value: auto mode
            scriptArgs.push('--archive');
        } else {
            // --archive with file path
            scriptArgs.push('--archive', parsed.archive);
        }
        if (parsed['dry-run']) {
            scriptArgs.push('--dry-run');
        }
    } else if (parsed.gaps) {
        scriptArgs.push('--gaps');
    } else {
        scriptArgs.push('--score');
    }
    
    runPythonScript('importance.py', scriptArgs);
};
