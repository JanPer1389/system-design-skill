'use strict';
const fs = require('node:fs');
const path = require('node:path');
const ROOT = path.resolve(__dirname, '..');
const marker = '[system-design bootstrap v1]';
function bootstrap(host = 'native') {
  const refs = path.join(ROOT, 'skills/system-design-enter/references');
  const policies = fs.readFileSync(path.join(refs, 'policies.md'), 'utf8');
  const mapping = fs.readFileSync(path.join(refs, 'host-tools.md'), 'utf8');
  return `${marker}\nSystem Design is available on ${host} for architecture discussion, static review and planning. Apply it only to relevant architecture requests, not every conversation. Load the requested skill, or system-design-enter when routing is unclear. Do not recursively reload enter.\nInstalled skills root: ${path.join(ROOT, 'skills')}\nThe shared policies below are already loaded. Resolve sibling references relative to the installed skill path.\n\n${policies}\n\n${mapping}`;
}
module.exports = { bootstrap, marker, ROOT };
