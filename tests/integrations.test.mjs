import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { readFileSync, mkdirSync, cpSync, rmSync, existsSync } from 'node:fs';
import { randomUUID } from 'node:crypto';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('../', import.meta.url));

test('session hooks emit exactly the host field and the shared policies', () => {
  for (const [host, field] of [['claude','hookSpecificOutput'], ['cursor','additional_context'],
                              ['copilot','additionalContext'], ['muse','hookSpecificOutput']]) {
    const run = spawnSync(process.execPath, [root + 'hooks/session-start.cjs','--host',host], {encoding:'utf8'});
    assert.equal(run.status, 0, run.stderr);
    const payload = JSON.parse(run.stdout);
    assert.deepEqual(Object.keys(payload), [field]);
    const content = typeof payload[field] === 'string' ? payload[field] : payload[field].additionalContext;
    assert.ok(content.includes('Static review'));
    assert.ok(content.includes('system-design-enter'));
    assert.ok(content.includes('docs/architecture/system-design/'));
    assert.ok(content.includes(readFileSync(root + 'skills/system-design-enter/references/policies.md','utf8')));
  }
});

test('hook refuses an unknown host without claiming successful injection', () => {
  const run = spawnSync(process.execPath, [root + 'hooks/session-start.cjs','--host','missing-host'], {encoding:'utf8'});
  assert.equal(run.status,1);
  assert.equal(run.stdout,'');
  assert.match(run.stderr,/Unknown hook host/);
});

test('relocated bootstrap has no dependency on reference checkout and fails clearly on missing policies', () => {
  const temporary = path.resolve(root,'../.system-design-test-temp/node-' + randomUUID());
  mkdirSync(temporary,{recursive:true});
  try {
    cpSync(root + 'hooks', path.join(temporary,'hooks'),{recursive:true});
    cpSync(root + 'integrations', path.join(temporary,'integrations'),{recursive:true});
    const missing = spawnSync(process.execPath,[path.join(temporary,'hooks/session-start.cjs')],{encoding:'utf8'});
    assert.equal(missing.status,1);
    assert.equal(missing.stdout,'');
    assert.match(missing.stderr,/bootstrap unavailable/);
    cpSync(root + 'skills', path.join(temporary,'skills'),{recursive:true});
    const complete = spawnSync(process.execPath,[path.join(temporary,'hooks/session-start.cjs')],{encoding:'utf8'});
    assert.equal(complete.status,0,complete.stderr);
    assert.ok(JSON.parse(complete.stdout).hookSpecificOutput.additionalContext.includes('Static review'));
  } finally {
    // Computed target is verified inside the dedicated workspace scratch directory.
    assert.ok(temporary.startsWith(path.resolve(root,'../.system-design-test-temp') + path.sep));
    rmSync(temporary,{recursive:true,force:true});
  }
});

test('OpenCode V1 discovery is idempotent and request injection survives fresh histories', async () => {
  const { SystemDesignPlugin } = await import('../.opencode/plugins/system-design.js');
  const hooks = await SystemDesignPlugin({});
  const config = {skills:{paths:['other']}};
  await hooks.config(config); await hooks.config(config);
  assert.equal(config.skills.paths.length, 2);
  for (let turn=0; turn<2; turn++) {
    const output = {messages:[{info:{role:'user'}, parts:[{type:'text',text:'review architecture'}]}]};
    await hooks['experimental.chat.messages.transform']({}, output);
    await hooks['experimental.chat.messages.transform']({}, output);
    assert.equal(output.messages[0].parts.length, 2);
    assert.ok(output.messages[0].parts[0].text.includes('Static review'));
  }
});

test('OpenCode V2 registers five skills and covers context, compaction and generate', async () => {
  const mod = (await import('../.opencode/plugins/system-design.js')).default;
  const skills = [], hooks = {};
  await mod.setup({skill:{transform: async cb => cb({add:s=>skills.push(s)})},
                   session:{hook:async (name,cb)=>{hooks[name]=cb;}}});
  assert.equal(skills.length,5);
  for(const s of skills) assert.ok(readFileSync(s.path,'utf8').includes(s.name));
  for (const name of ['context','compaction','generate']) {
    const event = {messages:[{role:'user',content:[{type:'text',text:'plan'}]}]};
    await hooks[name](event); await hooks[name](event);
    assert.equal(event.messages[0].content.length,2);
  }
  const checkpoint = {messages:[{role:'checkpoint',content:[]}]};
  await hooks.compaction(checkpoint);
  assert.equal(checkpoint.messages[1].role,'user');
});

test('Pi reinjects on every transient context and preserves compaction summary', async () => {
  const extension = (await import('../.pi/extensions/system-design.ts')).default;
  const handlers = {};
  extension({on:(name,cb)=>{handlers[name]=cb;}});
  const original = [{role:'compactionSummary',content:'summary'}, {role:'user',content:'review'}];
  for(let turn=0;turn<2;turn++) {
    const result = await handlers.context({messages:original});
    assert.equal(result.messages.length,3);
    assert.equal(result.messages[0], original[0]);
    assert.ok(result.messages[1].content[0].text.includes('Static review'));
    assert.equal((await handlers.context({messages:result.messages})), undefined);
  }
  assert.equal(original.length,2);
});
