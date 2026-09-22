#!/usr/bin/env node
// exuvia — uniform installer for Claude Code / Codex / omp / Cursor / OpenCode adapters.
// Zero dependencies. Renders adapters from core/ + templates/ so all harnesses share one source of truth.
"use strict";
const fs = require("fs");
const os = require("os");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const read = (p) => fs.readFileSync(path.join(ROOT, p), "utf8");
const AUDIT = read("core/AUDIT.md");
const APPLY = read("core/APPLY.md");
const DRIFT = read("core/DRIFT.md");
const TESTS = read("core/TESTS.md");
const BLAME = read("core/BLAME.md");
const TRANSLATE = read("core/TRANSLATE.md");
const render = (t) => t.replaceAll("{{AUDIT_BODY}}", AUDIT).replaceAll("{{APPLY_BODY}}", APPLY).replaceAll("{{DRIFT_BODY}}", DRIFT).replaceAll("{{TESTS_BODY}}", TESTS).replaceAll("{{BLAME_BODY}}", BLAME).replaceAll("{{TRANSLATE_BODY}}", TRANSLATE);
const HOME = os.homedir();

function harnesses() {
  const T = {
    skill: read("templates/skill.md"),
    skillDrift: read("templates/skill-drift.md"),
    skillConstitution: read("templates/skill-constitution.md"),
    skillBlame: read("templates/skill-blame.md"),
    skillTranslate: read("templates/skill-translate.md"),
    cmdAudit: read("templates/command-audit.md"),
    cmdApply: read("templates/command-apply.md"),
    cmdDrift: read("templates/command-drift.md"),
    cmdTest: read("templates/command-test.md"),
    cmdBlame: read("templates/command-blame.md"),
    cmdTranslate: read("templates/command-translate.md"),
    cursor: read("templates/cursor-rule.mdc"),
    opencode: read("templates/opencode.md"),
  };
  return [
    {
      id: "claude", name: "Claude Code", marker: path.join(HOME, ".claude"),
      targets: [
        ["commands/exuvia-audit.md", render(T.cmdAudit)],
        ["commands/exuvia-apply.md", render(T.cmdApply)],
        ["commands/exuvia-drift.md", render(T.cmdDrift)],
        ["commands/exuvia-test.md", render(T.cmdTest)],
        ["commands/exuvia-blame.md", render(T.cmdBlame)],
        ["commands/exuvia-translate.md", render(T.cmdTranslate)],
      ].map(([rel, content]) => [path.join(HOME, ".claude", rel), content]),
    },
    {
      id: "codex", name: "Codex", marker: path.join(HOME, ".codex"),
      targets: [
        ["prompts/exuvia-audit.md", render(T.cmdAudit)],
        ["prompts/exuvia-apply.md", render(T.cmdApply)],
        ["prompts/exuvia-drift.md", render(T.cmdDrift)],
        ["prompts/exuvia-test.md", render(T.cmdTest)],
        ["prompts/exuvia-blame.md", render(T.cmdBlame)],
        ["prompts/exuvia-translate.md", render(T.cmdTranslate)],
        ["skills/exuvia-audit/SKILL.md", render(T.skill)],
      ].map(([rel, content]) => [path.join(HOME, ".codex", rel), content]),
    },
    {
      id: "omp", name: "omp", marker: path.join(HOME, ".omp", "agent"),
      targets: [
        ["skills/exuvia-audit/SKILL.md", render(T.skill)],
        ["skills/exuvia-drift/SKILL.md", render(T.skillDrift)],
        ["skills/exuvia-constitution/SKILL.md", render(T.skillConstitution)],
        ["skills/exuvia-blame/SKILL.md", render(T.skillBlame)],
        ["skills/exuvia-translate/SKILL.md", render(T.skillTranslate)],
      ].map(([rel, content]) => [path.join(HOME, ".omp", "agent", rel), content]),
    },
    {
      id: "cursor", name: "Cursor", marker: path.join(HOME, ".cursor"),
      targets: [[path.join(HOME, ".cursor", "rules", "exuvia.mdc"), render(T.cursor)]],
    },
    {
      id: "opencode", name: "OpenCode", marker: path.join(HOME, ".config", "opencode"),
      targets: [[path.join(HOME, ".config", "opencode", "command", "exuvia.md"), render(T.opencode)]],
    },
  ];
}

