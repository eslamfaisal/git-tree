// Course journey: the Recent list on the New Tab page: reopen a repository from it, then remove one entry
// (the files stay). Starts at the `clean` checkpoint of course/demo-repo without a repository (openRepo: false).
//
// `prepare` fills the Recent list before the capture starts: it opens three repositories through the app's own
// Open flow (the system folder picker, driven with xdotool: it is outside the webview) and closes their tabs.
import { spawnSync } from 'node:child_process';
import { cpSync, mkdirSync, rmSync, writeFileSync } from 'node:fs';

const sh = (command) => spawnSync('bash', ['-c', command], { encoding: 'utf8' }).stdout.trim();
const SCALE = Number(process.env.OGT_DEMO_SCALE ?? 3);

const BUILT = '/tmp/ogt-demo-recent-repositories/demo-repo'; // what record.mjs builds from the checkpoint
const CODE = '/tmp/code';
const PICKER = { x: 340, y: 160, w: 600, h: 400 };

async function waitForPicker(ui) {
  let id = '';
  for (let i = 0; i < 150 && !id; i++) {
    id = sh('xdotool search --onlyvisible --name "Open a repository" | tail -1'); // a closed picker lingers, unmapped
    if (!id) await ui.sleep(40);
  }
  if (!id) throw new Error('the folder picker did not open');
  const want = `Geometry: ${PICKER.w * SCALE}x${PICKER.h * SCALE}`;
  for (let i = 0; i < 30; i++) {
    sh(
      `xdotool windowsize ${id} ${PICKER.w * SCALE} ${PICKER.h * SCALE} windowmove ${id} ${PICKER.x * SCALE} ${PICKER.y * SCALE} windowfocus ${id}`,
    );
    await ui.sleep(150);
    if (sh(`xdotool getwindowgeometry ${id}`).includes(want)) {
      await ui.sleep(300);
      if (sh(`xdotool getwindowgeometry ${id}`).includes(want)) break;
    }
  }
  await ui.sleep(500);
}

async function chooseFolder(ui, folder) {
  sh('xdotool key alt+Home');
  await ui.sleep(400);
  sh('xdotool key ctrl+l');
  await ui.sleep(400);
  sh(`xdotool type --delay 20 "${folder}/"`);
  await ui.sleep(500);
  sh('xdotool key Return');
  await ui.sleep(900);
  sh('xdotool key alt+o');
}

/** Opens `folder` through the Open card or Ctrl+O, waits for its tab, then closes the tab again. */
async function openAndClose(ui, folder, name) {
  await ui.keys(['Control', 'o'], { after: 100 });
  await waitForPicker(ui);
  await chooseFolder(ui, folder);
  try { await ui.find('tab', new RegExp(`^${name}`), { timeout: 8_000, first: true }); } catch (e) { spawnSync('ffmpeg', ['-y','-loglevel','error','-f','x11grab','-video_size','3840x2160','-i',process.env.DISPLAY,'-frames:v','1','-vf','scale=1280:720','/tmp/jtest-author1/fail.png']); throw e; }
  await ui.sleep(1500);
  await ui.keys(['Control', 'w'], { after: 1200 });
}

function makeSmallRepo(dir, files) {
  mkdirSync(dir, { recursive: true });
  mkdirSync(`${dir}/docs`); // a second folder: with only .git in it, the picker would complete the path to .git/
  writeFileSync(`${dir}/docs/about.md`, 'About this project.\n');
  for (const [name, text] of Object.entries(files)) writeFileSync(`${dir}/${name}`, text);
  sh(`cd ${dir} && git init -q -b main && git add -A && git commit -q -m "Start the project"`);
}

