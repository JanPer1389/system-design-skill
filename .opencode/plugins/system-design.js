// Native host adapters share the same installed skills and policy source.
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
const require = createRequire(import.meta.url);
const { bootstrap, marker, ROOT } = require('../../integrations/bootstrap.cjs');
const skillsDir = path.join(ROOT, 'skills');
const hasBootstrap = parts => parts.some(p => p.type === 'text' && p.text?.startsWith(marker));

export const SystemDesignPlugin = async () => ({
  config: async config => {
    if (Array.isArray(config.skills)) return; // V2 registers through setup.
    config.skills ??= {};
    config.skills.paths ??= [];
    if (!config.skills.paths.includes(skillsDir)) config.skills.paths.push(skillsDir);
  },
  'experimental.chat.messages.transform': async (_input, output) => {
    const user = output.messages.find(m => m.info.role === 'user');
    if (!user || !user.parts.length || hasBootstrap(user.parts)) return;
    user.parts.unshift({...user.parts[0], type:'text', text:bootstrap('OpenCode V1')});
  }
});

async function setup(ctx) {
  if (!ctx?.skill?.transform || !ctx?.session?.hook) return; // V1 uses named export.
  const skills = fs.readdirSync(skillsDir).filter(name => fs.existsSync(path.join(skillsDir,name,'SKILL.md')))
    .map(name => {
      const file = path.join(skillsDir,name,'SKILL.md');
      const text = fs.readFileSync(file,'utf8');
      const description = text.match(/^description: (.+)$/m)?.[1];
      return {id:name, name, description, path:file, content:text.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '')};
    });
  await ctx.skill.transform(draft => { for (const skill of skills) draft.add(skill); });
  const inject = async event => {
    if (!Array.isArray(event.messages)) return;
    const user = event.messages.find(m => m.role === 'user');
    if (user && (!Array.isArray(user.content) || hasBootstrap(user.content))) return;
    const part = {type:'text', text:bootstrap('OpenCode V2')};
    if (user) user.content.unshift(part);
    else event.messages.push({role:'user',content:[part]});
  };
  for (const event of ['context','compaction','generate']) await ctx.session.hook(event, inject);
}
export default {id:'system-design', server:SystemDesignPlugin, setup};
