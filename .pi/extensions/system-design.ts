// No SDK runtime dependency. Pi supplies the extension API.
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { bootstrap, marker } = require('../../integrations/bootstrap.cjs');
export default function systemDesign(pi) {
  pi.on('context', async event => {
    const found = event.messages.some(message => Array.isArray(message.content) &&
      message.content.some(part => part.type === 'text' && part.text?.startsWith(marker)));
    if (found) return;
    const message = {role:'user', content:[{type:'text',text:bootstrap('Pi')}], timestamp:Date.now()};
    let offset = 0;
    while (event.messages[offset]?.role === 'compactionSummary') offset++;
    return {messages:[...event.messages.slice(0,offset),message,...event.messages.slice(offset)]};
  });
}