export default {
  name: 'recent-repositories',
  wip: false,
  quietTooltips: true,
  openRepo: false,
  park: { x: 900, y: 600 },

  async prepare(ui) {
    rmSync(CODE, { recursive: true, force: true });
    mkdirSync(CODE, { recursive: true });
    cpSync(BUILT, `${CODE}/lumen`, { recursive: true });
    makeSmallRepo(`${CODE}/atlas`, { 'README.md': '# Atlas\n\nA map of the office.\n', 'rooms.txt': 'kitchen\nlibrary\n' });
    makeSmallRepo(`${CODE}/notes`, { 'todo.md': '- water the plants\n', 'ideas.md': '- a new logo\n' });
    // Oldest first: the most recently opened sits at the top of the list.
    await openAndClose(ui, `${CODE}/notes`, 'notes');
    await openAndClose(ui, `${CODE}/atlas`, 'atlas');
    await openAndClose(ui, `${CODE}/lumen`, 'lumen');
    await ui.sleep(800);
  },

  async run(ui, browser) {
    // Smoothly scrolls the New Tab page so the Recent list sits at the top of the window.
    const showRecent = async () => {
      await browser.execute(() => {
        const list = document.querySelector('section[aria-label="Recent"]');
        const page = list?.closest('.overflow-auto');
        if (page && list) page.scrollTo({ top: page.scrollTop + list.getBoundingClientRect().top - 150, behavior: 'smooth' });
      });
      await ui.sleep(900);
    };
    const recent = () => ui.find('region', 'Recent');
    // The Saved list above has rows with the same names: pick the one inside the Recent list.
    const inRecent = async (role, name) => {
      for (const match of await ui.queryAll({ role, name })) {
        const inside = await browser.execute(
          (css) => Boolean(document.querySelector(css)?.closest('section[aria-label="Recent"]')),
          match.selector,
        );
        if (inside) return match.selector;
      }
      throw new Error(`no ${role} ${String(name)} in the Recent list`);
    };

    await ui.mark('start');
    await ui.sleep(3600); // the New Tab page, the Saved list above the Recent list
    await ui.mark('scroll');
    await showRecent();
    const list = await recent();
    await ui.mark('recent', list);
    await ui.hoverSelector(list, { at: [0.5, 0.35], duration: 800 });
    await ui.sleep(7200); // three rows: name, folder, when
    await ui.mark('list-end');

    await ui.mark('reopen-begin');
    const atlas = await inRecent('button', /^Open atlas \(/);
    await ui.mark('atlas-row', atlas);
    await ui.hoverSelector(atlas, { at: [0.3, 0.5], duration: 800 });
    await ui.sleep(1800);
    await ui.clickSelector(atlas, { after: 300 });
    await ui.find('tab', /^atlas/, { timeout: 20_000, first: true });
    await ui.mark('reopened');
    await ui.sleep(4200); // the repository is back in a tab
    await ui.mark('reopen-end');

    await ui.mark('newtab-begin');
    await ui.keys(['Control', 't'], { after: 900 });
    await showRecent();
    await ui.mark('newtab-shown');
    const list2 = await recent();
    await ui.mark('recent-again', list2);
    await ui.hoverSelector(list2, { at: [0.5, 0.35], duration: 600 });
    await ui.sleep(5200); // atlas is now at the top
    await ui.mark('newtab-end');

    await ui.mark('remove-begin');
    const remove = await inRecent('button', /^Remove notes from recents/);
    await ui.hoverSelector(remove, { duration: 900 });
    await ui.mark('remove-button', remove);
    await ui.sleep(2600);
    await ui.clickSelector(remove, { after: 100 });
    await ui.hoverSelector('body', { at: [0.8, 0.6], duration: 700 }); // off the row that slid under the pointer
    await ui.sleep(500);
    await ui.mark('removed');
    const list3 = await recent();
    await ui.mark('recent-after', list3);
    await ui.hoverSelector(list3, { at: [0.5, 0.2], duration: 700 });
    await ui.sleep(4600); // two rows left
    await ui.mark('remove-end');

    await ui.mark('star-begin');
    const star = await inRecent('button', /^Favourite lumen/);
    await ui.hoverSelector(star, { duration: 900 });
    await ui.mark('star-button', star);
    await ui.sleep(4400); // hovered, not clicked
    await ui.mark('end');
    await ui.sleep(500);
  },
};
