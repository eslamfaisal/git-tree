// Course journey: open a repository from the New Tab page with the Open card and the folder picker,
// then with Ctrl+O, and see what GitTree says about a folder that is not a repository.
// The app starts without a repository (openRepo: false) at the `clean` checkpoint of course/demo-repo.
//
// The folder picker is the operating system's own dialog (GTK on Linux), outside the webview, so WebDriver cannot reach it:
// it is driven with xdotool (keyboard only), and moved and sized to sit in the middle of the window (no window manager
// runs under Xvfb, so it would otherwise open oversized and unframed). Dropping a folder cannot be driven, so it is only
// mentioned; the hint on the New Tab page that announces it is on screen.
import { spawnSync } from 'node:child_process';
import { cpSync, mkdirSync, rmSync, writeFileSync } from 'node:fs';

const sh = (command) => spawnSync('bash', ['-c', command], { encoding: 'utf8' }).stdout.trim();
const SCALE = Number(process.env.OGT_DEMO_SCALE ?? 3);
const WIDTH = Number(process.env.OGT_DEMO_WIDTH ?? 1280);
const HEIGHT = Number(process.env.OGT_DEMO_HEIGHT ?? 720);

const BUILT = '/tmp/ogt-demo-open-a-repository/demo-repo'; // what record.mjs builds from the checkpoint
const PROJECTS = '/tmp/projects';
const LUMEN = `${PROJECTS}/lumen`;
const PLAIN = `${PROJECTS}/recipes`; // a folder that is not a repository

// The picker as it is placed: 600 x 400 window px in the middle of the window.
const PICKER = { x: 340, y: 160, w: 600, h: 400 };

/** Waits for the native picker, sizes it, and returns once it is on screen. */
async function waitForPicker(ui) {
  let id = '';
  for (let i = 0; i < 150 && !id; i++) {
    id = sh('xdotool search --onlyvisible --name "Open a repository" | tail -1'); // a closed picker lingers, unmapped
    if (!id) await ui.sleep(40);
  }
  if (!id) throw new Error('the folder picker did not open');
  const want = `Geometry: ${PICKER.w * SCALE}x${PICKER.h * SCALE}`;
  // GTK resizes the window again while it maps; place it until it stays put.
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
  return id;
}

/** Types a folder into the picker's location field and confirms with Open. */
async function chooseFolder(ui, folder) {
  sh('xdotool key alt+Home'); // leave the "Recent" view
  await ui.sleep(500);
  sh('xdotool key ctrl+l');
  await ui.sleep(500);
  sh(`xdotool type --delay 85 "${folder}/"`);
  await ui.sleep(900);
  await ui.mark(`path-typed-${folder.split('/').pop()}`);
  sh('xdotool key Return'); // goes into the folder
  await ui.sleep(1200);
  sh('xdotool key alt+o'); // the Open button
}

export default {
  name: 'open-a-repository',
  wip: false,
  quietTooltips: true,
  openRepo: false,
  park: { x: 900, y: 600 },

  async prepare() {
    rmSync(PROJECTS, { recursive: true, force: true });
    mkdirSync(PLAIN, { recursive: true });
    writeFileSync(`${PLAIN}/pancakes.txt`, 'Two eggs, one cup of flour, milk.\n');
    cpSync(BUILT, LUMEN, { recursive: true });
  },

  async run(ui, browser) {
    await ui.mark('start');
    await ui.sleep(1200);
    // The hint at the bottom of the page announces the drop target; tag it so a box can outline it.
    await browser.execute(() => {
      const hint = [...document.querySelectorAll('p')].find((p) => /drop a folder onto this window/.test(p.textContent ?? ''));
      hint?.setAttribute('data-demo', 'drop-hint');
    });
    const cards = await ui.find('button', /^Open/, { first: true });
    await ui.mark('new-tab');
    await ui.hoverSelector(cards, { at: [0.5, 0.5], duration: 900 });
    await ui.mark('open-card', cards);
    await ui.sleep(5200); // the three cards
    await ui.mark('drop-hint-begin');
    await ui.hoverSelector('[data-demo="drop-hint"]', { at: [0.5, 0.5], duration: 800 });
    await ui.sleep(300);
    await ui.mark('drop-hint', '[data-demo="drop-hint"]');
    await ui.sleep(4200); // the hint about dropping a folder
    await ui.mark('new-tab-end');

    await browser.execute(() => document.querySelector('[data-demo="drop-hint"]')?.closest('.overflow-auto')?.scrollTo(0, 0));
    await ui.sleep(500);
    await ui.mark('click-open');
    await ui.hoverSelector(cards, { at: [0.5, 0.5], duration: 800 });
    await ui.sleep(800);
    await ui.clickSelector(cards, { after: 200 });
    await waitForPicker(ui);
    await ui.mark('picker-shown');
    await ui.mark('picker', PICKER);
    await ui.sleep(4400); // the picker, while it is explained
    await ui.mark('choose-begin');
    await chooseFolder(ui, LUMEN);
    await ui.mark('choose-end');

    await ui.find('grid', 'Commit history', { timeout: 30_000 });
    await ui.mark('opened');
    const tab = await ui.find('tab', /^lumen/, { timeout: 10_000, first: true });
    await ui.mark('tab', tab);
    await ui.sleep(5800); // the tab and the graph
    await ui.mark('opened-end');

    await ui.mark('shortcut-begin');
    await ui.keys(['Control', 'o'], { after: 100 });
    await waitForPicker(ui);
    await ui.mark('shortcut-picker');
    await ui.sleep(4200);
    await ui.mark('plain-begin');
    await chooseFolder(ui, PLAIN);
    const refused = await ui.dialog(/not a Git repository/);
    await ui.mark('refused', refused);
    await ui.mark('refused-shown');
    await ui.sleep(6000); // what GitTree says about a plain folder
    await ui.click('button', 'Close', { first: true, after: 900 });
    await ui.mark('end');
    await ui.sleep(500);
  },
};
