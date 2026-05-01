'use strict';
const { runPythonScript, parseArgs, findProjectRoot, colors } = require('../utils');

module.exports = function hooks(args) {
    const parsed = parseArgs(args);
    const action = parsed._[0]; // install/uninstall
    
    if (parsed.help || parsed.h || !action) {
        console.log(`
Usage: promem hooks <action>

Manage Git Hooks.

Actions:
  install     Install ProMem hooks (post-commit, pre-push, post-merge)
  uninstall   Remove ProMem hooks

Examples:
  promem hooks install
  promem hooks uninstall
`);
        return;
    }
    
    const scriptArgs = [];
    const projectRoot = findProjectRoot();
    if (projectRoot) {
        scriptArgs.push('--repo-root', projectRoot);
    }
    
    if (action === 'uninstall') {
        scriptArgs.push('--uninstall');
    } else if (action !== 'install') {
        console.error(colors.red(`Unknown action: ${action}`));
        process.exit(1);
    }
    
    runPythonScript('install_hooks.py', scriptArgs);
};
