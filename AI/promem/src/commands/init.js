'use strict';

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const { execSync } = require('child_process');
const { findProjectRoot, checkPython, colors, parseArgs, findScriptsDir, findHooksDir, findTemplatesDir, findIntegrationsDir } = require('../utils');

/**
 * Interactive multi-select menu (pure readline + ANSI)
 * 
 * @param {string} question - Question text
 * @param {Array<{label: string, value: string, default?: boolean}>} options - Options
 * @returns {Promise<string[]>} Selected values array
 */
async function multiSelect(question, options) {
    return new Promise((resolve) => {
        const selected = new Set(
            options.filter(o => o.default).map(o => o.value)
        );
        let cursor = 0;
        let firstRender = true;
        
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });
        
        // Enable raw mode to capture arrow keys
        if (process.stdin.isTTY) {
            process.stdin.setRawMode(true);
        }
        readline.emitKeypressEvents(process.stdin);
        
        function render() {
            if (!firstRender) {
                // Clear previous output
                process.stdout.write('\x1b[' + (options.length + 1) + 'A'); // Move up
                process.stdout.write('\x1b[0J'); // Clear to bottom
            }
            firstRender = false;
            
            console.log(`\x1b[1m? ${question}\x1b[0m \x1b[2m(Space to toggle, Enter to confirm)\x1b[0m`);
            options.forEach((opt, i) => {
                const icon = selected.has(opt.value) ? '\x1b[32m◉\x1b[0m' : '◯';
                const pointer = i === cursor ? '\x1b[36m❯\x1b[0m ' : '  ';
                console.log(`${pointer}${icon} ${opt.label}`);
            });
        }
        
        render();
        
        const onKeypress = (str, key) => {
            if (!key) return;
            
            if (key.name === 'up') {
                cursor = (cursor - 1 + options.length) % options.length;
                render();
            } else if (key.name === 'down') {
                cursor = (cursor + 1) % options.length;
                render();
            } else if (key.name === 'space') {
                const val = options[cursor].value;
                if (selected.has(val)) selected.delete(val);
                else selected.add(val);
                render();
            } else if (key.name === 'return') {
                cleanup();
                resolve([...selected]);
            } else if (key.name === 'c' && key.ctrl) {
                cleanup();
                process.exit(0);
            }
        };
        
        function cleanup() {
            process.stdin.removeListener('keypress', onKeypress);
            if (process.stdin.isTTY) {
                process.stdin.setRawMode(false);
            }
            rl.close();
        }
        
        process.stdin.on('keypress', onKeypress);
    });
}

/**
 * Y/n confirmation prompt
 * 
 * @param {string} question - Question text
 * @param {boolean} defaultYes - Default value
 * @returns {Promise<boolean>}
 */
async function confirm(question, defaultYes = true) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    
    const suffix = defaultYes ? '\x1b[2m(Y/n)\x1b[0m' : '\x1b[2m(y/N)\x1b[0m';
    
    return new Promise((resolve) => {
        rl.question(`\x1b[1m? ${question}\x1b[0m ${suffix} `, (answer) => {
            rl.close();
            if (!answer || answer.trim() === '') resolve(defaultYes);
            else resolve(answer.toLowerCase().startsWith('y'));
        });
    });
}

/**
 * Print help message
 */
function printHelp() {
    console.log(`
${colors.bold('Usage:')} promem init [options]

Initialize ProMem in the current project.

${colors.bold('Options:')}
  --force, -f     Force re-initialization (overwrite existing files)
  --yes, -y       Skip interactive prompts, use defaults
  --tool <names>  Specify AI tools (comma-separated: cursor,claude,qoder)
  --skip-hooks    Skip Git hook installation
  --help, -h      Show this help message

${colors.bold('Examples:')}
  ${colors.dim('# Interactive mode')}
  npx promem init

  ${colors.dim('# Non-interactive with defaults')}
  npx promem init --yes

  ${colors.dim('# Specific tools only')}
  npx promem init --tool cursor,claude

  ${colors.dim('# Skip hooks')}
  npx promem init --yes --skip-hooks

  ${colors.dim('# Force re-initialize')}
  npx promem init --force
`);
}

/**
 * Copy template file if not exists or force
 */
function copyTemplate(templatesDir, templateName, targetPath, force) {
    if (fs.existsSync(targetPath) && !force) return false;
    const src = path.join(templatesDir, templateName);
    if (fs.existsSync(src)) {
        fs.copyFileSync(src, targetPath);
        return true;
    }
    return false;
}

/**
 * Install integration file to project
 * @param {string} templateFile - Template file name
 * @param {string} targetPath - Target file absolute path
 * @param {string} label - Display name (e.g. "Cursor", "Claude Code", "Qoder")
 * @param {boolean} force - Whether to force update ProMem section
 */
