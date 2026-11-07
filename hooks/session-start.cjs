'use strict';
const { bootstrap } = require('../integrations/bootstrap.cjs');
const arg = process.argv.indexOf('--host');
const host = arg >= 0 ? process.argv[arg + 1] :
  process.env.CURSOR_PLUGIN_ROOT ? 'cursor' : process.env.COPILOT_CLI ? 'copilot' :
  process.env.MUSE_PLUGIN_ROOT ? 'muse' : 'claude';
try {
  if (!['claude', 'cursor', 'copilot', 'muse'].includes(host)) throw new Error('Unknown hook host');
  const content = bootstrap(host);
  const payload = host === 'cursor' ? {additional_context: content} :
    host === 'copilot' ? {additionalContext: content} :
    {hookSpecificOutput: {hookEventName: 'SessionStart', additionalContext: content}};
  process.stdout.write(JSON.stringify(payload) + '\n');
} catch (error) {
  process.stderr.write(`System Design bootstrap unavailable: ${error.message}\n`);
  process.exitCode = 1;
}