function copyTree(src, dst, dry) {
  let wrote = 0;
  for (const e of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, e.name), d = path.join(dst, e.name);
    if (e.isDirectory()) wrote += copyTree(s, d, dry);
    else {
      if (fs.existsSync(d) && fs.readFileSync(d, "utf8") === fs.readFileSync(s, "utf8")) continue;
      if (!dry) { fs.mkdirSync(path.dirname(d), { recursive: true }); fs.copyFileSync(s, d); }
      wrote++;
    }
  }
  return wrote;
}

function installEngines(dry) {
  const dst = path.join(HOME, ".exuvia", "engines");
  let wrote = 0;
  for (const dir of ["meters", "drift", "constitution", "blame", "translate", "core"]) {
    wrote += copyTree(path.join(ROOT, dir), path.join(dst, dir), dry);
  }
  console.log(`  ${wrote === 0 && !dry ? "=" : dry ? "~" : "+"} engines -> ~/.exuvia/engines (${wrote} file${wrote === 1 ? "" : "s"} changed)`);
}

const detected = () => harnesses().filter((h) => fs.existsSync(h.marker));

function status() {
  const all = harnesses();
  if (!all.length) return console.log("no harness templates found (broken install?)");
  console.log("Harnesses on this machine:");
  for (const h of all) {
    const det = fs.existsSync(h.marker);
    const inst = h.targets.every(([p]) => fs.existsSync(p));
    console.log(`  ${h.name.padEnd(12)} ${det ? "detected" : "not found"} · adapter ${inst ? "INSTALLED" : det ? "missing (run: exuvia init)" : "n/a"}`);
  }
}

function install(dry) {
  const list = detected();
  if (!list.length) return console.log("No supported harness detected. Nothing to do.");
  for (const h of list) {
    for (const [dest, content] of h.targets) {
      if (fs.existsSync(dest) && fs.readFileSync(dest, "utf8") === content) {
        console.log(`  = ${h.name}: up-to-date ${path.relative(HOME, dest)}`);
        continue;
      }
      if (dry) { console.log(`  ~ ${h.name}: would write ${path.relative(HOME, dest)}`); continue; }
      fs.mkdirSync(path.dirname(dest), { recursive: true });
      fs.writeFileSync(dest, content);
      console.log(`  + ${h.name}: wrote ${path.relative(HOME, dest)}`);
    }
  }
  installEngines(dry);
  if (!dry) console.log(
    "\nDone. Commands (Claude Code / Codex): /exuvia-audit, /exuvia-apply, /exuvia-drift, /exuvia-test, /exuvia-blame.\n" +
    "omp / Cursor / OpenCode: ask \"audit my prompt debt\" / \"check instruction drift\" / \"blame this line\".\n" +
    "Python engines: ~/.exuvia/engines");
}

function uninstall() {
  for (const h of harnesses()) {
    for (const [dest] of h.targets) {
      if (fs.existsSync(dest)) { fs.rmSync(dest); console.log(`  - removed ${path.relative(HOME, dest)}`); }
    }
  }
  const eng = path.join(HOME, ".exuvia");
  if (fs.existsSync(eng)) { fs.rmSync(eng, { recursive: true, force: true }); console.log("  - removed ~/.exuvia (engines)"); }
}


const cmd = process.argv[2] || "status";
if (cmd === "status") status();
else if (cmd === "init") install(process.argv.includes("--dry"));
else if (cmd === "uninstall") uninstall();
else { console.log("usage: exuvia [status | init [--dry] | uninstall]"); process.exit(2); }
