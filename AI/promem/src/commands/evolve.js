'use strict';
const { runPythonScript, parseArgs } = require('../utils');

module.exports = function evolve(args) {
    const parsed = parseArgs(args);
    
    if (parsed.help || parsed.h) {
        console.log(`
Usage: promem evolve [options]

Analyze memories for evolution opportunities.

Options:
  --check         Check for suggestions (default)
  --analyze       Full analysis
  --apply <id>    Apply a suggestion (e.g., SUG-001)
  --history       View suggestion history
  --help, -h      Show help
`);
        return;
    }
    
    const scriptArgs = [];
    if (parsed.apply) scriptArgs.push('--apply', parsed.apply);
    else if (parsed.history) scriptArgs.push('--history');
    else if (parsed.analyze) scriptArgs.push('--analyze');
    else scriptArgs.push('--check');
    
    runPythonScript('evolve.py', scriptArgs);
};