function installIntegration(templateFile, targetPath, label, force) {
    const integrationsDir = findIntegrationsDir();
    const tplPath = path.join(integrationsDir, templateFile);
    
    if (!fs.existsSync(tplPath)) {
        console.log(colors.yellow(`  ⚠ Template ${templateFile} not found, skipped`));
        return;
    }
    
    const tpl = fs.readFileSync(tplPath, 'utf8');
    
    if (!fs.existsSync(targetPath)) {
        // File does not exist → create new
        fs.writeFileSync(targetPath, tpl);
        console.log(colors.green(`  ✓ Generated ${path.basename(targetPath)} (${label} integration)`));
        return;
    }
    
    const existing = fs.readFileSync(targetPath, 'utf8');
    
    if (existing.includes('<!-- ProMem Start -->')) {
        if (force) {
            // Replace existing ProMem section
            const updated = existing.replace(
                /<!-- ProMem Start -->[\s\S]*?<!-- ProMem End -->/,
                tpl.trim()
            );
            fs.writeFileSync(targetPath, updated);
            console.log(colors.green(`  ✓ Updated ProMem section in ${path.basename(targetPath)}`));
        } else {
            console.log(colors.yellow(`  ⚠ ${path.basename(targetPath)} already contains ProMem section, skipped (use --force to update)`));
        }
        return;
    }
    
    // File exists but no ProMem section → append
    fs.appendFileSync(targetPath, '\n\n' + tpl);
    console.log(colors.green(`  ✓ Appended ProMem section to ${path.basename(targetPath)}`));
}

/**
 * Install Git hooks
 */
function installGitHooks(projectRoot, options) {
    const hooksSourceDir = findHooksDir();
    const gitHooksDir = path.join(projectRoot, '.git', 'hooks');
    
    if (!fs.existsSync(path.join(projectRoot, '.git'))) {
        console.log(colors.yellow('  ⚠ Not a Git repository, skipping hooks'));
        return 0;
    }
    
    if (!fs.existsSync(gitHooksDir)) {
        fs.mkdirSync(gitHooksDir, { recursive: true });
    }
    
    const hooksToCopy = ['post-merge']; // Always install
    if (options.enableCommitHook) hooksToCopy.push('post-commit');
    if (options.enablePushHook) hooksToCopy.push('pre-push');
    
    let installed = 0;
    for (const hook of hooksToCopy) {
        const src = path.join(hooksSourceDir, hook);
        const dst = path.join(gitHooksDir, hook);
        if (fs.existsSync(src)) {
            // Backup existing hook
            if (fs.existsSync(dst) && !dst.endsWith('.promem-backup')) {
                const backupPath = dst + '.promem-backup';
                if (!fs.existsSync(backupPath)) {
                    fs.copyFileSync(dst, backupPath);
                }
            }
            fs.copyFileSync(src, dst);
            fs.chmodSync(dst, '755');
            installed++;
        }
    }
    
    return installed;
}

/**
 * Print success message
 */
function printSuccess(selectedTools, hooksInstalled) {
    const toolNames = { cursor: 'Cursor', claude: 'Claude Code', qoder: 'Qoder' };
    const toolList = selectedTools.map(t => toolNames[t] || t).join(', ');
    
    console.log(`
${colors.bold(colors.green('✅ ProMem initialized successfully!'))}

  ${colors.dim('AI Tools:')} ${toolList}
  ${colors.dim('Hooks:')} ${hooksInstalled > 0 ? `${hooksInstalled} installed` : 'skipped'}

${colors.bold('Next steps:')}
  ${colors.cyan('•')} Start coding — knowledge is captured automatically on each commit
  ${colors.cyan('•')} Search memories: ${colors.dim('npx promem search "keyword"')}
  ${colors.cyan('•')} Check evolution: ${colors.dim('npx promem evolve')}
  ${colors.cyan('•')} View scores:    ${colors.dim('npx promem score')}
`);
}

/**
 * Main init command
 */
