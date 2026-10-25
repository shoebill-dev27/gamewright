#!/usr/bin/env node
'use strict';
// Usage: node play.js [--trace] <script-file | ->    (format: see manual.md)
const fs = require('fs');
const SC = require('./src/script.js');

const USAGE = 'Usage: node play.js [--trace] <script-file | ->\nSee manual.md for the script format.';

function main(argv) {
  let trace = false;
  const files = [];
  for (const a of argv.slice(2)) {
    if (a === '--trace') trace = true;
    else if (a === '-h' || a === '--help') { console.log(USAGE); return 0; }
    else files.push(a);
  }
  if (files.length !== 1) { console.error(USAGE); return 2; }
  let text;
  try { text = files[0] === '-' ? fs.readFileSync(0, 'utf8') : fs.readFileSync(files[0], 'utf8'); }
  catch (e) { console.error('Cannot read script: ' + e.message); return 2; }
  let parsed;
  try { parsed = SC.parseScript(text); } catch (e) { console.error(e.message); return 2; }
  const res = SC.runScript(parsed.seed, parsed.commands);
  console.log(SC.renderRun(res, { trace: trace }));
  return 0;
}

process.exitCode = main(process.argv);
