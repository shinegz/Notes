#!/usr/bin/env node

/**
 * render-mermaid.js
 *
 * Render Mermaid diagrams to beautiful SVG or ASCII art using beautiful-mermaid.
 * Usage: node scripts/render-mermaid.js [options]
 *
 * Options:
 *   -i, --input <file>       Input .mmd file (or use stdin)
 *   -o, --output <file>      Output file (default: stdout)
 *   -t, --theme <name>       Built-in theme name (default: tokyo-night)
 *   -c, --custom <json>      Custom theme as JSON string
 *       --ascii              Render to ASCII instead of SVG
 *       --list-themes        List all available built-in themes
 *   -h, --help               Show help
 *
 * Examples:
 *   node scripts/render-mermaid.js -i diagram.mmd -o output.svg -t tokyo-night
 *   node scripts/render-mermaid.js -i diagram.mmd --ascii
 *   node scripts/render-mermaid.js -i diagram.mmd -o output.svg -c '{"bg":"#1a1b26","fg":"#a9b1d6"}'
 *   echo "graph LR; A-->B" | node scripts/render-mermaid.js --ascii
 */

import { createRequire } from 'module'
import fs from 'fs'
import path from 'path'

const require = createRequire(import.meta.url)

// Lazy import beautiful-mermaid so we can print a helpful error if not installed
let renderMermaidSVG, renderMermaidASCII, THEMES

function loadLibrary() {
  try {
    const lib = require('beautiful-mermaid')
    renderMermaidSVG = lib.renderMermaidSVG
    renderMermaidASCII = lib.renderMermaidASCII
    THEMES = lib.THEMES
  } catch {
    console.error(
      '[render-mermaid] Error: beautiful-mermaid is not installed.\n' +
      'Run: npm install beautiful-mermaid\n' +
      'from the learning-assistant skill directory.'
    )
    process.exit(1)
  }
}

// ---------- CLI argument parsing ----------

function parseArgs(argv) {
  const args = argv.slice(2)
  const opts = {
    input: null,
    output: null,
    theme: 'tokyo-night',
    customTheme: null,
    ascii: false,
    listThemes: false,
    help: false,
  }

  for (let i = 0; i < args.length; i++) {
    const a = args[i]
    if (a === '-i' || a === '--input') {
      opts.input = args[++i]
    } else if (a === '-o' || a === '--output') {
      opts.output = args[++i]
    } else if (a === '-t' || a === '--theme') {
      opts.theme = args[++i]
    } else if (a === '-c' || a === '--custom') {
      opts.customTheme = args[++i]
    } else if (a === '--ascii') {
      opts.ascii = true
    } else if (a === '--list-themes') {
      opts.listThemes = true
    } else if (a === '-h' || a === '--help') {
      opts.help = true
    }
  }

  return opts
}

function printHelp() {
  console.log(`
render-mermaid.js — Render Mermaid diagrams to beautiful SVG or ASCII

Usage: node scripts/render-mermaid.js [options]

Options:
  -i, --input <file>       Input .mmd file (reads stdin if omitted)
  -o, --output <file>      Output file (writes to stdout if omitted)
  -t, --theme <name>       Built-in theme name (default: tokyo-night)
  -c, --custom <json>      Custom theme as JSON, e.g. '{"bg":"#0f0f0f","fg":"#e0e0e0"}'
      --ascii              Render to ASCII/Unicode instead of SVG
      --list-themes        Print all available built-in theme names and exit
  -h, --help               Show this help and exit

Built-in themes: zinc-light, zinc-dark, tokyo-night, tokyo-night-storm,
  tokyo-night-light, catppuccin-mocha, catppuccin-latte, nord, nord-light,
  dracula, github-light, github-dark, solarized-light, solarized-dark, one-dark

Examples:
  node scripts/render-mermaid.js -i diagram.mmd -o output.svg
  node scripts/render-mermaid.js -i diagram.mmd -o output.svg -t github-light
  node scripts/render-mermaid.js -i diagram.mmd --ascii
  node scripts/render-mermaid.js -i diagram.mmd -c '{"bg":"#1a1b26","fg":"#a9b1d6","accent":"#7aa2f7"}'
  echo "graph LR; A-->B-->C" | node scripts/render-mermaid.js --ascii
`)
}

// ---------- Read input ----------

async function readInput(inputPath) {
  if (inputPath) {
    const resolved = path.resolve(inputPath)
    if (!fs.existsSync(resolved)) {
      console.error(`[render-mermaid] Error: Input file not found: ${resolved}`)
      process.exit(1)
    }
    return fs.readFileSync(resolved, 'utf8').trim()
  }

  // Read from stdin
  return new Promise((resolve, reject) => {
    const chunks = []
    process.stdin.setEncoding('utf8')
    process.stdin.on('data', chunk => chunks.push(chunk))
    process.stdin.on('end', () => resolve(chunks.join('').trim()))
    process.stdin.on('error', reject)
  })
}

// ---------- Write output ----------

function writeOutput(content, outputPath) {
  if (outputPath) {
    const resolved = path.resolve(outputPath)
    fs.writeFileSync(resolved, content, 'utf8')
    console.error(`[render-mermaid] Saved to: ${resolved}`)
  } else {
    process.stdout.write(content)
    if (!content.endsWith('\n')) process.stdout.write('\n')
  }
}

// ---------- Main ----------

async function main() {
  const opts = parseArgs(process.argv)

  if (opts.help) {
    printHelp()
    process.exit(0)
  }

  loadLibrary()

  if (opts.listThemes) {
    const themeNames = Object.keys(THEMES)
    console.log('Available built-in themes:\n')
    themeNames.forEach(name => console.log(`  ${name}`))
    process.exit(0)
  }

  const diagramCode = await readInput(opts.input)

  if (!diagramCode) {
    console.error('[render-mermaid] Error: No diagram code provided. Use -i <file> or pipe via stdin.')
    process.exit(1)
  }

  // Resolve theme
  let theme
  if (opts.customTheme) {
    try {
      theme = JSON.parse(opts.customTheme)
    } catch {
      console.error('[render-mermaid] Error: --custom value is not valid JSON.')
      process.exit(1)
    }
  } else {
    theme = THEMES[opts.theme]
    if (!theme) {
      const available = Object.keys(THEMES).join(', ')
      console.error(
        `[render-mermaid] Error: Unknown theme "${opts.theme}".\nAvailable: ${available}`
      )
      process.exit(1)
    }
  }

  // Render
  let output
  try {
    if (opts.ascii) {
      output = renderMermaidASCII(diagramCode)
    } else {
      output = renderMermaidSVG(diagramCode, theme)
    }
  } catch (err) {
    console.error(`[render-mermaid] Render error: ${err.message}`)
    process.exit(1)
  }

  writeOutput(output, opts.output)
}

main().catch(err => {
  console.error('[render-mermaid] Unexpected error:', err)
  process.exit(1)
})
