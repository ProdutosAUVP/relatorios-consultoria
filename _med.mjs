import { chromium } from 'playwright';
import { readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
function fc(){const b=process.env.PLAYWRIGHT_BROWSERS_PATH;if(!b||!existsSync(b))return undefined;
for(const d of readdirSync(b).filter(x=>x.startsWith('chromium-')).sort().reverse()){const e=join(b,d,'chrome-linux','chrome');if(existsSync(e))return e;}}
let br;try{br=await chromium.launch();}catch(e){br=await chromium.launch({executablePath:fc()});}
const pg=await br.newPage();
await pg.goto('file://'+process.argv[2]);await pg.waitForTimeout(300);
console.log(await pg.evaluate(()=>[...document.querySelectorAll('.slide')].slice(0,2).map((s,i)=>{
  const g=s.querySelector('.graf'); if(!g) return `slide ${i+1}: sem graf`;
  const sb=s.getBoundingClientRect(), gb=g.getBoundingClientRect();
  const sv=g.querySelector('svg').getBoundingClientRect();
  return `slide ${i+1}: graf w=${gb.width.toFixed(1)} h=${gb.height.toFixed(1)} `+
    `dir=${(sb.right-gb.right).toFixed(1)} topo=${(gb.top-sb.top).toFixed(1)} base=${(sb.bottom-gb.bottom).toFixed(1)} `+
    `| svg w=${sv.width.toFixed(1)} h=${sv.height.toFixed(1)}`;
}).join('\n')));
await br.close();