module.exports = async function init(args) {
    const parsed = parseArgs(args);
    
    // Handle help
    if (parsed.help || parsed.h) {
        printHelp();
        return;
    }
    
    // Determine if interactive mode
    const isInteractive = process.stdin.isTTY && !parsed.yes && !parsed.y;
    
    // Print header
    console.log(colors.bold('\n🧠 ProMem - Project Memory for AI Agents\n'));
    
    // Step 1: Check environment
    const projectRoot = findProjectRoot();
    if (!projectRoot) {
        console.error(colors.red('Error: Not a Git repository. Please run "git init" first.'));
        process.exit(1);
    }
    console.log(colors.dim(`Initializing in: ${projectRoot}\n`));
    
    if (!checkPython()) {
        console.error(colors.red('Error: python3 not found. ProMem requires Python 3.6+'));
        process.exit(1);
    }
    
    // Step 2: Select AI tools
    let selectedTools;
    if (parsed.tool) {
        selectedTools = parsed.tool.split(',').map(t => t.trim().toLowerCase());
    } else if (isInteractive) {
        selectedTools = await multiSelect('Select your AI coding tools:', [
            { label: 'Cursor', value: 'cursor', default: true },
            { label: 'Claude Code', value: 'claude', default: true },
            { label: 'Qoder', value: 'qoder', default: false },
        ]);
        console.log(''); // Add spacing after selection
    } else {
        selectedTools = ['cursor', 'claude']; // Default
    }
    
    // Step 3: Select hooks
    let enableCommitHook = true;
    let enablePushHook = true;
    
    if (parsed['skip-hooks']) {
        enableCommitHook = false;
        enablePushHook = false;
    } else if (isInteractive) {
        enableCommitHook = await confirm('Enable auto-capture on git commit?', true);
        enablePushHook = await confirm('Enable pre-push regression analysis?', true);
        console.log(''); // Add spacing
    }
    
    // Step 4: Setup
    console.log(colors.cyan('Setting up ProMem...\n'));
    
    const promemDir = path.join(projectRoot, '.promem');
    const force = parsed.force || parsed.f;
    
    // Check if already exists
    if (fs.existsSync(promemDir) && !force) {
        console.log(colors.yellow('  .promem/ already exists. Use --force to re-initialize.'));
        console.log(colors.dim('  Continuing with integration files and hooks...\n'));
    }
    
    // Create directory structure
    const dirs = [
        'memory/decisions',
        'memory/bugs',
        'memory/rules',
        'memory/entities',
        'memory/journal',
        'memory/summaries',
        'memory/suggestions',
        'memory/archive',         // 归档目录
    ];
    
    for (const dir of dirs) {
        fs.mkdirSync(path.join(promemDir, dir), { recursive: true });
    }
    console.log(colors.green('  ✓ Created .promem/ directory structure'));
    
    // Step 5: Copy template files
    const templatesDir = findTemplatesDir();
    
    if (copyTemplate(templatesDir, 'config.yaml', path.join(promemDir, 'config.yaml'), force)) {
        console.log(colors.green('  ✓ Created .promem/config.yaml'));
    }
    
    if (copyTemplate(templatesDir, 'gitignore', path.join(promemDir, '.gitignore'), force)) {
        console.log(colors.green('  ✓ Created .promem/.gitignore'));
    }
    
    if (copyTemplate(templatesDir, 'RULES.md', path.join(promemDir, 'RULES.md'), force)) {
        console.log(colors.green('  ✓ Created .promem/RULES.md'));
    }
    
    if (copyTemplate(templatesDir, 'PATTERNS.md', path.join(promemDir, 'PATTERNS.md'), force)) {
        console.log(colors.green('  ✓ Created .promem/PATTERNS.md'));
    }
    
    // Step 6: Generate AI tool integration files (unified logic)
    if (selectedTools.includes('cursor')) {
        installIntegration('cursorrules.tpl', path.join(projectRoot, '.cursorrules'), 'Cursor', force);
    }
    
    if (selectedTools.includes('claude')) {
        installIntegration('claude-md.tpl', path.join(projectRoot, 'CLAUDE.md'), 'Claude Code', force);
    }
    
    if (selectedTools.includes('qoder')) {
        installIntegration('agents-md.tpl', path.join(projectRoot, 'AGENTS.md'), 'Qoder', force);
    }
    
    // Step 7: Install Git Hooks
    let hooksInstalled = 0;
    if (enableCommitHook || enablePushHook) {
        hooksInstalled = installGitHooks(projectRoot, { enableCommitHook, enablePushHook });
        if (hooksInstalled > 0) {
            const hookNames = [];
            if (enableCommitHook) hookNames.push('post-commit');
            if (enablePushHook) hookNames.push('pre-push');
            hookNames.push('post-merge');
            console.log(colors.green(`  ✓ Installed Git hooks (${hookNames.join(', ')})`));
        }
    } else {
        console.log(colors.dim('  ○ Skipped Git hook installation'));
    }
    
    // Step 8: Build index if there are existing memories
    const memoryDir = path.join(promemDir, 'memory');
    try {
        const allFiles = [];
        const walkDir = (dir) => {
            if (!fs.existsSync(dir)) return;
            for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
                if (entry.isDirectory()) {
                    walkDir(path.join(dir, entry.name));
                } else if (entry.name.endsWith('.md')) {
                    allFiles.push(entry.name);
                }
            }
        };
        walkDir(memoryDir);
        
        if (allFiles.length > 0) {
            console.log(colors.dim('  Building initial index...'));
            const scriptsDir = findScriptsDir();
            const indexScript = path.join(scriptsDir, 'index_memory.py');
            if (fs.existsSync(indexScript)) {
                try {
                    execSync(`python3 "${indexScript}" --full --memory-root "${memoryDir}"`, { stdio: 'pipe' });
                    console.log(colors.green('  ✓ Built memory index'));
                } catch {
                    console.log(colors.yellow('  ⚠ Index build skipped'));
                }
            }
        }
    } catch {
        // Ignore errors during index building
    }
    
    // Done
    printSuccess(selectedTools, hooksInstalled);
};
